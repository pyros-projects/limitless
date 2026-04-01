#!/usr/bin/env bash
set -euo pipefail

# pyro-init.sh — Initialize ~/.pyro/ global state and .pyro/ project state
# Usage: pyro-init.sh [project-name]

PYRO_GLOBAL="$HOME/.pyro"
PYRO_DIR=".pyro"

# Derive project name from argument or current directory basename
PROJECT_NAME="${1:-$(basename "$(pwd)")}"
TODAY="$(date +%Y-%m-%d)"
ABS_CWD="$(pwd)"

# ---------------------------------------------------------------------------
# Global state initialization (~/.pyro/)
# ---------------------------------------------------------------------------

init_global() {
  if [ ! -d "$PYRO_GLOBAL" ]; then
    echo "[pyro] Creating global state at $PYRO_GLOBAL/"
    mkdir -p "$PYRO_GLOBAL"
  else
    echo "[pyro] Global state exists at $PYRO_GLOBAL/"
  fi

  # config.yaml
  if [ ! -f "$PYRO_GLOBAL/config.yaml" ]; then
    cat > "$PYRO_GLOBAL/config.yaml" << 'GCFG'
dormancy_threshold_days: 5
pulse_auto_suggest: true
fascination_intensity_decay: true
default_start_phase: 0
GCFG
    echo "[pyro] Created $PYRO_GLOBAL/config.yaml"
  fi

  # project-registry.yaml
  if [ ! -f "$PYRO_GLOBAL/project-registry.yaml" ]; then
    cat > "$PYRO_GLOBAL/project-registry.yaml" << 'GREG'
projects: []
GREG
    echo "[pyro] Created $PYRO_GLOBAL/project-registry.yaml"
  fi

  # fascination-index.md
  if [ ! -f "$PYRO_GLOBAL/fascination-index.md" ]; then
    cat > "$PYRO_GLOBAL/fascination-index.md" << 'GFASC'
---
entries: []
---

# Fascination Index

Cross-project fascination registry. Updated by /autopsy, read by /spark.
GFASC
    echo "[pyro] Created $PYRO_GLOBAL/fascination-index.md"
  fi

  # autopsies/
  if [ ! -d "$PYRO_GLOBAL/autopsies" ]; then
    mkdir -p "$PYRO_GLOBAL/autopsies"
    touch "$PYRO_GLOBAL/autopsies/.gitkeep"
    echo "[pyro] Created $PYRO_GLOBAL/autopsies/"
  fi

  # patterns/
  if [ ! -d "$PYRO_GLOBAL/patterns" ]; then
    mkdir -p "$PYRO_GLOBAL/patterns"
    touch "$PYRO_GLOBAL/patterns/.gitkeep"
    echo "[pyro] Created $PYRO_GLOBAL/patterns/"
  fi
}

# ---------------------------------------------------------------------------
# Register current project in ~/.pyro/project-registry.yaml
# ---------------------------------------------------------------------------

register_project() {
  local registry="$PYRO_GLOBAL/project-registry.yaml"

  # Check if this project path is already registered
  if grep -qF "path: $ABS_CWD" "$registry" 2>/dev/null; then
    echo "[pyro] Project already registered in global registry."
    return
  fi

  local entry
  entry="  - path: ${ABS_CWD}
    name: ${PROJECT_NAME}
    status: active
    phase: 0
    last_activity: ${TODAY}
    spark_date: \"\"
    fascinations: []"

  # Handle empty list case: projects: []
  if grep -q 'projects: \[\]' "$registry" 2>/dev/null; then
    # Replace empty list with populated list
    {
      echo "projects:"
      echo "$entry"
    } > "$registry"
  else
    # Append after existing entries
    printf '\n%s\n' "$entry" >> "$registry"
  fi

  echo "[pyro] Registered project '$PROJECT_NAME' in global registry."
}

# --- Run global init first ---
init_global
register_project

# ---------------------------------------------------------------------------
# Project-local state initialization (.pyro/)
# ---------------------------------------------------------------------------

# Idempotency check — repair missing artifacts if .pyro/ exists
if [ -d "$PYRO_DIR" ]; then
  echo "[pyro] .pyro/ already exists in $(pwd). Checking for missing artifacts..."
  REPAIRED=0

  if [ ! -f "$PYRO_DIR/state.md" ]; then
    cat > "$PYRO_DIR/state.md" << EOF
---
project: ${PROJECT_NAME}
phase: 0
status: active
soul: ""
original_spark: ""
last_skill: none
last_activity: ${TODAY}
momentum: steady
gate_history: []
pulse_count: 0
---

## Current State
Project initialized. No work started yet.

## Decisions Made
- ${TODAY}: Project tracking initialized with Pyro Kit
EOF
    echo "[pyro] Repaired: created missing $PYRO_DIR/state.md"
    REPAIRED=$((REPAIRED + 1))
  fi

  if [ ! -f "$PYRO_DIR/config.yaml" ]; then
    cat > "$PYRO_DIR/config.yaml" << 'PCFG'
# Project-local Pyro config overrides
PCFG
    echo "[pyro] Repaired: created missing $PYRO_DIR/config.yaml"
    REPAIRED=$((REPAIRED + 1))
  fi

  if [ ! -f "$PYRO_DIR/pulse-log.md" ]; then
    cat > "$PYRO_DIR/pulse-log.md" << 'EOF'
# Pulse Log

Append-only log of /pulse check-ins.
EOF
    echo "[pyro] Repaired: created missing $PYRO_DIR/pulse-log.md"
    REPAIRED=$((REPAIRED + 1))
  fi

  if [ ! -d "$PYRO_DIR/session-notes" ]; then
    mkdir -p "$PYRO_DIR/session-notes"
    touch "$PYRO_DIR/session-notes/.gitkeep"
    echo "[pyro] Repaired: created missing $PYRO_DIR/session-notes/"
    REPAIRED=$((REPAIRED + 1))
  fi

  if [ "$REPAIRED" -eq 0 ]; then
    echo "[pyro] All artifacts present. Nothing to repair."
  else
    echo "[pyro] Repaired ${REPAIRED} missing artifact(s)."
  fi
  exit 0
fi

echo "[pyro] Initializing project: $PROJECT_NAME"

# Create .pyro/ directory
mkdir -p "$PYRO_DIR"
echo "[pyro] Created $PYRO_DIR/"

# Create state.md
cat > "$PYRO_DIR/state.md" << EOF
---
project: ${PROJECT_NAME}
phase: 0
status: active
soul: ""
original_spark: ""
last_skill: none
last_activity: ${TODAY}
momentum: steady
gate_history: []
pulse_count: 0
---

## Current State
Project initialized. No work started yet.

## Decisions Made
- ${TODAY}: Project tracking initialized with Pyro Kit
EOF
echo "[pyro] Created $PYRO_DIR/state.md"

# Create config.yaml
cat > "$PYRO_DIR/config.yaml" << 'PCFG'
# Project-local Pyro config overrides
PCFG
echo "[pyro] Created $PYRO_DIR/config.yaml"

# Create pulse-log.md
cat > "$PYRO_DIR/pulse-log.md" << 'EOF'
# Pulse Log

Append-only log of /pulse check-ins.
EOF
echo "[pyro] Created $PYRO_DIR/pulse-log.md"

# Create session-notes/ with .gitkeep
mkdir -p "$PYRO_DIR/session-notes"
touch "$PYRO_DIR/session-notes/.gitkeep"
echo "[pyro] Created $PYRO_DIR/session-notes/"

echo "[pyro] Done. Project '$PROJECT_NAME' is ready."
