#!/usr/bin/env bash
set -euo pipefail

# Pyro Kit SessionStart Hook
# Injects project context and detects dormancy at session start.
# Output: JSON with additionalContext field, or nothing (silent exit).

STATE_FILE=".pyro/state.md"

# 1. CHECK: Does .pyro/state.md exist?
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# 2. READ .pyro/state.md — extract YAML frontmatter fields
# Frontmatter is between the first two "---" lines.
in_frontmatter=false
frontmatter=""
while IFS= read -r line; do
  if [[ "$line" == "---" ]]; then
    if $in_frontmatter; then
      break
    else
      in_frontmatter=true
      continue
    fi
  fi
  if $in_frontmatter; then
    frontmatter+="$line"$'\n'
  fi
done < "$STATE_FILE"

# Parse simple "key: value" fields from frontmatter
extract_field() {
  local field="$1"
  printf '%s' "$frontmatter" | sed -n "s/^${field}:[[:space:]]*//p" | head -1 | sed 's/[[:space:]]*$//'
}

project=$(extract_field "project")
phase=$(extract_field "phase")
status=$(extract_field "status")
last_activity=$(extract_field "last_activity")
momentum=$(extract_field "momentum")
last_skill=$(extract_field "last_skill")

# Bail if we couldn't read essential fields
if [[ -z "$project" || -z "$last_activity" ]]; then
  echo "⚠ Pyro: Could not parse .pyro/state.md — run '/pyro init' to repair" >&2
  exit 0
fi

# 3. COMPUTE dormancy
# Read threshold from ~/.pyro/config.yaml, default to 5
dormancy_threshold=5
config_file="$HOME/.pyro/config.yaml"
if [[ -f "$config_file" ]]; then
  threshold_val=$(sed -n 's/^dormancy_threshold_days:[[:space:]]*//p' "$config_file" | head -1 | sed 's/[[:space:]]*$//')
  if [[ -n "$threshold_val" && "$threshold_val" =~ ^[0-9]+$ ]]; then
    dormancy_threshold="$threshold_val"
  fi
fi

# Compute days since last activity
today_epoch=$(date +%s)
# Support both GNU and BSD date
if date -d "2000-01-01" +%s >/dev/null 2>&1; then
  # GNU date
  last_epoch=$(date -d "$last_activity" +%s 2>/dev/null || echo "")
else
  # BSD date (macOS)
  last_epoch=$(date -j -f "%Y-%m-%d" "$last_activity" +%s 2>/dev/null || echo "")
fi

days_inactive=0
if [[ -n "$last_epoch" ]]; then
  days_inactive=$(( (today_epoch - last_epoch) / 86400 ))
  # Clamp to 0 if negative (future date)
  if (( days_inactive < 0 )); then
    days_inactive=0
  fi
fi

# 4. BUILD context message
context="Pyro Kit: Project '${project}', Phase ${phase:-unknown}, status ${status:-unknown}, momentum ${momentum:-unknown}. Last skill: ${last_skill:-none}, last active ${last_activity}."

if (( days_inactive > dormancy_threshold )); then
  context+=" Warning: Project inactive for ${days_inactive} days. Consider running /pulse for a momentum check."
fi

# 5. CHECK cross-project dormancy
registry_file="$HOME/.pyro/project-registry.yaml"
if [[ -f "$registry_file" ]]; then
  # Parse project-registry.yaml: look for entries with status: active
  # Format written by pyro-init.sh:
  #   - path: /some/path
  #     name: ProjectName
  #     status: active
  #     last_activity: 2025-01-01
  current_name=""
  current_path=""
  current_status=""
  current_last=""

  # Helper: emit previous entry if it was dormant
  _emit_if_dormant() {
    if [[ -n "$current_name" && "$current_status" == "active" && -n "$current_last" ]]; then
      # Match by path (precise) or name (fallback) to skip current project
      local abs_cwd
      abs_cwd="$(pwd)"
      if [[ "$current_path" == "$abs_cwd" || "$current_name" == "$project" ]]; then
        return
      fi
      local entry_epoch=""
      if date -d "2000-01-01" +%s >/dev/null 2>&1; then
        entry_epoch=$(date -d "$current_last" +%s 2>/dev/null || echo "")
      else
        entry_epoch=$(date -j -f "%Y-%m-%d" "$current_last" +%s 2>/dev/null || echo "")
      fi
      if [[ -n "$entry_epoch" ]]; then
        local entry_days=$(( (today_epoch - entry_epoch) / 86400 ))
        if (( entry_days > dormancy_threshold )); then
          context+=" Also dormant: ${current_name} (${entry_days} days)."
        fi
      fi
    fi
  }

  while IFS= read -r line; do
    # Strip leading whitespace for matching
    trimmed="${line#"${line%%[![:space:]]*}"}"

    # Entry delimiter: "- path:" (first field written by pyro-init.sh)
    if [[ "$trimmed" =~ ^-[[:space:]]*path:[[:space:]]*(.*) ]]; then
      # Emit previous entry before starting a new one
      _emit_if_dormant
      current_path="${BASH_REMATCH[1]}"
      current_path="${current_path#"${current_path%%[![:space:]]*}"}"
      current_name=""
      current_status=""
      current_last=""
    elif [[ "$trimmed" =~ ^name:[[:space:]]*(.*) ]]; then
      current_name="${BASH_REMATCH[1]}"
      current_name="${current_name#"${current_name%%[![:space:]]*}"}"
    elif [[ "$trimmed" =~ ^status:[[:space:]]*(.*) ]]; then
      current_status="${BASH_REMATCH[1]}"
      current_status="${current_status#"${current_status%%[![:space:]]*}"}"
    elif [[ "$trimmed" =~ ^last_activity:[[:space:]]*(.*) ]]; then
      current_last="${BASH_REMATCH[1]}"
      current_last="${current_last#"${current_last%%[![:space:]]*}"}"
    fi
  done < "$registry_file"

  # Process the last entry
  _emit_if_dormant
fi

# 6. OUTPUT JSON to stdout
# Escape backslashes, double quotes, and newlines for valid JSON
escaped_context=$(printf '%s' "$context" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' ')
printf '{"additionalContext":"%s"}\n' "$escaped_context"
