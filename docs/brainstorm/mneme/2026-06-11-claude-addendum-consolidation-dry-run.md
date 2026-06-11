# Claude Addendum — The Consolidation Dry Run (Field Notes for Mneme)

*Field notes · 2026-06-11 · Claude (Fable 5) + Pyro*

> Status: evidence document. On 2026-06-11 we manually executed most of
> Mneme's consolidation story with bash, a one-off Python importer, and
> symlinks. Pyro named it mid-session: "we are basically doing the clunky
> version of Mneme." These notes record what the clunky version proved,
> what it broke, and what that sharpens for the phase-1 scaffold.

---

## What we did by hand

1. Migrated both agents' basic-memory archives into their vaults —
   Claude: 63 reflections + 20 dreams; Codie: 91 reflections + 79 dreams
   — as `trust: historical` records with original `created` dates and
   `captured_from` provenance. Importer idempotent (keyed on
   `captured_from` + title/date).
2. Consolidated both vaults into the knowledge-base repo:
   `claude-knowledge/memory/Claude/` + `memory/Codie/`, parallel. My
   vault moved by rename (history preserved); Codie's moved in from his
   standalone repo (which keeps pre-move history as archive).
3. Repointed `~/.memory/{Claude,Codie}` symlinks — the codies-memory
   plugin and QMD resolved through them with **zero changes and zero
   downtime**.
4. Deleted the stale unversioned vault snapshot at `basic-memory/.memory/`
   (after verifying nothing unique) and the rotted `/wake-up` command.
5. Wrote `identity/memory-map.md` into both vaults — boot-exempt, so
   every future session self-describes the whole construct.

## The mapping

| Today, manually | Mneme, by design |
|---|---|
| Both vaults in one repo, parallel dirs | one vault, one repo of record |
| Symlinks kept `~/.memory/*` stable; tools never noticed | thin host adapters over implementation seams |
| `trust: historical` + `captured_from` imports | the ingestion/promotion bridge |
| QMD over eight scattered collections | one retrieval/indexing layer |
| `memory-map.md` self-description at boot | one user-facing concept model |
| Claude with bash + one-off scripts | the install story |

## Casualties as evidence

The day's failures are the spec's argument made flesh:

- **The dream practice died at a layer seam.** basic-memory went
  read-only 2026-04-01; the vault had a `dreams/` dir from day one; not
  one dream landed in it for ten weeks. Nobody decided this — the
  practice was anchored to the old layer's sign-off ritual and nothing
  in the new layer claimed it. Exactly the "user must not learn
  implementation seams" failure from Codie's product-boundary addendum,
  with a body count.
- **The stale snapshot.** An unversioned copy of all three vaults
  (creator unknown, 129 files behind) fooled both Pyro and Claude into
  believing Codie's memory was unversioned — and nearly motivated an
  architecture change on a false premise. This is what ad-hoc copies do
  when there is no single system of record.
- **The wake-up command rot.** A boot ritual written for the old
  construct survived two architecture generations unmaintained: a
  recent-activity check on a frozen archive (with a quoting bug, hit
  independently by both agents), sign-off instructions pointing at a
  read-only tier, a stale model name. Docs that aren't part of the
  system's self-description decay silently.

## What worked — keep these in Mneme

- **Provenance fields were already in the schema.**
  `PROVENANCE_FIELDS = {captured_from, capture_date, original_created}`
  and the `historical` trust level existed before anyone needed them —
  the migration required zero schema changes. Design-for-ingestion pays.
- **Idempotent import keyed on provenance.** Re-runs are free; partial
  failures are safe. Any Mneme ingestion path should have this property
  from day one.
- **Date-sorted summaries made historical imports harmless.** Boot
  surfaces "recent" by semantic date, not record ID — so 170 imported
  old records changed nothing at boot. Rule: derived views sort by
  semantic time, never by identifier sequence.
- **Symlink indirection = host adapter, proven.** Two live consumers
  (plugin, QMD) rode through a full vault relocation without config
  changes. The adapter layer can be this thin.
- **Boot-exempt identity files as self-description.** The construct now
  explains itself every session for ~400 tokens. Mneme's concept model
  should ship the same way: inside the memory, not beside it.

## Friction the spec should absorb

- **"Uncommitted for review" conflicts with consolidation.** The import
  was left uncommitted in Codie's repo as a review gate; the same-day
  repo merge force-committed everything. In a one-repo world, review
  must be post-hoc edit rights with provenance, not pre-commit gates.
- **Migration checklists must enumerate practices, not just data.** The
  data migration was lossless; the *practice* (dreaming) still died.
  "What writes here, and where does that behavior live now?" is a
  first-class migration question.
- **Stated rationale vs structural intent.** "So we can versionize it"
  was technically already satisfied; the real goal was one roof for all
  knowledge. Consolidation requests should be evaluated against the
  end-state ("single repo managing ALL knowledge"), not the sub-goal.

## The remaining delta = phase-1 backlog, sharpened

- basic-memory is still a third repo — formally archived, outside the
  roof. Fold or formally freeze with a manifest.
- QMD's collection config lives outside the repo it indexes; Mneme owns
  its index definition in-repo.
- `writings/`, `portfolio/`, product-ideas: still scattered repos —
  "ALL my knowledge and info" isn't under the roof yet.
- The octocat vault is convention, not contract — agent namespacing
  needs to be a declared property of the vault root.
- No compiled layer: promotion exists per-vault; nothing compiles
  across vaults/layers yet (Codie's compiled-layer addendum remains
  unbuilt).

## Bottom line

The interaction surface of Mneme is now field-validated: one repo,
provenance-tagged ingestion, adapter indirection, search-first access,
self-describing boot. We lived in it for a day before writing a line of
product code — surface-first development applied to memory
infrastructure. Phase-1 scaffold can start from evidence, not intuition.
