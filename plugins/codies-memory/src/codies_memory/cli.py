"""CLI entry points for codies-memory."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from codies_memory import __version__
from codies_memory.vault import (
    ensure_general_project_vault,
    init_global_vault,
    init_project_vault,
    validate_vault,
    resolve_global_vault,
    resolve_project_vault,
)
from codies_memory.boot import assemble_boot
from codies_memory import favorites
from codies_memory.inbox import capture, pending_review
from codies_memory.records import (
    append_daily_log,
    create_record,
    list_records,
    read_record,
    SHORT_TEXT_LIMIT,
    sanitize_short_text,
    update_record,
)
from codies_memory.promotion import evaluate_for_promotion, promote_within_project, promote_to_global
from codies_memory.profile import load_profile, get_write_gate_bias
from codies_memory.warm import write_warm_artifacts
from codies_memory import transcripts


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_agent(args: argparse.Namespace) -> str:
    """Resolve agent name from --agent flag."""
    agent = getattr(args, "agent", None)
    if not agent:
        print("Error: --agent flag is required.", file=sys.stderr)
        sys.exit(1)
    return agent


def _require_global_vault(args: argparse.Namespace) -> Path:
    agent = _resolve_agent(args)
    vault = resolve_global_vault(agent)
    if not (vault / "registry" / "projects.yaml").is_file():
        print(
            f"Error: global vault is not initialized. Run 'codies-memory init --type global --agent {agent}' first.",
            file=sys.stderr,
        )
        sys.exit(1)
    return vault


def _nonnegative_int(value: str) -> int:
    count = int(value)
    if count < 0:
        raise argparse.ArgumentTypeError("must be a non-negative integer")
    return count


def _resolve_project_vault(
    args: argparse.Namespace,
    *,
    fallback_to_general: bool = False,
) -> tuple[Path, Path]:
    """Resolve global and project vault paths from args.

    Returns (global_vault, project_vault).
    Exits with error if no project vault is found unless *fallback_to_general*
    is true, in which case the reserved ``_general`` project vault is created
    if needed and returned.
    """
    global_vault = _require_global_vault(args)
    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)
    if project_vault is None:
        if fallback_to_general:
            return global_vault, ensure_general_project_vault(global_vault)
        print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
        sys.exit(1)
    return global_vault, project_vault


def _resolve_project_vault_for_read(
    args: argparse.Namespace,
    global_vault: Path,
) -> tuple[Path | None, Path]:
    """Resolve project context for read commands.

    Normal reads use the working directory. Explicit ``--general`` reads use
    the reserved catch-all project vault and create it if an older global vault
    does not have it yet.
    """
    working_dir = (
        Path(args.working_dir).resolve()
        if getattr(args, "working_dir", None)
        else Path.cwd()
    )
    if getattr(args, "general", False):
        return ensure_general_project_vault(global_vault), working_dir
    return resolve_project_vault(global_vault, working_dir), working_dir


def _format_usage_line(name: str, stats: dict) -> str:
    """Format one boot-budget line; flag slices at 90%+ of capacity."""
    used = stats["used"]
    cap = stats["budget"]
    pct = (used / cap * 100) if cap else 0.0
    left = max(0, cap - used)
    line = f"{name}: {used}/{cap} tokens ({pct:.0f}%) — {left} left"
    if pct >= 90:
        line += "  ⚠ over 90% full"
    return line


def _short_from_args(given: str | None, fallback: str) -> str:
    """Sanitize ``--short`` (or *fallback*) and say on stderr when it had to be cut."""
    short = sanitize_short_text(given or fallback)
    if given and given.strip() and short != " ".join(given.split()):
        print(f"Note: --short is longer than {SHORT_TEXT_LIMIT} characters; shortened to: {short}",
              file=sys.stderr)
    return short


def _parse_field_value(value: str) -> object:
    """Return a ``--field`` value: "[a, b]" becomes the list ["a", "b"].

    Items keep their text exactly (no YAML typing: "on" stays "on", "001"
    stays "001"). A value starting with "[[" is a wikilink and stays a string.
    """
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")) or stripped.startswith("[["):
        return value
    # split on commas outside quotes; a quote opens only at the start of an item
    items, current, quote = [], "", None
    for ch in stripped[1:-1]:
        if quote:
            if ch == quote:
                quote = None
            else:
                current += ch
        elif ch in "'\"" and not current.strip():
            quote, current = ch, ""
        elif ch == ",":
            items.append(current.strip())
            current = ""
        else:
            current += ch
    items.append(current.strip())
    return [item for item in items if item]


def _normalize_inline_body(body: str) -> str:
    """Normalize inline body text from CLI flags.

    Shell quoting often leaves literal ``\\n`` sequences in ``--body`` values.
    Treat those as real newlines so inline record creation remains usable.
    """
    return body.replace("\\r\\n", "\n").replace("\\n", "\n")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    if args.type == "global":
        global_vault = resolve_global_vault(agent)
        init_global_vault(global_vault)
        print(f"Initialized global vault at {global_vault}")
    else:
        global_vault = _require_global_vault(args)
        working_dir = Path(args.working_dir).resolve() if args.working_dir else Path.cwd()
        slug = getattr(args, "slug", None)
        vault = init_project_vault(
            global_vault=global_vault,
            slug=slug,
            working_dir=working_dir,
        )
        print(f"Initialized project vault at {vault}")


def cmd_validate(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    if args.type == "global":
        path = global_vault
    else:
        global_vault = _require_global_vault(args)
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        project_vault = resolve_project_vault(global_vault, working_dir)
        if project_vault is None:
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)
        path = project_vault

    result = validate_vault(path, vault_type=args.type)
    if result.is_valid:
        print(f"Vault at {path} is valid.")
    else:
        print(f"Vault at {path} is INVALID.")
        if result.missing:
            print("Missing directories:")
            for d in result.missing:
                print(f"  {d}")
        if result.missing_files:
            print("Missing files:")
            for f in result.missing_files:
                print(f"  {f}")
        if result.extra:
            print("Invalid files:")
            for f in result.extra:
                print(f"  {f}")
        sys.exit(1)


def _transcript_context(args: argparse.Namespace, hook: dict, working_dir: Path) -> dict | None:
    """Collect harness, current session and directory for transcript checks.

    Hook input wins over the environment, the environment over nothing. Returns
    ``None`` when the harness cannot be told. The hook's transcript folder is
    used only while the hook's directory is the one boot works in.
    """
    transcript_path = hook.get("transcript_path")
    harness = (
        getattr(args, "harness", None)
        or transcripts.harness_from_path(transcript_path)
        or transcripts.detect_harness()
    )
    if harness is None:
        return None
    transcript_dir = None
    hook_cwd = Path(hook["cwd"]).resolve() if hook.get("cwd") else None
    if harness == "claude-code" and transcript_path and hook_cwd == working_dir:
        transcript_dir = Path(transcript_path).parent
    return {
        "harness": harness,
        "current_id": hook.get("session_id") or transcripts.current_session_id(harness),
        "source": hook.get("source"),
        "working_dir": working_dir,
        "transcript_dir": transcript_dir,
    }


def cmd_boot(args: argparse.Namespace) -> None:
    global_vault = _require_global_vault(args)

    # One directory for everything boot does: --working-dir, else the hook's
    # cwd, else the process's.
    hook = transcripts.read_hook_input(args.hook_input) if getattr(args, "hook_input", None) else {}
    if hook.get("cwd") and not getattr(args, "working_dir", None):
        args.working_dir = str(hook["cwd"])  # --general picks the vault, not the directory
    project_vault, working_dir = _resolve_project_vault_for_read(args, global_vault)
    context = _transcript_context(args, hook, working_dir)

    if project_vault is None:
        print("Warning: no project vault found; global-only boot.", file=sys.stderr)
    elif getattr(args, "general", False):
        print("Using reserved _general project vault.", file=sys.stderr)

    # Rebuild warm summaries so boot never serves stale derived artifacts.
    write_warm_artifacts(global_vault, project_vault=project_vault)

    packet = assemble_boot(
        global_vault=global_vault,
        project_vault=project_vault,
        branch=args.branch,
        budget=args.budget,
    )
    print("=== Global Packet ===")
    print(packet["global_packet"])
    print()
    print("=== Project Packet ===")
    print(packet["project_packet"])

    if context is not None:
        agent = _resolve_agent(args)
        if context["source"] == "compact":
            print()
            print("=== Checkpoint ===")
            print(transcripts.render_checkpoint(agent, context["current_id"]))
        try:
            items = transcripts.open_transcripts(
                global_vault,
                context["harness"],
                context["working_dir"],
                current_id=context["current_id"],
                transcript_dir=context["transcript_dir"],
            )
        except OSError as exc:
            items = []
            print(f"Warning: could not read transcripts: {exc}", file=sys.stderr)
        warning = transcripts.transcript_retention_warning() if context["harness"] == "claude-code" else None
        section = transcripts.render_open_section(items, agent, context["harness"], warning=warning)
        if section:
            print()
            print("=== Open Sessions ===")
            print(section)

    agent = _resolve_agent(args)
    due = [(kind, favorites.due_reason(global_vault, kind)) for kind in favorites.KINDS]
    due = [(kind, reason) for kind, reason in due if reason]
    if due:
        print()
        print("=== Favorites Due ===")
        for kind, reason in due:
            print(f"- {kind}: {reason}. Choose your three favorites again: "
                  f"codies-memory favorites {kind} ID ID ID --why \"...\" --why \"...\" --why \"...\" "
                  f"--agent {agent}")

    usage = packet["usage"]
    print()
    print("=== Boot Budget ===")
    print(f"identity: {usage['identity']['used']} tokens (exempt — no limit)")
    for name in ("favorite_reflections", "favorite_dreams"):
        if usage[name]["used"]:
            print(f"{name}: {usage[name]['used']} tokens (exempt — always in full)")
    reflection = usage["latest_reflection"]
    if reflection["used"]:
        print(f"latest_reflection: {reflection['used']} tokens (exempt — own cap {reflection['cap']})")
    for name, stats in usage["layers"].items():
        print(_format_usage_line(name, stats))
    print(_format_usage_line("total", usage["total"]))


def cmd_capture(args: argparse.Namespace) -> None:
    global_vault, project_vault = _resolve_project_vault(args, fallback_to_general=True)

    gate = args.gate
    if gate is None:
        profile = load_profile(global_vault, project_vault)
        gate = get_write_gate_bias(profile)

    short = _short_from_args(getattr(args, "short", None), args.content[:80])
    record_path = capture(
        vault=project_vault,
        content=args.content,
        source=args.source,
        gate=gate,
    )
    update_record(record_path, short=short)

    record = read_record(record_path)
    append_daily_log(global_vault, record["frontmatter"]["id"], short, project_vault.name)
    print(record["frontmatter"]["id"])


def cmd_create(args: argparse.Namespace) -> None:
    global_vault = _require_global_vault(args)

    # Global-only types: auto-route to global scope
    GLOBAL_ONLY_TYPES = {"reflection", "dream", "skill", "playbook", "identity"}
    if args.type in GLOBAL_ONLY_TYPES and args.scope == "project":
        args.scope = "global"

    # Read body from --body or --body-file
    body = getattr(args, "body", None)
    body_file = getattr(args, "body_file", None)
    if body_file:
        body = Path(body_file).read_text(encoding="utf-8")
    elif body is not None:
        body = _normalize_inline_body(body)
    if not body:
        print("Error: --body or --body-file is required.", file=sys.stderr)
        sys.exit(1)

    scope = args.scope
    trust = args.trust

    # Parse extra --field key=value pairs
    extra: dict = {}
    for field_str in (args.field or []):
        if "=" not in field_str:
            print(f"Error: --field must be key=value, got: {field_str!r}", file=sys.stderr)
            sys.exit(1)
        key, value = field_str.split("=", 1)
        extra[key] = _parse_field_value(value)
    short = _short_from_args(getattr(args, "short", None), args.title)
    extra["short"] = short

    # A session summary links to the transcript it covers: the one named with
    # --transcript, else the session this command runs in. It covers the
    # transcript up to --covered-until (what a digest showed), else up to now.
    link_flags = [
        flag for flag, value in (
            ("--transcript", getattr(args, "transcript", None)),
            ("--covered-until", getattr(args, "covered_until", None) is not None),
            ("--checkpoint", getattr(args, "checkpoint", False)),
        ) if value
    ]
    if args.type == "session":
        transcript_id = getattr(args, "transcript", None) or transcripts.current_session_id()
        covered_until = datetime.now(timezone.utc)
        if getattr(args, "covered_until", None) is not None:
            covered_until = transcripts.parse_time(args.covered_until)
            if covered_until is None:
                print(f"Error: --covered-until is not an ISO time: {args.covered_until!r}", file=sys.stderr)
                sys.exit(1)
        if transcript_id:
            extra["transcript"] = transcript_id
            extra["transcript_covered_at"] = transcripts.isoformat(covered_until)
            if getattr(args, "checkpoint", False):
                extra["transcript_checkpoint"] = True
        elif link_flags:
            print(f"Error: {', '.join(link_flags)} needs --transcript outside an agent session.", file=sys.stderr)
            sys.exit(1)
    elif link_flags:
        print(f"Error: {', '.join(link_flags)} only applies to session records.", file=sys.stderr)
        sys.exit(1)

    # Resolve vault
    if scope == "global":
        vault = global_vault
        project_slug = "global"
    else:
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
        if vault is None:
            vault = ensure_general_project_vault(global_vault)
        project_slug = vault.name

    record_path = create_record(
        vault=vault,
        record_type=args.type,
        scope=scope,
        title=args.title,
        body=body,
        trust=trust,
        **extra,
    )

    record = read_record(record_path)
    append_daily_log(global_vault, record["frontmatter"]["id"], short, project_slug)
    print(record["frontmatter"]["id"])
    kind = {"reflection": "reflections", "dream": "dreams"}.get(args.type)
    if kind:
        _favorites_reminder(global_vault, kind, _resolve_agent(args))


def _favorites_reminder(global_vault: Path, kind: str, agent: str) -> None:
    """After a new reflection or dream: the pick of favorites is due (or, before the first pick, possible)."""
    command = (f"codies-memory favorites {kind} ID ID ID --why \"...\" --why \"...\" --why \"...\" "
               f"--agent {agent}")
    try:
        picked = favorites.load_favorites(global_vault, kind) is not None
    except favorites.FavoritesError:
        picked = True
    if picked:
        print(f"Now choose your three favorite {kind} again (due after every new one): {command}. "
              f"Boot reports the pick as due until you do.", file=sys.stderr)
    else:
        print(f"Tip: pick your three favorite {kind} and boot shows them in full: {command}",
              file=sys.stderr)


def cmd_favorites(args: argparse.Namespace) -> None:
    """Show or set the agent's three favorite reflections or dreams."""
    global_vault = _require_global_vault(args)
    kind = args.kind
    if args.ids:
        try:
            path = favorites.save_favorites(global_vault, kind, args.ids, args.why or [])
        except favorites.FavoritesError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"Favorite {kind} saved: {', '.join(args.ids)} ({path.relative_to(global_vault)})")
        return

    try:
        current = favorites.load_favorites(global_vault, kind)
    except favorites.FavoritesError as exc:
        print(f"Error: {exc}; choosing again rewrites it.", file=sys.stderr)
        sys.exit(1)
    if current is None:
        print(f"No favorite {kind} chosen yet. Pick with: codies-memory favorites {kind} ID ID ID "
              f"--why \"...\" --why \"...\" --why \"...\" --agent {_resolve_agent(args)}")
        return
    print(f"Favorite {kind} (chosen {current['chosen']}, after {current['after'] or 'none'}):")
    for pick in current["favorites"]:
        print(f"- {pick['id']} {pick.get('title', '')}: {pick.get('why', '')}")
    reason = favorites.due_reason(global_vault, kind)
    if reason:
        print(f"Due again: {reason}.")


def cmd_promote(args: argparse.Namespace) -> None:
    global_vault = _require_global_vault(args)

    source_path = Path(args.source).resolve()
    if not source_path.is_file():
        print(f"Error: source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "check", False):
        source = read_record(source_path)
        if source["frontmatter"].get("type") not in {"inbox", "thread"}:
            print("Error: --check supports inbox and thread records only.", file=sys.stderr)
            sys.exit(1)
        result = evaluate_for_promotion(source, context={
            "session_count": args.session_count,
            "references": args.references,
        })
        print(json.dumps(result, indent=2))
        return

    to_type = getattr(args, "to", None)
    to_global = getattr(args, "to_global", False)

    if to_global and to_type:
        print("Error: --to and --to-global are mutually exclusive.", file=sys.stderr)
        sys.exit(1)
    if not to_global and not to_type:
        print("Error: one of --to or --to-global is required.", file=sys.stderr)
        sys.exit(1)

    if to_global:
        new_path = promote_to_global(source_path, global_vault)
    else:
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        project_vault = resolve_project_vault(global_vault, working_dir)
        if project_vault is None:
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)
        new_path = promote_within_project(source_path, to_type, project_vault)

    record = read_record(new_path)
    print(record["frontmatter"]["id"])


def cmd_list(args: argparse.Namespace) -> None:
    global_vault = _require_global_vault(args)
    scope = args.scope

    if scope == "global":
        if getattr(args, "general", False):
            print("Error: --general can only be used with --scope project.", file=sys.stderr)
            sys.exit(1)
        vault = global_vault
    else:
        vault, working_dir = _resolve_project_vault_for_read(args, global_vault)
        if vault is None:
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)

    # Map user-facing plural names to record types
    type_aliases = {
        "inbox": "inbox",
        "threads": "thread",
        "thread": "thread",
        "lessons": "lesson",
        "lesson": "lesson",
        "decisions": "decision",
        "decision": "decision",
        "sessions": "session",
        "session": "session",
        "daily-logs": "daily-log",
        "daily-log": "daily-log",
        "reflections": "reflection",
        "reflection": "reflection",
        "dreams": "dream",
        "dream": "dream",
    }
    record_type = type_aliases.get(args.type, args.type)

    # Build filters
    filters: dict = {}
    if args.status:
        filters["status"] = args.status
    if args.trust:
        filters["trust"] = args.trust

    records = list_records(vault, record_type, scope=scope, **filters)

    fmt = args.format
    if fmt == "json":
        output = []
        for r in records:
            entry = dict(r["frontmatter"])
            entry["path"] = str(r["path"])
            output.append(entry)
        print(json.dumps(output, indent=2, default=str))
    elif fmt == "paths":
        for r in records:
            print(r["path"])
    else:
        # table format
        if not records:
            print("No records found.")
            return

        # Header
        print(f"{'ID':<12}{'Title':<46}{'Status':<10}{'Trust':<12}{'Created'}")
        for r in records:
            fm = r["frontmatter"]
            rec_id = str(fm.get("id", ""))[:11]
            title = str(fm.get("title", ""))[:45]
            status = str(fm.get("status", ""))[:9]
            trust = str(fm.get("trust", ""))[:11]
            created = str(fm.get("created", ""))[:10]
            print(f"{rec_id:<12}{title:<46}{status:<10}{trust:<12}{created}")


def cmd_status(args: argparse.Namespace) -> None:
    global_vault = _require_global_vault(args)

    project_vault, working_dir = _resolve_project_vault_for_read(args, global_vault)

    if project_vault is None:
        print(f"Global vault: {global_vault}")
        print(f"Project vault: none (no project initialized for {working_dir})")
        print("\nRun 'codies-memory init --type project' to initialize a project vault here.")
        return

    result = pending_review(project_vault)
    active = result.get("active", [])
    aging = result.get("aging", [])
    stale = result.get("stale", [])

    print(f"Global vault: {global_vault}")
    print(f"Project vault: {project_vault}")
    print(f"\nActive: {len(active)}  Aging: {len(aging)}  Stale: {len(stale)}")

    if not active and not aging and not stale:
        print("Inbox is clean.")
        return

    show_all = getattr(args, "all", False)
    if show_all:
        if active:
            print(f"\nActive ({len(active)} item(s)):")
            for record in active:
                fm = record.get("frontmatter", {})
                title = fm.get("title", "(no title)")
                created = fm.get("created", "unknown")
                print(f"  [{created}] {title}")
        if aging:
            print(f"\nAging ({len(aging)} item(s)):")
            for record in aging:
                fm = record.get("frontmatter", {})
                title = fm.get("title", "(no title)")
                created = fm.get("created", "unknown")
                print(f"  [{created}] {title}")
        if stale:
            print(f"\nStale ({len(stale)} item(s)):")
            for record in stale:
                fm = record.get("frontmatter", {})
                title = fm.get("title", "(no title)")
                created = fm.get("created", "unknown")
                print(f"  [{created}] {title}")


def cmd_user(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)
    user_file = global_vault / "identity" / "user.md"

    if not user_file.exists():
        print(f"Error: identity files not initialized. Run 'codies-memory init --type global --agent {agent}' first.", file=sys.stderr)
        sys.exit(1)

    # Read existing content
    existing = user_file.read_text(encoding="utf-8")

    # Append bullet point
    bullet = f"- {args.observation}\n"
    if existing.rstrip().endswith("---") or existing.rstrip().endswith("---\n"):
        # Only frontmatter, no content yet — add a blank line first
        updated = existing.rstrip() + f"\n\n{bullet}"
    else:
        updated = existing.rstrip() + f"\n{bullet}"

    user_file.write_text(updated, encoding="utf-8")
    print(f"Noted: {args.observation[:60]}")


def cmd_feedback(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)
    feedback_dir = global_vault / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)

    import secrets
    from datetime import date
    today = date.today()
    suffix = secrets.token_hex(2)
    filename = f"FB-{today.strftime('%Y%m%d')}-{suffix}.md"
    title = args.message[:80]

    content = f"---\ntitle: \"{title}\"\nagent: {agent}\ncreated: '{today}'\n---\n\n{args.message}\n"
    path = feedback_dir / filename
    path.write_text(content, encoding="utf-8")
    print(f"Feedback saved: {filename}")


def cmd_refresh(args: argparse.Namespace) -> None:
    """Rebuild derived warm-memory artifacts."""
    global_vault = _require_global_vault(args)

    scope = getattr(args, "scope", "both")
    project_vault = None
    if scope in {"project", "both"}:
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        project_vault = resolve_project_vault(global_vault, working_dir)
        if project_vault is None and scope == "project":
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)

    if scope == "global":
        written = write_warm_artifacts(global_vault)
    elif scope == "project":
        written = write_warm_artifacts(global_vault, project_vault=project_vault)
    else:
        written = write_warm_artifacts(global_vault, project_vault=project_vault)

    for key, path in written.items():
        if scope == "global" and key != "global_summary":
            continue
        print(f"{key}: {path}")


def _transcript_harness(args: argparse.Namespace) -> str:
    harness = getattr(args, "harness", None) or transcripts.detect_harness()
    if harness is None:
        print("Error: cannot tell the harness; pass --harness claude-code or --harness codex.", file=sys.stderr)
        sys.exit(1)
    return harness


def cmd_transcripts(args: argparse.Namespace) -> None:
    """List, digest or skip session transcripts that lack a session summary."""
    global_vault = _require_global_vault(args)
    agent = _resolve_agent(args)
    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()

    if args.action == "open":
        harness = _transcript_harness(args)
        items = transcripts.open_transcripts(
            global_vault,
            harness,
            working_dir,
            current_id=transcripts.current_session_id(harness),
            days=args.days,
        )
        if args.format == "json":
            print(json.dumps([
                {
                    "session_id": o.transcript.session_id,
                    "harness": o.transcript.harness,
                    "path": str(o.transcript.path),
                    "label": o.transcript.label,
                    "started": o.transcript.started.isoformat() if o.transcript.started else None,
                    "last_activity": o.transcript.last_activity.isoformat() if o.transcript.last_activity else None,
                    "user_messages": o.transcript.user_messages,
                    "covered_at": o.covered_at.isoformat() if o.covered_at else None,
                    "covered_by_checkpoint": bool(o.covered and o.covered.checkpoint),
                }
                for o in items
            ], indent=2))
            return
        if not items:
            print("No open sessions.")
            return
        print(transcripts.render_open_section(items, agent, harness, limit=len(items)))
        return

    if not args.session_id:
        print(f"Error: transcripts {args.action} needs a session id.", file=sys.stderr)
        sys.exit(1)

    path = transcripts.locate_transcript(args.session_id, getattr(args, "harness", None), working_dir)

    if args.action == "skip":
        if not args.reason:
            print("Error: transcripts skip needs --reason.", file=sys.stderr)
            sys.exit(1)
        # The skip reaches as far as the transcript goes now; later user
        # messages open the session again.
        through = transcripts.read_transcript(path).last_activity if path else None
        if through is None:
            print(f"Error: cannot read how far {args.session_id} went (transcript not found or without times); "
                  "check --harness.", file=sys.stderr)
            sys.exit(1)
        transcripts.skip_transcript(global_vault, args.session_id, args.reason, through)
        print(f"Skipped {args.session_id}")
        return

    if path is None:
        print(f"Error: no transcript found for {args.session_id}", file=sys.stderr)
        sys.exit(1)
    transcript = transcripts.read_transcript(path)
    covered_at = None
    if not args.all:
        covered, legacy = transcripts.scan_records(global_vault)
        best = transcripts.best_coverage(transcript, covered, legacy)
        if best and best.at.year < 9999:
            covered_at = best.at
    print(transcripts.render_digest(transcript, covered_at=covered_at, max_chars=args.max_chars), end="")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="codies-memory",
        description="File-based two-tier memory system for AI agents.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- init ---
    init_parser = subparsers.add_parser("init", help="Initialize a vault.")
    init_parser.add_argument(
        "--agent",
        required=True,
        help="Agent name (e.g. claude).",
    )
    init_parser.add_argument(
        "--type",
        choices=["global", "project"],
        default="project",
        help="Vault type (default: project).",
    )
    init_parser.add_argument(
        "--slug",
        default=None,
        help="Project slug (defaults to directory name).",
    )
    init_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory for the project (defaults to cwd).",
    )
    init_parser.set_defaults(func=cmd_init)

    # --- validate ---
    validate_parser = subparsers.add_parser("validate", help="Validate vault structure.")
    validate_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    validate_parser.add_argument(
        "--type",
        choices=["global", "project"],
        default="project",
        help="Vault type (default: project).",
    )
    validate_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory for project vault resolution (defaults to cwd).",
    )
    validate_parser.set_defaults(func=cmd_validate)

    # --- boot ---
    boot_parser = subparsers.add_parser("boot", help="Assemble a boot packet.")
    boot_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    boot_parser.add_argument(
        "--branch",
        default="main",
        help="Branch name (default: main).",
    )
    boot_parser.add_argument(
        "--budget",
        type=int,
        default=12000,
        help="Token budget for non-identity layers; identity never counts (default: 12000).",
    )
    boot_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Project working directory (default: cwd).",
    )
    boot_parser.add_argument(
        "--general",
        action="store_true",
        default=False,
        help="Load the reserved _general project vault instead of resolving from the working directory.",
    )
    boot_parser.add_argument(
        "--harness",
        choices=list(transcripts.HARNESSES),
        default=None,
        help="Agent harness whose transcripts to check for sessions without a summary "
             "(default: detected from the hook input or the environment).",
    )
    boot_parser.add_argument(
        "--hook-input",
        dest="hook_input",
        default=None,
        help="SessionStart hook payload as a file, or - for stdin. Supplies the session id, "
             "the transcript folder, and whether the session was just compacted.",
    )
    boot_parser.set_defaults(func=cmd_boot)

    # --- status ---
    status_parser = subparsers.add_parser("status", help="Show inbox/review status.")
    status_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    status_parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="List individual items.",
    )
    status_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Project working directory (default: cwd).",
    )
    status_parser.add_argument(
        "--general",
        action="store_true",
        default=False,
        help="Read the reserved _general project vault instead of resolving from the working directory.",
    )
    status_parser.set_defaults(func=cmd_status)

    # --- capture ---
    capture_parser = subparsers.add_parser("capture", help="Capture an inbox item.")
    capture_parser.add_argument(
        "content",
        help="Content to capture.",
    )
    capture_parser.add_argument(
        "--source",
        required=True,
        help="Source of the capture (e.g. 'testing', 'review').",
    )
    capture_parser.add_argument(
        "--gate",
        default=None,
        help="Gate value (default: profile's write_gate_bias).",
    )
    capture_parser.add_argument(
        "--short",
        default=None,
        help="One-line summary for the global daily log.",
    )
    capture_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    capture_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory (defaults to cwd).",
    )
    capture_parser.set_defaults(func=cmd_capture)

    # --- create ---
    create_parser = subparsers.add_parser("create", help="Create a new record.")
    create_parser.add_argument(
        "type",
        choices=[
            "thread",
            "lesson",
            "decision",
            "session",
            "reflection",
            "dream",
            "skill",
            "playbook",
            "identity",
        ],
        help="Record type.",
    )
    create_parser.add_argument(
        "--title",
        required=True,
        help="Record title.",
    )
    body_group = create_parser.add_mutually_exclusive_group(required=True)
    body_group.add_argument(
        "--body",
        default=None,
        help="Record body text. Literal \\n sequences are normalized to newlines.",
    )
    body_group.add_argument(
        "--body-file",
        dest="body_file",
        default=None,
        help="Path to file containing record body. Preferred for rich multiline content.",
    )
    create_parser.add_argument(
        "--scope",
        choices=["project", "global"],
        default="project",
        help="Scope (default: project).",
    )
    create_parser.add_argument(
        "--trust",
        choices=["speculative", "working", "confirmed", "canonical"],
        default="working",
        help="Trust level (default: working).",
    )
    create_parser.add_argument(
        "--field",
        action="append",
        default=None,
        help="Extra frontmatter field as key=value (repeatable).",
    )
    create_parser.add_argument(
        "--short",
        default=None,
        help="One-line summary for the global daily log.",
    )
    create_parser.add_argument(
        "--transcript",
        default=None,
        help="Session id of the transcript a session record covers "
             "(default: the session this command runs in).",
    )
    create_parser.add_argument(
        "--covered-until",
        dest="covered_until",
        default=None,
        help="ISO time up to which the record covers the transcript; transcripts digest prints it "
             "(default: now).",
    )
    create_parser.add_argument(
        "--checkpoint",
        action="store_true",
        default=False,
        help="Mark a session record as an interim checkpoint (after a compaction), not a close.",
    )
    create_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    create_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory (defaults to cwd).",
    )
    create_parser.set_defaults(func=cmd_create)

    # --- list ---
    list_parser = subparsers.add_parser("list", help="List records.")
    list_parser.add_argument(
        "type",
        help="Record type (inbox, threads, lessons, decisions, sessions, daily-log, reflections, dreams).",
    )
    list_parser.add_argument(
        "--scope",
        choices=["project", "global"],
        default="project",
        help="Scope (default: project).",
    )
    list_parser.add_argument(
        "--status",
        default=None,
        help="Filter by status.",
    )
    list_parser.add_argument(
        "--trust",
        default=None,
        help="Filter by trust level.",
    )
    list_parser.add_argument(
        "--format",
        choices=["table", "json", "paths"],
        default="table",
        help="Output format (default: table).",
    )
    list_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    list_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory (defaults to cwd).",
    )
    list_parser.add_argument(
        "--general",
        action="store_true",
        default=False,
        help="List records from the reserved _general project vault instead of resolving from the working directory.",
    )
    list_parser.set_defaults(func=cmd_list)

    # --- promote ---
    promote_parser = subparsers.add_parser("promote", help="Promote a record.")
    promote_parser.add_argument(
        "source",
        help="Path to the source record file.",
    )
    promote_group = promote_parser.add_mutually_exclusive_group(required=True)
    promote_group.add_argument(
        "--to",
        default=None,
        help="Target type for within-project promotion (e.g. thread, lesson).",
    )
    promote_group.add_argument(
        "--to-global",
        dest="to_global",
        action="store_true",
        default=False,
        help="Promote to global vault.",
    )
    promote_group.add_argument(
        "--check",
        action="store_true",
        help="Evaluate inbox/thread promotion heuristics as JSON without changing the record.",
    )
    promote_parser.add_argument(
        "--session-count",
        type=_nonnegative_int,
        default=0,
        help="Observed sessions for this record, used with --check (default: 0).",
    )
    promote_parser.add_argument(
        "--references",
        type=_nonnegative_int,
        default=0,
        help="Observed references to this record, used with --check (default: 0).",
    )
    promote_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    promote_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory (defaults to cwd).",
    )
    promote_parser.set_defaults(func=cmd_promote)

    # --- user ---
    user_parser = subparsers.add_parser("user", help="Save an observation about the user to identity/user.md.")
    user_parser.add_argument(
        "observation",
        help="What you learned about the user.",
    )
    user_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    user_parser.set_defaults(func=cmd_user)

    # --- feedback ---
    feedback_parser = subparsers.add_parser("feedback", help="Report a bug, issue, or observation about the memory system.")
    feedback_parser.add_argument(
        "message",
        help="The feedback text.",
    )
    feedback_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    feedback_parser.set_defaults(func=cmd_feedback)

    # --- favorites ---
    favorites_parser = subparsers.add_parser(
        "favorites",
        help="Show or choose your three favorite reflections or dreams; boot shows them in full.",
    )
    favorites_parser.add_argument("kind", choices=list(favorites.KINDS), help="reflections or dreams.")
    favorites_parser.add_argument(
        "ids",
        nargs="*",
        help=f"Ids of your {favorites.FAVORITE_COUNT} favorites (omit to show the current pick).",
    )
    favorites_parser.add_argument(
        "--why",
        action="append",
        default=None,
        help="Why you keep it; once per id, in the same order.",
    )
    favorites_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    favorites_parser.set_defaults(func=cmd_favorites)

    # --- refresh ---
    refresh_parser = subparsers.add_parser("refresh", help="Rebuild derived warm-memory summaries.")
    refresh_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    refresh_parser.add_argument(
        "--scope",
        choices=["global", "project", "both"],
        default="both",
        help="Which summaries to rebuild (default: both).",
    )
    refresh_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Project working directory (defaults to cwd).",
    )
    refresh_parser.set_defaults(func=cmd_refresh)

    # --- transcripts ---
    transcripts_parser = subparsers.add_parser(
        "transcripts",
        help="Find sessions that ended without a session summary and catch them up.",
    )
    transcripts_parser.add_argument(
        "action",
        choices=["open", "digest", "skip"],
        help="open: list sessions without a summary; digest: print one transcript compactly; "
             "skip: mark one as not needing a summary.",
    )
    transcripts_parser.add_argument(
        "session_id",
        nargs="?",
        default=None,
        help="Session id (for digest and skip).",
    )
    transcripts_parser.add_argument(
        "--harness",
        choices=list(transcripts.HARNESSES),
        default=None,
        help="Agent harness (default: detected from the environment).",
    )
    transcripts_parser.add_argument(
        "--days",
        type=_nonnegative_int,
        default=transcripts.DEFAULT_DAYS,
        help=f"How far back open looks (default: {transcripts.DEFAULT_DAYS}).",
    )
    transcripts_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for open (default: text).",
    )
    transcripts_parser.add_argument(
        "--max-chars",
        dest="max_chars",
        type=_nonnegative_int,
        default=24000,
        help="Size limit for digest (default: 24000).",
    )
    transcripts_parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Digest the whole transcript, including parts a summary already covers.",
    )
    transcripts_parser.add_argument(
        "--reason",
        default=None,
        help="Why the session needs no summary (for skip).",
    )
    transcripts_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (required).",
    )
    transcripts_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Directory the sessions ran in (defaults to cwd).",
    )
    transcripts_parser.set_defaults(func=cmd_transcripts)

    args = parser.parse_args()
    args.func(args)
