# Pyro Kit Phase Map

## Phase 0: Ignition (Pre-Idea -> Idea)

**Gate G0: Idea Crystallized**
- One-sentence intent exists
- At least one idea thumbnail was selected
- Developer confirms readiness

**Skills**: /spark, /remix, /fascination

**State produced**: `.pyro/spark.md`
**State consumed**: `~/.pyro/fascination-index.md` (by /spark, /fascination)

---

## Phase 1: Exploration (Idea -> Developed Idea)

**Gate G1: Direction Locked**
- One direction chosen from multiple explored
- Rejected alternatives logged
- Key constraints identified

**Skills**: /explore, /narrow

**State produced**: `.pyro/explore.md`
**State consumed**: `.pyro/spark.md`

---

## Phase 2: Surface (Direction -> Converged Prototype)

**Gate G2: Surface Converged**
- Critical flows demonstrated
- Surface State Inventory completed
- Edge cases explored
- Decision log current

**Skills**: /surface

**State produced**: `.pyro/surface.md`
**State consumed**: `.pyro/explore.md`

---

## Phase 3: Contract (Converged Surface -> Frozen Specs)

**Gate G3: Contracts Frozen**
- API contracts versioned
- Invariants documented
- NFRs with measurable targets
- Architecture reviewed

**Skills**: /contract

**State produced**: `.pyro/contract.md`
**State consumed**: `.pyro/surface.md`

---

## Phase 4: Build (Contracts -> Working Software)

**Gate G4: Slice Complete** (per slice)
**Gate G5: Release Ready** (all slices)
- Each slice makes one surface flow real E2E
- Progressive hardening replaces mocks
- Acceptance tests pass against surface baseline

**Skills**: /build

**State consumed**: `.pyro/contract.md`

---

## Phase 5: Momentum (Anti-Abandonment Intervention)

**Gate G6: Momentum Check**
- Fires on signals: commit frequency decline, stale branches, new repos created
- Requires explicit push/pivot/shelve decision
- Can fire regardless of current phase

**Skills**: /pulse, /reframe, /scope, /decide

**State produced**: `.pyro/pulse-log.md` (append), `.pyro/scope.md`, `.pyro/decide.md`
**State consumed**: `.pyro/state.md`, `.pyro/spark.md` (by /scope), `.pyro/contract.md` (by /reframe, /scope, /decide), `.pyro/pulse-log.md` (by /decide, appended by /reframe), `.pyro/surface.md` (by /reframe, /decide), git history

---

## Phase 6: Lifecycle (Completion or Composting)

**Gate G7: Lifecycle Complete**
- Project has exactly one terminal state: shipped, shelved, or composted
- No undead projects

**Skills**: /autopsy, /ship, /revive, /patterns

**State produced**: `~/.pyro/autopsies/{name}.md`, `~/.pyro/fascination-index.md` updates, `.pyro/harvest.md` (from /revive organ harvest)
**State consumed**: `.pyro/contract.md`, `.pyro/surface.md` (by /ship); code, commits, README, `.pyro/state.md`, `.pyro/spark.md` (by /revive); `~/.pyro/fascination-index.md`, `~/.pyro/project-registry.yaml`, `~/.pyro/autopsies/` (by /patterns); full project state + git history (by /autopsy)
