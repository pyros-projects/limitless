#!/usr/bin/env bash
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

if [[ -n "${CM_BIN:-}" ]]; then
  CM=("${CM_BIN}")
elif [[ -x "${PLUGIN_ROOT}/.venv/bin/codies-memory" ]]; then
  CM=("${PLUGIN_ROOT}/.venv/bin/codies-memory")
else
  CM=(uv run codies-memory)
fi

tmp_home=""
tmp_project=""
tmp_float=""

cleanup() {
  if [[ -n "${tmp_home}" ]]; then
    rm -rf "${tmp_home}"
  fi
  if [[ -n "${tmp_project}" ]]; then
    rm -rf "${tmp_project}"
  fi
  if [[ -n "${tmp_float}" ]]; then
    rm -rf "${tmp_float}"
  fi
}
trap cleanup EXIT

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

ok() {
  printf 'ok - %s\n' "$*"
}

contains() {
  local haystack="$1"
  local needle="$2"
  if [[ "${haystack}" != *"${needle}"* ]]; then
    printf '--- output ---\n%s\n--------------\n' "${haystack}" >&2
    fail "expected output to contain: ${needle}"
  fi
}

not_contains() {
  local haystack="$1"
  local needle="$2"
  if [[ "${haystack}" == *"${needle}"* ]]; then
    printf '--- output ---\n%s\n--------------\n' "${haystack}" >&2
    fail "expected output not to contain: ${needle}"
  fi
}

run_cm() {
  HOME="${tmp_home}" "${CM[@]}" "$@"
}

tmp_home="$(mktemp -d)"
tmp_project="$(mktemp -d)"
tmp_float="$(mktemp -d)"
agent="Smoke"
project_slug="project-smoke"

printf 'codies-memory smoke using HOME=%s\n' "${tmp_home}"

global_init="$(run_cm init --type global --agent "${agent}")"
contains "${global_init}" "Initialized global vault"
run_cm validate --type global --agent "${agent}" >/dev/null
ok "global init and validate"

project_init="$(run_cm init --type project --agent "${agent}" --slug "${project_slug}" --working-dir "${tmp_project}")"
contains "${project_init}" "Initialized project vault"
[[ "$(cat "${tmp_project}/.codies-memory")" == "${project_slug}" ]] || fail "project marker did not contain ${project_slug}"
run_cm validate --type project --agent "${agent}" --working-dir "${tmp_project}" >/dev/null
ok "project init, marker, and validate"

user_out="$(run_cm user "Smoke user prefers explicit memory checks." --agent "${agent}")"
contains "${user_out}" "Noted:"
grep -Fq "Smoke user prefers explicit memory checks." "${tmp_home}/.memory/${agent}/identity/user.md"

feedback_out="$(run_cm feedback "Smoke feedback exercises feedback storage." --agent "${agent}")"
contains "${feedback_out}" "Feedback saved:"
find "${tmp_home}/.memory/${agent}/feedback" -type f -name 'FB-*.md' -print -quit | grep -q .
ok "user and feedback writes"

capture_id="$(run_cm capture "Project inbox item for smoke promotion" \
  --source smoke \
  --gate allow \
  --short "Project inbox smoke" \
  --agent "${agent}" \
  --working-dir "${tmp_project}")"
[[ "${capture_id}" == IN-* ]] || fail "expected project capture ID to start with IN-, got ${capture_id}"

status_out="$(run_cm status --agent "${agent}" --working-dir "${tmp_project}" --all)"
contains "${status_out}" "Active: 1"
contains "${status_out}" "Project inbox item for smoke promotion"

inbox_list="$(run_cm list inbox --agent "${agent}" --working-dir "${tmp_project}")"
contains "${inbox_list}" "${capture_id:0:11}"
inbox_path="$(run_cm list inbox --agent "${agent}" --working-dir "${tmp_project}" --format paths | head -n 1)"
[[ -f "${inbox_path}" ]] || fail "project inbox path does not exist: ${inbox_path}"

thread_id="$(run_cm promote "${inbox_path}" --to thread --agent "${agent}" --working-dir "${tmp_project}")"
[[ "${thread_id}" == TH-* ]] || fail "expected thread ID, got ${thread_id}"
thread_list="$(run_cm list threads --agent "${agent}" --working-dir "${tmp_project}")"
contains "${thread_list}" "Project inbox item for smoke promotion"
status_after_promote="$(run_cm status --agent "${agent}" --working-dir "${tmp_project}" --all)"
contains "${status_after_promote}" "Active: 0"
ok "project capture, list, status, and promote to thread"

lesson_id="$(run_cm create lesson \
  --title "Project Smoke Lesson" \
  --short "Project lesson smoke" \
  --body "When smoke tests run, assert the CLI consistency path end to end." \
  --trust confirmed \
  --field "trigger=package smoke" \
  --field "why=catch cross-command regressions" \
  --agent "${agent}" \
  --working-dir "${tmp_project}")"
[[ "${lesson_id}" == LS-* ]] || fail "expected lesson ID, got ${lesson_id}"

decision_id="$(run_cm create decision \
  --title "Project Smoke Decision" \
  --short "Project decision smoke" \
  --body "The smoke flow should cover both named project and catch-all project behavior." \
  --field "rationale=general consistency matters" \
  --agent "${agent}" \
  --working-dir "${tmp_project}")"
[[ "${decision_id}" == DC-* ]] || fail "expected decision ID, got ${decision_id}"

session_body="${tmp_project}/session-body.md"
printf 'Project session body from a body file.\nNext check the smoke logs.\n' > "${session_body}"
session_id="$(run_cm create session \
  --title "Project Smoke Session" \
  --short "Project session smoke" \
  --body-file "${session_body}" \
  --field "next_step=Review smoke logs" \
  --agent "${agent}" \
  --working-dir "${tmp_project}")"
[[ "${session_id}" == SS-* ]] || fail "expected session ID, got ${session_id}"

lesson_json="$(run_cm list lessons --agent "${agent}" --working-dir "${tmp_project}" --format json)"
contains "${lesson_json}" "Project Smoke Lesson"
session_list="$(run_cm list sessions --agent "${agent}" --working-dir "${tmp_project}")"
contains "${session_list}" "Project Smoke Session"
ok "project lesson, decision, session, JSON list, and body-file flow"

lesson_path="$(run_cm list lessons --agent "${agent}" --working-dir "${tmp_project}" --format paths | head -n 1)"
[[ -f "${lesson_path}" ]] || fail "project lesson path does not exist: ${lesson_path}"
global_lesson_id="$(run_cm promote "${lesson_path}" --to-global --agent "${agent}")"
[[ "${global_lesson_id}" == LS-G* ]] || fail "expected global lesson ID, got ${global_lesson_id}"
global_lessons="$(run_cm list lessons --scope global --agent "${agent}")"
contains "${global_lessons}" "Project Smoke Lesson"

reflection_id="$(run_cm create reflection \
  --title "Smoke Reflection" \
  --short "Smoke reflection" \
  --body "A smoke test is a tiny proof that continuity still works." \
  --agent "${agent}" \
  --working-dir "${tmp_project}")"
[[ "${reflection_id}" == RF-* ]] || fail "expected reflection ID, got ${reflection_id}"
reflections="$(run_cm list reflections --scope global --agent "${agent}")"
contains "${reflections}" "Smoke Reflection"
ok "global lesson promotion and global reflection auto-routing"

refresh_out="$(run_cm refresh --agent "${agent}" --working-dir "${tmp_project}")"
contains "${refresh_out}" "global_summary:"
contains "${refresh_out}" "project_summary:"
contains "${refresh_out}" "recent_episodes:"

project_boot="$(run_cm boot --agent "${agent}" --working-dir "${tmp_project}" 2>&1)"
not_contains "${project_boot}" "no project vault found"
contains "${project_boot}" "Project Smoke Decision"
contains "${project_boot}" "Project Smoke Session"
contains "${project_boot}" "Global Daily Log"
contains "${project_boot}" "Smoke Reflection"
ok "refresh and named-project boot"

general_capture_id="$(run_cm capture "General inbox item for smoke" \
  --source smoke \
  --gate allow \
  --short "General inbox smoke" \
  --agent "${agent}" \
  --working-dir "${tmp_float}")"
[[ "${general_capture_id}" == IN-* ]] || fail "expected general capture ID, got ${general_capture_id}"

general_session_id="$(run_cm create session \
  --title "General Smoke Session" \
  --short "General session smoke" \
  --body "General session body should only appear during explicit general boot." \
  --agent "${agent}" \
  --working-dir "${tmp_float}")"
[[ "${general_session_id}" == SS-* ]] || fail "expected general session ID, got ${general_session_id}"

status_none="$(run_cm status --agent "${agent}" --working-dir "${tmp_float}")"
contains "${status_none}" "Project vault: none"

if run_cm list sessions --agent "${agent}" --working-dir "${tmp_float}" >/tmp/codies-memory-smoke-list.out 2>/tmp/codies-memory-smoke-list.err; then
  fail "vault-less list sessions succeeded without --general"
fi
grep -Fq "no project vault found" /tmp/codies-memory-smoke-list.err
rm -f /tmp/codies-memory-smoke-list.out /tmp/codies-memory-smoke-list.err

status_general="$(run_cm status --agent "${agent}" --working-dir "${tmp_float}" --general --all)"
contains "${status_general}" "/_general"
contains "${status_general}" "Active: 1"
contains "${status_general}" "General inbox item for smoke"

general_sessions="$(run_cm list sessions --agent "${agent}" --working-dir "${tmp_float}" --general)"
contains "${general_sessions}" "General Smoke Session"
ok "vault-less writes, normal read refusal, and explicit general status/list"

normal_float_boot="$(run_cm boot --agent "${agent}" --working-dir "${tmp_float}" 2>&1)"
contains "${normal_float_boot}" "Warning: no project vault found; global-only boot."
contains "${normal_float_boot}" "Global Daily Log"
contains "${normal_float_boot}" "General session smoke (_general)"
not_contains "${normal_float_boot}" "General session body should only appear"

general_boot="$(run_cm boot --agent "${agent}" --working-dir "${tmp_float}" --general 2>&1)"
contains "${general_boot}" "Using reserved _general project vault."
contains "${general_boot}" "General Smoke Session"
contains "${general_boot}" "General session body should only appear"
contains "${general_boot}" "Global Daily Log"

if run_cm list reflections --scope global --agent "${agent}" --general >/tmp/codies-memory-smoke-general.out 2>/tmp/codies-memory-smoke-general.err; then
  fail "global list accepted --general"
fi
grep -Fq -- "--general can only be used with --scope project" /tmp/codies-memory-smoke-general.err
rm -f /tmp/codies-memory-smoke-general.out /tmp/codies-memory-smoke-general.err
ok "global-only boot versus explicit general boot"

daily_log="$(run_cm list daily-log --scope global --agent "${agent}")"
contains "${daily_log}" "DL-"
daily_file="$(find "${tmp_home}/.memory/${agent}/sessions" -type f -name '*.md' -print -quit)"
[[ -f "${daily_file}" ]] || fail "daily log file does not exist"
grep -Fq "Project lesson smoke (${project_slug})" "${daily_file}"
grep -Fq "General session smoke (_general)" "${daily_file}"
ok "daily-log list and append-only contents"

run_cm validate --type global --agent "${agent}" >/dev/null
run_cm validate --type project --agent "${agent}" --working-dir "${tmp_project}" >/dev/null
ok "final validation"

printf '\nPASS: codies-memory smoke completed with isolated HOME=%s\n' "${tmp_home}"
