#!/usr/bin/env bash
set -euo pipefail

# smoke-test.sh — Verify Pyro Kit plugin installation is structurally correct
# Usage: smoke-test.sh [plugin-root]

PLUGIN_ROOT="$(cd "${1:-$(dirname "$0")/..}" && pwd)"
PASS_COUNT=0
FAIL_COUNT=0

pass() { echo "  PASS: $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "  FAIL: $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

check_exists() {
  if [ -e "$PLUGIN_ROOT/$1" ]; then pass "$1 exists"; else fail "$1 missing"; fi
}

check_executable() {
  if [ -x "$PLUGIN_ROOT/$1" ]; then pass "$1 is executable"; else fail "$1 not executable"; fi
}

check_json() {
  local f="$PLUGIN_ROOT/$1"
  if command -v jq >/dev/null 2>&1; then
    if jq empty "$f" 2>/dev/null; then pass "$1 valid JSON"; else fail "$1 invalid JSON"; fi
  elif command -v python3 >/dev/null 2>&1; then
    if python3 -m json.tool "$f" >/dev/null 2>&1; then pass "$1 valid JSON"; else fail "$1 invalid JSON"; fi
  else
    fail "$1 JSON check skipped (no jq or python3)"
  fi
}

echo "=== Pyro Kit Smoke Test ==="
echo "Plugin root: $PLUGIN_ROOT"
echo ""

echo "-- File existence --"
check_exists ".claude-plugin/plugin.json"
check_exists "skills/spark/SKILL.md"
check_exists "skills/pulse/SKILL.md"
check_exists "skills/autopsy/SKILL.md"
check_exists "skills/pyro/SKILL.md"
check_exists "skills/pyro/reference/skill-catalog.md"
check_exists "skills/pyro/reference/phase-map.md"
check_exists "agents/excavator.md"
check_exists "hooks/hooks.json"
check_exists "scripts/pyro-init.sh"
check_exists "scripts/session-init.sh"
check_exists "scripts/git-activity.sh"
check_exists "docs/schemas/state-files.md"
check_exists "docs/skill-authoring.md"
check_exists "docs/context-budget-audit.md"

# Phase 2 skills
check_exists "skills/remix/SKILL.md"
check_exists "skills/fascination/SKILL.md"
check_exists "skills/explore/SKILL.md"
check_exists "skills/explore/reference/direction-format.md"
check_exists "skills/explore/reference/explore-output-format.md"

echo ""
echo "-- Script executability --"
check_executable "scripts/pyro-init.sh"
check_executable "scripts/session-init.sh"
check_executable "scripts/git-activity.sh"

echo ""
echo "-- JSON validity --"
check_json ".claude-plugin/plugin.json"
check_json "hooks/hooks.json"

echo ""
echo "-- Fresh init test --"
TMPDIR_TEST=$(mktemp -d)
trap 'rm -rf "$TMPDIR_TEST"' EXIT
(
  cd "$TMPDIR_TEST"
  git init -q .
  bash "$PLUGIN_ROOT/scripts/pyro-init.sh" test-project >/dev/null 2>&1
)
if [ -f "$TMPDIR_TEST/.pyro/state.md" ]; then pass "pyro-init creates state.md"; else fail "pyro-init missing state.md"; fi
if [ -f "$TMPDIR_TEST/.pyro/config.yaml" ]; then pass "pyro-init creates config.yaml"; else fail "pyro-init missing config.yaml"; fi
if [ -f "$TMPDIR_TEST/.pyro/pulse-log.md" ]; then pass "pyro-init creates pulse-log.md"; else fail "pyro-init missing pulse-log.md"; fi
if grep -q "project:" "$TMPDIR_TEST/.pyro/state.md" 2>/dev/null && \
   grep -q "phase:" "$TMPDIR_TEST/.pyro/state.md" 2>/dev/null && \
   grep -q "momentum:" "$TMPDIR_TEST/.pyro/state.md" 2>/dev/null; then
  pass "state.md has expected frontmatter fields"
else
  fail "state.md missing expected frontmatter fields"
fi

echo ""
echo "-- Catalog consistency --"
SKILL_COUNT=$(grep -c '^### /' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md" 2>/dev/null || echo 0)
if [ "$SKILL_COUNT" -ge 15 ] && [ "$SKILL_COUNT" -le 20 ]; then
  pass "Skill catalog has $SKILL_COUNT entries (expected 15-20)"
else
  fail "Skill catalog has $SKILL_COUNT entries (expected 15-20)"
fi

echo ""
echo "-- Phase 2: Shared infrastructure --"
# IGN-04: Domain lenses must NOT be duplicated into remix or explore
if [ ! -f "$PLUGIN_ROOT/skills/remix/reference/domain-lenses.md" ] && \
   [ ! -f "$PLUGIN_ROOT/skills/explore/reference/domain-lenses.md" ]; then
  pass "Domain lenses not duplicated (shared infrastructure)"
else
  fail "Domain lenses duplicated -- must use shared reference from spark/"
fi

# EXP-05: explore.md schema must be documented
if grep -q "explore.md" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "explore.md schema documented in state-files.md"
else
  fail "explore.md schema missing from state-files.md"
fi

# /fascination must be read-only (no Write in allowed-tools)
if ! grep "allowed-tools" "$PLUGIN_ROOT/skills/fascination/SKILL.md" | grep -q "Write"; then
  pass "/fascination is read-only (no Write tool)"
else
  fail "/fascination has Write tool -- should be read-only"
fi

echo ""
echo "-- Phase 3: Direction Lock + SFD Wrapper --"
# EXP-04: /narrow skill exists
check_exists "skills/narrow/SKILL.md"

# SRF-01: /surface skill exists
check_exists "skills/surface/SKILL.md"

# SRF-01: /surface reference material
check_exists "skills/surface/reference/surface-output-format.md"

# SRF-04: surface.md schema documented
if grep -q "surface.md" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "surface.md schema documented in state-files.md"
else
  fail "surface.md schema missing from state-files.md"
fi

# EXP-04: locked fields documented in explore.md schema
if grep -q "locked" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "locked fields documented in state-files.md"
else
  fail "locked fields missing from state-files.md"
fi

# SRF-03: Surface State Inventory documented
if grep -q "Surface State Inventory" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "Surface State Inventory documented in state-files.md"
else
  fail "Surface State Inventory missing from state-files.md"
fi

echo ""
echo "-- Phase 4: SFD Core Wrappers --"
# CTR-01: /contract skill exists
check_exists "skills/contract/SKILL.md"

# CTR-01: /contract reference material
check_exists "skills/contract/reference/contract-output-format.md"

# BLD-01: /build skill exists
check_exists "skills/build/SKILL.md"

# BLD-01: /build reference material
check_exists "skills/build/reference/slice-planning.md"

# CTR-03: contract.md schema documented
if grep -q "contract.md" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "contract.md schema documented in state-files.md"
else
  fail "contract.md schema missing from state-files.md"
fi

# Catalog consistency: /contract and /build marked [Available]
if grep -q '/contract \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/contract marked [Available] in catalog"
else
  fail "/contract not marked [Available] in catalog"
fi

if grep -q '/build \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/build marked [Available] in catalog"
else
  fail "/build not marked [Available] in catalog"
fi

echo ""
echo "-- Phase 5: Momentum --"

# Skill existence
check_exists "skills/reframe/SKILL.md"
check_exists "skills/scope/SKILL.md"
check_exists "skills/decide/SKILL.md"

# Schema documentation
if grep -q "scope.md" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "scope.md schema documented in state-files.md"
else
  fail "scope.md schema missing from state-files.md"
fi

if grep -q "decide.md" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "decide.md schema documented in state-files.md"
else
  fail "decide.md schema missing from state-files.md"
fi

# Catalog accuracy
if grep -q '/reframe \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/reframe marked [Available] in catalog"
else
  fail "/reframe not marked [Available] in catalog"
fi

if grep -q '/scope \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/scope marked [Available] in catalog"
else
  fail "/scope not marked [Available] in catalog"
fi

if grep -q '/decide \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/decide marked [Available] in catalog"
else
  fail "/decide not marked [Available] in catalog"
fi

# Shared infrastructure (IGN-04) -- domain-lenses NOT duplicated
if [ -d "$PLUGIN_ROOT/skills/reframe/reference" ] && [ -f "$PLUGIN_ROOT/skills/reframe/reference/domain-lenses.md" ]; then
  fail "domain-lenses.md duplicated in reframe/ (must use shared from spark/reference/)"
else
  pass "domain-lenses.md not duplicated in reframe/"
fi

# /spark --smaller mode
if grep -q "smaller" "$PLUGIN_ROOT/skills/spark/SKILL.md"; then
  pass "/spark --smaller mode present"
else
  fail "/spark --smaller mode missing from spark SKILL.md"
fi

# /pulse suggests /decide
if grep -q "/decide" "$PLUGIN_ROOT/skills/pulse/SKILL.md"; then
  pass "/pulse suggests /decide in closing"
else
  fail "/pulse does not suggest /decide in closing"
fi

echo ""
echo "-- Phase 6: Lifecycle --"

# Skill existence
check_exists "skills/ship/SKILL.md"
check_exists "skills/revive/SKILL.md"
check_exists "skills/revive/reference/revival-options.md"
check_exists "skills/patterns/SKILL.md"

# Schema documentation
if grep -q "harvest.md" "$PLUGIN_ROOT/docs/schemas/state-files.md"; then
  pass "harvest.md schema documented in state-files.md"
else
  fail "harvest.md schema missing from state-files.md"
fi

# Catalog accuracy
if grep -q '/ship \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/ship marked [Available] in catalog"
else
  fail "/ship not marked [Available] in catalog"
fi

if grep -q '/revive \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/revive marked [Available] in catalog"
else
  fail "/revive not marked [Available] in catalog"
fi

if grep -q '/patterns \[Available\]' "$PLUGIN_ROOT/skills/pyro/reference/skill-catalog.md"; then
  pass "/patterns marked [Available] in catalog"
else
  fail "/patterns not marked [Available] in catalog"
fi

# Read-only enforcement (LIF-01, LIF-03)
if ! grep "allowed-tools" "$PLUGIN_ROOT/skills/ship/SKILL.md" | grep -q "Write"; then
  pass "/ship is read-only (no Write tool)"
else
  fail "/ship has Write tool -- should be read-only"
fi

if ! grep "allowed-tools" "$PLUGIN_ROOT/skills/patterns/SKILL.md" | grep -q "Write"; then
  pass "/patterns is read-only (no Write tool)"
else
  fail "/patterns has Write tool -- should be read-only"
fi

# /revive any-repo compatibility
if grep -q "NO_PROJECT_STATE" "$PLUGIN_ROOT/skills/revive/SKILL.md"; then
  pass "/revive handles missing .pyro/ state"
else
  fail "/revive missing NO_PROJECT_STATE fallback"
fi

echo ""
echo "=== Smoke test complete: $PASS_COUNT passed, $FAIL_COUNT failed ==="
exit "$FAIL_COUNT"
