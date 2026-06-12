#!/usr/bin/env bash
# generate_no_lyrics_v5.5.sh — render no_lyrics_v5.5.md via suno-pp-cli
# Keep in sync with no_lyrics_v5.5.md — Title/Lyrics/Style/Exclude are
# extracted live from the markdown; settings below mirror its table.
set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$PACK_DIR/no_lyrics_v5.5.md"
PROMPT_NAME="no_lyrics_v5.5"
SLUG="the_light_keeps_itself"
MODEL="v5.5"
WEIRDNESS=40
STYLE_INFLUENCE=80
INSTRUMENTAL=1   # Settings table: Instrumental toggle ON
VARIANT_LABEL="single"

cat <<BANNER
==================================================================
 The Light Keeps Itself — Instrumental — $MODEL
 Prompt file : $PROMPT_FILE
 Settings    : weirdness $WEIRDNESS / style influence $STYLE_INFLUENCE / instrumental ON
 COST        : ~10 credits for 2 takes — THIS SPENDS REAL CREDITS.
 Note        : --exclude is passed for forward-compat, but the CLI
               currently sends negative_tags empty; the anti-vocal
               defense here rests on the toggle + clean style +
               bracket structure tags (all of which transmit).
               v5.5 hallucinates vocals — budget regenerations.
==================================================================
BANNER

if [[ "${1:-}" != "--yes" ]]; then
  read -r -p "Spend credits and generate now? [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]] || { echo "Aborted — no credits spent."; exit 1; }
fi

command -v suno-pp-cli >/dev/null 2>&1 || {
  echo "suno-pp-cli not found. Install (no sudo!):"
  echo "  npx -y @mvanhorn/printing-press-library install suno"
  exit 1
}
command -v jq >/dev/null 2>&1 || { echo "jq is required."; exit 1; }

extract_after() { # $1=file $2=heading-regex
  awk -v pat="$2" '
    !hit && $0 ~ pat {hit=1; next}
    hit && /^```/ { if (inb) exit; inb=1; next }
    inb {print}
  ' "$1"
}

TITLE="$(extract_after "$PROMPT_FILE" '^## Title')"
STYLE="$(extract_after "$PROMPT_FILE" '^## Style of Music')"
EXCLUDE="$(extract_after "$PROMPT_FILE" '^## Exclude Styles')"
LYRICS_TMP="$(mktemp)"
trap 'rm -f "$LYRICS_TMP"' EXIT
extract_after "$PROMPT_FILE" '^## Lyrics' > "$LYRICS_TMP"

[[ -n "$TITLE" && -n "$STYLE" && -s "$LYRICS_TMP" ]] || {
  echo "Extraction failed (title/style/lyrics empty) — check $PROMPT_FILE"; exit 1; }

LYR_SHA="$(sha256sum "$LYRICS_TMP" | cut -c1-10)"
STY_SHA="$(printf '%s' "$STYLE" | sha256sum | cut -c1-10)"

if ls "$PACK_DIR/runs/"*.json >/dev/null 2>&1; then
  if grep -l "\"lyrics_sha256\": \"$LYR_SHA\"" "$PACK_DIR/runs/"*.json 2>/dev/null \
     | xargs -r grep -l "\"style_sha256\": \"$STY_SHA\"" >/dev/null 2>&1; then
    echo "WARNING: a prior run log in runs/ matches these exact prompts."
    if [[ "${1:-}" != "--yes" ]]; then
      read -r -p "Takes may already exist. Re-spend anyway? [y/N] " ans2
      [[ "$ans2" == "y" || "$ans2" == "Y" ]] || { echo "Aborted."; exit 1; }
    fi
  fi
fi

CREDITS_BEFORE="$(suno-pp-cli --agent credits 2>/dev/null || echo "unknown")"
echo "Credits before: $CREDITS_BEFORE"

suno-pp-cli --json --yes --dry-run generate create \
  --title "$TITLE" \
  --lyrics-file "$LYRICS_TMP" \
  --tags "$STYLE" \
  --exclude "$EXCLUDE" \
  --model "$MODEL" \
  --weirdness "$WEIRDNESS" --style-influence "$STYLE_INFLUENCE" \
  --instrumental \
  --wait >/dev/null
echo "Dry-run preflight OK — firing live."

RESP="$(suno-pp-cli --json --yes generate create \
  --title "$TITLE" \
  --lyrics-file "$LYRICS_TMP" \
  --tags "$STYLE" \
  --exclude "$EXCLUDE" \
  --model "$MODEL" \
  --weirdness "$WEIRDNESS" --style-influence "$STYLE_INFLUENCE" \
  --instrumental \
  --wait)"

mapfile -t CLIP_IDS < <(jq -r '(.clips // .data.clips // [])[] | .id // .clip_id // empty' <<<"$RESP")
if [[ ${#CLIP_IDS[@]} -eq 0 ]]; then
  mkdir -p "$PACK_DIR/runs"
  printf '%s' "$RESP" > "$PACK_DIR/runs/$(date -u +%Y-%m-%dT%H-%M-%SZ)-$PROMPT_NAME-raw-response.json"
  echo "No clip ids parsed — raw response saved to runs/ for inspection."
  echo "If this was a captcha failure (422 token_validation_failed), run:"
  echo "  suno-pp-cli auth captcha login"
  exit 1
fi

mkdir -p "$PACK_DIR/audio" "$PACK_DIR/runs"
N=0
for id in "${CLIP_IDS[@]}"; do
  N=$((N+1))
  TMPD="$(mktemp -d)"
  suno-pp-cli download "$id" --out "$TMPD/"
  SRC="$(find "$TMPD" -maxdepth 1 -type f -name '*.mp3' | head -n1)"
  DEST="$PACK_DIR/audio/${SLUG}-${MODEL}-take${N}-${id:0:8}.mp3"
  mv "$SRC" "$DEST"
  rm -rf "$TMPD"
  echo "take $N → $DEST"
done

TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
CREDITS_AFTER="$(suno-pp-cli --agent credits 2>/dev/null || echo "unknown")"
CLIPS_JSON="$(for i in "${!CLIP_IDS[@]}"; do
  n=$((i+1)); id="${CLIP_IDS[$i]}"
  jq -n --arg id "$id" --arg f "audio/${SLUG}-${MODEL}-take${n}-${id:0:8}.mp3" \
    '{clip_id:$id, file:$f}'
done | jq -s '.')"
jq -n \
  --arg pack "$SLUG" --arg pf "$PROMPT_NAME.md" --arg variant "$VARIANT_LABEL" \
  --arg model "$MODEL" --argjson w "$WEIRDNESS" --argjson s "$STYLE_INFLUENCE" \
  --argjson instr "$( ((INSTRUMENTAL)) && echo true || echo false )" \
  --arg lsha "$LYR_SHA" --arg ssha "$STY_SHA" \
  --argjson clips "$CLIPS_JSON" \
  --arg cb "$CREDITS_BEFORE" --arg ca "$CREDITS_AFTER" \
  '{request:{pack:$pack, prompt_file:$pf, variant:$variant,
    settings:{model:$model, weirdness:$w, style_influence:$s, instrumental:$instr},
    cli_args:["generate","create","--title","…","--lyrics-file","…","--tags","…","--exclude","…","--model",$model,"--weirdness",($w|tostring),"--style-influence",($s|tostring),"--instrumental","--wait"],
    lyrics_sha256:$lsha, style_sha256:$ssha, sliders_not_cli_settable:null},
   result:{clips:$clips, credits_before:$cb, credits_after:$ca, captcha:"open"},
   human_scorecard:{}}' \
  > "$PACK_DIR/runs/$TS-$PROMPT_NAME.json"
echo "Run log: runs/$TS-$PROMPT_NAME.json"

suno-pp-cli --agent sync --latest-only >/dev/null 2>&1 || true

echo "Done. ${#CLIP_IDS[@]} take(s) in audio/. Credits: $CREDITS_BEFORE → $CREDITS_AFTER"
echo "Listen and judge — the script has no ears. If vocals leaked in, regenerate."
