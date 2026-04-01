"""CLI entry points for codies-memory."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from codies_memory.vault import (
    init_global_vault,
    init_project_vault,
    validate_vault,
    resolve_global_vault,
    resolve_project_vault,
)
from codies_memory.boot import assemble_boot
from codies_memory.inbox import capture, pending_review
from codies_memory.records import create_record, read_record, list_records
from codies_memory.promotion import promote_within_project, promote_to_global
from codies_memory.profile import load_profile, get_write_gate_bias


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_agent(args: argparse.Namespace) -> str:
    """Resolve agent name from --agent flag or CODIES_MEMORY_AGENT env var."""
    agent = getattr(args, "agent", None) or os.environ.get("CODIES_MEMORY_AGENT")
    if not agent:
        print("Error: --agent flag or CODIES_MEMORY_AGENT env var required.", file=sys.stderr)
        sys.exit(1)
    return agent


def _resolve_project_vault(args: argparse.Namespace) -> tuple[Path, Path]:
    """Resolve global and project vault paths from args.

    Returns (global_vault, project_vault).
    Exits with error if no project vault is found.
    """
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)
    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)
    if project_vault is None:
        print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
        sys.exit(1)
    return global_vault, project_vault


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
        global_vault = resolve_global_vault(agent)
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
        sys.exit(1)


def cmd_boot(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)

    if project_vault is None:
        print("Warning: no project vault found; global-only boot.", file=sys.stderr)

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


def cmd_capture(args: argparse.Namespace) -> None:
    global_vault, project_vault = _resolve_project_vault(args)

    gate = args.gate
    if gate is None:
        profile = load_profile(global_vault, project_vault)
        gate = get_write_gate_bias(profile)

    record_path = capture(
        vault=project_vault,
        content=args.content,
        source=args.source,
        gate=gate,
    )

    record = read_record(record_path)
    print(record["frontmatter"]["id"])


def cmd_create(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    # Global-only types: auto-route to global scope
    GLOBAL_ONLY_TYPES = {"reflection", "dream", "skill", "playbook", "identity"}
    if args.type in GLOBAL_ONLY_TYPES and args.scope == "project":
        args.scope = "global"

    # Read body from --body or --body-file
    body = getattr(args, "body", None)
    body_file = getattr(args, "body_file", None)
    if body_file:
        body = Path(body_file).read_text(encoding="utf-8")
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
        extra[key] = value

    # Resolve vault
    if scope == "global":
        vault = global_vault
    else:
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
        if vault is None:
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)

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
    print(record["frontmatter"]["id"])


def cmd_promote(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    source_path = Path(args.source).resolve()
    if not source_path.exists():
        print(f"Error: source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

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
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)
    scope = args.scope

    if scope == "global":
        vault = global_vault
    else:
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
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
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)

    if project_vault is None:
        print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
        sys.exit(1)

    result = pending_review(project_vault)
    active = result.get("active", [])
    aging = result.get("aging", [])
    stale = result.get("stale", [])

    print(f"Active: {len(active)}  Aging: {len(aging)}  Stale: {len(stale)}")

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


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="codies-memory",
        description="File-based two-tier memory system for AI agents.",
    )
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
        help="Agent name (or set CODIES_MEMORY_AGENT).",
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
        help="Agent name (or set CODIES_MEMORY_AGENT).",
    )
    boot_parser.add_argument(
        "--branch",
        default="main",
        help="Branch name (default: main).",
    )
    boot_parser.add_argument(
        "--budget",
        type=int,
        default=4000,
        help="Token budget (default: 4000).",
    )
    boot_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Project working directory (default: cwd).",
    )
    boot_parser.set_defaults(func=cmd_boot)

    # --- status ---
    status_parser = subparsers.add_parser("status", help="Show inbox/review status.")
    status_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (or set CODIES_MEMORY_AGENT).",
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
        "--agent",
        default=None,
        help="Agent name (or set CODIES_MEMORY_AGENT).",
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
        choices=["thread", "lesson", "decision", "session", "reflection", "dream"],
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
        help="Record body text.",
    )
    body_group.add_argument(
        "--body-file",
        dest="body_file",
        default=None,
        help="Path to file containing record body.",
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
        "--agent",
        default=None,
        help="Agent name (or set CODIES_MEMORY_AGENT).",
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
        help="Record type (inbox, threads, lessons, decisions, sessions, reflections, dreams).",
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
        help="Agent name (or set CODIES_MEMORY_AGENT).",
    )
    list_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory (defaults to cwd).",
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
    promote_parser.add_argument(
        "--agent",
        default=None,
        help="Agent name (or set CODIES_MEMORY_AGENT).",
    )
    promote_parser.add_argument(
        "--working-dir",
        dest="working_dir",
        default=None,
        help="Working directory (defaults to cwd).",
    )
    promote_parser.set_defaults(func=cmd_promote)

    args = parser.parse_args()
    args.func(args)
