#!/usr/bin/env bash
set -euo pipefail

# git-activity.sh — Structured git activity metrics for /pulse momentum dashboard
# Usage: git-activity.sh [window_days]

WINDOW_DAYS="${1:-30}"
# Validate WINDOW_DAYS is a positive integer; default to 30 if not
if ! [[ "$WINDOW_DAYS" =~ ^[1-9][0-9]*$ ]]; then
  WINDOW_DAYS=30
fi
TODAY="$(date +%Y-%m-%d)"

# --- Validate environment ---

if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  cat <<EOF
=== GIT_ACTIVITY_REPORT ===
generated: ${TODAY}

=== OVERVIEW ===
repo_root: $(pwd)
total_commits: 0
days_since_last_commit: n/a
first_commit_date: n/a
last_commit_date: n/a
not_a_git_repo: true

=== COMMIT_FREQUENCY ===
window_days: ${WINDOW_DAYS}
total_in_window: 0
daily_average: 0.0

=== MESSAGE_SENTIMENT ===
create_count: 0
maintain_count: 0
other_count: 0
create_ratio: 0.00
maintain_ratio: 0.00
first_half_create_ratio: 0.00
second_half_create_ratio: 0.00
sentiment_trend: none

=== BRANCHES ===
active_branch: n/a
total_branches: 0

=== NEW_REPOS ===
new_repos_detected: 0
EOF
  exit 0
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"

# --- Check if repo has any commits ---

COMMIT_COUNT="$(git rev-list --count HEAD 2>/dev/null || echo 0)"

if [ "$COMMIT_COUNT" -eq 0 ]; then
  cat <<EOF
=== GIT_ACTIVITY_REPORT ===
generated: ${TODAY}

=== OVERVIEW ===
repo_root: ${REPO_ROOT}
total_commits: 0
days_since_last_commit: n/a
first_commit_date: n/a
last_commit_date: n/a

=== COMMIT_FREQUENCY ===
window_days: ${WINDOW_DAYS}
total_in_window: 0
daily_average: 0.0

=== MESSAGE_SENTIMENT ===
create_count: 0
maintain_count: 0
other_count: 0
create_ratio: 0.00
maintain_ratio: 0.00
first_half_create_ratio: 0.00
second_half_create_ratio: 0.00
sentiment_trend: none

=== BRANCHES ===
active_branch: $(git branch --show-current 2>/dev/null || echo "detached")
total_branches: $(git branch --list | wc -l | tr -d ' ')
no_remote: true

=== NEW_REPOS ===
new_repos_detected: 0
EOF
  exit 0
fi

# --- Overview ---

WINDOW_SINCE="$(date -d "${WINDOW_DAYS} days ago" +%Y-%m-%d 2>/dev/null \
  || date -v-"${WINDOW_DAYS}"d +%Y-%m-%d 2>/dev/null)"

FIRST_COMMIT_DATE="$(git log --reverse --format='%ad' --date=short | head -1)"
LAST_COMMIT_DATE="$(git log -1 --format='%ad' --date=short)"

LAST_COMMIT_EPOCH="$(git log -1 --format='%at')"
NOW_EPOCH="$(date +%s)"
DAYS_SINCE_LAST=$(( (NOW_EPOCH - LAST_COMMIT_EPOCH) / 86400 ))

HAS_REMOTE=true
if ! git remote 2>/dev/null | head -1 | grep -q .; then
  HAS_REMOTE=false
fi

cat <<EOF
=== GIT_ACTIVITY_REPORT ===
generated: ${TODAY}

=== OVERVIEW ===
repo_root: ${REPO_ROOT}
total_commits: ${COMMIT_COUNT}
days_since_last_commit: ${DAYS_SINCE_LAST}
first_commit_date: ${FIRST_COMMIT_DATE}
last_commit_date: ${LAST_COMMIT_DATE}
EOF
if [ "$HAS_REMOTE" = false ]; then
  echo "no_remote: true"
fi

# --- Commit Frequency ---

# Get commits within the window (efficient --since for large repos)
WINDOW_COMMITS="$(git log --since="${WINDOW_SINCE}" --format='%ad' --date=short 2>/dev/null)"
TOTAL_IN_WINDOW=0
if [ -n "$WINDOW_COMMITS" ]; then
  TOTAL_IN_WINDOW="$(echo "$WINDOW_COMMITS" | wc -l | tr -d ' ')"
fi

# Daily average (awk handles the float division)
DAILY_AVG="$(awk "BEGIN { printf \"%.1f\", ${TOTAL_IN_WINDOW} / ${WINDOW_DAYS} }")"

echo ""
echo "=== COMMIT_FREQUENCY ==="
echo "window_days: ${WINDOW_DAYS}"
echo "total_in_window: ${TOTAL_IN_WINDOW}"
echo "daily_average: ${DAILY_AVG}"

# Daily breakdown — build an associative array then print each day in the window
declare -A DAY_COUNTS
if [ -n "$WINDOW_COMMITS" ]; then
  while read -r count date_str; do
    DAY_COUNTS["$date_str"]="$count"
  done < <(echo "$WINDOW_COMMITS" | sort | uniq -c)
fi

# Iterate each day in the window
FIRST_HALF_COMMITS=0
SECOND_HALF_COMMITS=0
for (( i=0; i<WINDOW_DAYS; i++ )); do
  DAY="$(date -d "${i} days ago" +%Y-%m-%d 2>/dev/null \
    || date -v-"${i}"d +%Y-%m-%d 2>/dev/null)"
  DAY_COUNT="${DAY_COUNTS[$DAY]:-0}"
  echo "${DAY}: ${DAY_COUNT}"
  if (( i < WINDOW_DAYS / 2 )); then
    SECOND_HALF_COMMITS=$((SECOND_HALF_COMMITS + DAY_COUNT))
  else
    FIRST_HALF_COMMITS=$((FIRST_HALF_COMMITS + DAY_COUNT))
  fi
done

# Compute commit frequency trend
if [ "$TOTAL_IN_WINDOW" -lt 5 ]; then
  FREQ_TREND="insufficient_data"
elif awk "BEGIN { exit !(${SECOND_HALF_COMMITS} > ${FIRST_HALF_COMMITS} * 1.2) }"; then
  FREQ_TREND="increasing"
elif awk "BEGIN { exit !(${SECOND_HALF_COMMITS} < ${FIRST_HALF_COMMITS} * 0.8) }"; then
  FREQ_TREND="declining"
else
  FREQ_TREND="stable"
fi
echo "trend: ${FREQ_TREND}"

# --- Message Sentiment ---

# Gather first words of commit messages within the window
FIRST_WORDS=""
if [ "$TOTAL_IN_WINDOW" -gt 0 ]; then
  FIRST_WORDS="$(git log --since="${WINDOW_SINCE}" --format='%s' | \
    sed 's/^[[:space:]]*//' | \
    awk '{ w=tolower($1); sub(/\(.*\)?:$/, ":", w); sub(/:$/, "", w); print w }')"
fi

classify_word() {
  local word="$1"
  case "$word" in
    add|create|implement|new|initial|feat|introduce)
      echo "create"
      ;;
    fix|hotfix|patch|update|refactor|cleanup|clean|improve|adjust|correct|chore|docs|test|style|perf|ci|build)
      echo "maintain"
      ;;
    *)
      echo "other"
      ;;
  esac
}

CREATE_COUNT=0
MAINTAIN_COUNT=0
OTHER_COUNT=0

if [ -n "$FIRST_WORDS" ]; then
  while IFS= read -r word; do
    category="$(classify_word "$word")"
    case "$category" in
      create)   CREATE_COUNT=$((CREATE_COUNT + 1)) ;;
      maintain) MAINTAIN_COUNT=$((MAINTAIN_COUNT + 1)) ;;
      other)    OTHER_COUNT=$((OTHER_COUNT + 1)) ;;
    esac
  done <<< "$FIRST_WORDS"
fi

TOTAL_SENTIMENT=$((CREATE_COUNT + MAINTAIN_COUNT + OTHER_COUNT))
if [ "$TOTAL_SENTIMENT" -gt 0 ]; then
  CREATE_RATIO="$(awk "BEGIN { printf \"%.2f\", ${CREATE_COUNT} / ${TOTAL_SENTIMENT} }")"
  MAINTAIN_RATIO="$(awk "BEGIN { printf \"%.2f\", ${MAINTAIN_COUNT} / ${TOTAL_SENTIMENT} }")"
else
  CREATE_RATIO="0.00"
  MAINTAIN_RATIO="0.00"
fi

# Trend: split window into first half and second half
HALF_DAYS=$(( WINDOW_DAYS / 2 ))
HALF_SINCE="$(date -d "${HALF_DAYS} days ago" +%Y-%m-%d 2>/dev/null \
  || date -v-"${HALF_DAYS}"d +%Y-%m-%d 2>/dev/null)"

# Second half = most recent half (HALF_SINCE to now)
# First half = older half (WINDOW_SINCE to HALF_SINCE)
SECOND_HALF_WORDS=""
FIRST_HALF_WORDS=""
if [ "$TOTAL_IN_WINDOW" -gt 0 ]; then
  SECOND_HALF_WORDS="$(git log --since="${HALF_SINCE}" --format='%s' | \
    sed 's/^[[:space:]]*//' | awk '{ w=tolower($1); sub(/\(.*\)?:$/, ":", w); sub(/:$/, "", w); print w }')"
  FIRST_HALF_WORDS="$(git log --since="${WINDOW_SINCE}" --until="${HALF_SINCE}" --format='%s' | \
    sed 's/^[[:space:]]*//' | awk '{ w=tolower($1); sub(/\(.*\)?:$/, ":", w); sub(/:$/, "", w); print w }')"
fi

count_create() {
  local words="$1"
  local count=0
  if [ -z "$words" ]; then
    echo 0
    return
  fi
  while IFS= read -r w; do
    case "$w" in
      add|create|implement|new|initial|feat|introduce) count=$((count + 1)) ;;
      fix|hotfix|patch|update|refactor|cleanup|clean|improve|adjust|correct|chore|docs|test|style|perf|ci|build) ;;
    esac
  done <<< "$words"
  echo "$count"
}

count_total() {
  local words="$1"
  if [ -z "$words" ]; then
    echo 0
    return
  fi
  echo "$words" | wc -l | tr -d ' '
}

FH_CREATE="$(count_create "$FIRST_HALF_WORDS")"
FH_TOTAL="$(count_total "$FIRST_HALF_WORDS")"
SH_CREATE="$(count_create "$SECOND_HALF_WORDS")"
SH_TOTAL="$(count_total "$SECOND_HALF_WORDS")"

if [ "$FH_TOTAL" -gt 0 ]; then
  FH_RATIO="$(awk "BEGIN { printf \"%.2f\", ${FH_CREATE} / ${FH_TOTAL} }")"
else
  FH_RATIO="0.00"
fi
if [ "$SH_TOTAL" -gt 0 ]; then
  SH_RATIO="$(awk "BEGIN { printf \"%.2f\", ${SH_CREATE} / ${SH_TOTAL} }")"
else
  SH_RATIO="0.00"
fi

# Determine trend
TREND="stable"
if awk "BEGIN { exit !(${FH_RATIO} - ${SH_RATIO} > 0.10) }"; then
  TREND="declining"
elif awk "BEGIN { exit !(${SH_RATIO} - ${FH_RATIO} > 0.10) }"; then
  TREND="increasing"
fi

echo ""
cat <<EOF
=== MESSAGE_SENTIMENT ===
create_count: ${CREATE_COUNT}
maintain_count: ${MAINTAIN_COUNT}
other_count: ${OTHER_COUNT}
create_ratio: ${CREATE_RATIO}
maintain_ratio: ${MAINTAIN_RATIO}
first_half_create_ratio: ${FH_RATIO}
second_half_create_ratio: ${SH_RATIO}
sentiment_trend: ${TREND}
EOF

# --- Branches ---

ACTIVE_BRANCH="$(git branch --show-current 2>/dev/null || echo "detached")"
TOTAL_BRANCHES="$(git branch --list | wc -l | tr -d ' ')"

echo ""
echo "=== BRANCHES ==="
echo "active_branch: ${ACTIVE_BRANCH}"
echo "total_branches: ${TOTAL_BRANCHES}"

# Stale branches (no commits in 14+ days)
STALE_THRESHOLD=14
STALE_EPOCH=$(( NOW_EPOCH - STALE_THRESHOLD * 86400 ))

while IFS= read -r branch; do
  branch="$(echo "$branch" | sed 's/^[* ]*//' | tr -d ' ')"
  [ -z "$branch" ] && continue
  LAST_BRANCH_EPOCH="$(git log -1 --format='%at' "$branch" -- 2>/dev/null || echo "$NOW_EPOCH")"
  DAYS_STALE=$(( (NOW_EPOCH - LAST_BRANCH_EPOCH) / 86400 ))
  if [ "$LAST_BRANCH_EPOCH" -lt "$STALE_EPOCH" ]; then
    echo "stale: ${branch} (${DAYS_STALE} days)"
  fi
done < <(git branch --list)

# --- New Repos ---

echo ""
echo "=== NEW_REPOS ==="

REGISTRY="$HOME/.pyro/project-registry.yaml"
NEW_REPO_COUNT=0

if [ -f "$REGISTRY" ]; then
  # Try to find this project's spark_date from the registry
  # Look for the project entry matching our repo root or name
  PROJECT_NAME="$(basename "$REPO_ROOT")"
  SPARK_DATE=""

  # Parse YAML with grep/sed: find the block for this project, then its spark_date
  SPARK_DATE="$(grep -A 10 "name:.*${PROJECT_NAME}" "$REGISTRY" 2>/dev/null \
    | grep 'spark_date' | head -1 \
    | sed 's/.*spark_date:[[:space:]]*//' | tr -d '"' | tr -d "'" || echo "")"

  if [ -n "$SPARK_DATE" ]; then
    # Count projects with spark_date after ours and status active
    while IFS= read -r line; do
      OTHER_DATE="$(echo "$line" | sed 's/.*spark_date:[[:space:]]*//' | tr -d '"' | tr -d "'")"
      if [ -n "$OTHER_DATE" ] && [[ "$OTHER_DATE" > "$SPARK_DATE" ]]; then
        NEW_REPO_COUNT=$((NEW_REPO_COUNT + 1))
      fi
    done < <(grep 'spark_date' "$REGISTRY" 2>/dev/null || true)
    # Subtract 1 if we counted ourselves
    if [ "$NEW_REPO_COUNT" -gt 0 ]; then
      NEW_REPO_COUNT=$((NEW_REPO_COUNT > 0 ? NEW_REPO_COUNT : 0))
    fi
  fi

  echo "new_repos_detected: ${NEW_REPO_COUNT}"

  # List new repos if any
  if [ "$NEW_REPO_COUNT" -gt 0 ] && [ -n "$SPARK_DATE" ]; then
    # Re-scan and print names
    CURRENT_NAME=""
    CURRENT_SPARK=""
    while IFS= read -r line; do
      if echo "$line" | grep -q 'name:'; then
        CURRENT_NAME="$(echo "$line" | sed 's/.*name:[[:space:]]*//' | tr -d '"' | tr -d "'")"
      fi
      if echo "$line" | grep -q 'spark_date:'; then
        CURRENT_SPARK="$(echo "$line" | sed 's/.*spark_date:[[:space:]]*//' | tr -d '"' | tr -d "'")"
        if [ -n "$CURRENT_SPARK" ] && [[ "$CURRENT_SPARK" > "$SPARK_DATE" ]] && [ "$CURRENT_NAME" != "$PROJECT_NAME" ]; then
          echo "new_repo: ${CURRENT_NAME} (sparked ${CURRENT_SPARK})"
        fi
      fi
    done < "$REGISTRY"
  fi
else
  echo "new_repos_detected: 0"
  echo "# project-registry.yaml not found at ${REGISTRY}"
fi
