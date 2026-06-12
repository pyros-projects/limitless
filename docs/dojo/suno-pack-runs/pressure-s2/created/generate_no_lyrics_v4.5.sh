#!/usr/bin/env bash
# generate_no_lyrics_v4.5.sh — Sodium Lights — Instrumental — v4.5
# Emitted by suno-pack. Extracts prompt fields from no_lyrics_v4.5.md and
# fires the exact `generate create` invocation from references/pp-cli.md.
# NEVER uses --download (title collisions destroy takes); downloads per
# clip id and applies the take-aware rename.
set -euo pipefail
cd "$(dirname "$0")"

PROMPT_FILE="no_lyrics_v4.5.md"
SLUG="sodium_lights"
MODEL="v4.5"
WEIRDNESS=25
STYLE_INFLUENCE=90

# --- banner -----------------------------------------------------------
echo "=== Sodium Lights — Instrumental — v4.5 ==="
echo "Settings: model $MODEL | weirdness $WEIRDNESS | style influence $STYLE_INFLUENCE | instrumental ON"
echo "Style variant: A — lean tags (★ Recommended)"
echo
echo "WARNING: this command SPENDS Suno credits."
echo "Observed cost: 10 credits for one generate (2 takes) on v4.5."
echo

# --- preconditions ----------------------------------------------------
command -v suno-pp-cli >/dev/null 2>&1 || { echo "suno-pp-cli not found. Install: npx -y @mvanhorn/printing-press-library install suno (no sudo)"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq is required to parse clip ids"; exit 1; }
suno-pp-cli --agent doctor | grep -q '"credentials": *"valid"' || {
  echo "Doctor reports credentials are not valid. Log into suno.com in your"
  echo "browser, then run: suno-pp-cli auth login --chrome  — and retry."
  exit 1
}
echo "Credits before:"
suno-pp-cli --agent credits || true
echo

# --- confirm (explicit; --yes skips) ----------------------------------
if [[ "${1:-}" != "--yes" ]]; then
  read -r -p "Spend ~10 credits to render $PROMPT_FILE? [y/N] " answer
  case "$answer" in y|Y|yes|YES) ;; *) echo "Aborted — nothing spent."; exit 1;; esac
fi

# --- extract fields from the canonical markdown ------------------------
extract_block_after() { # $1 = heading regex; prints first fenced block after it
  awk -v h="$1" '
    $0 ~ h {found=1}
    found && /^```/ { if (inblock) exit; inblock=1; next }
    inblock {print}
  ' "$PROMPT_FILE"
}
TITLE="$(extract_block_after '^## Title')"
LYRICS="$(extract_block_after '^## Lyrics')"
EXCLUDE="$(extract_block_after '^## Exclude Styles')"
TAGS="$(extract_block_after 'Recommended')"   # the ★ Recommended variant
[[ -n "$TITLE" && -n "$LYRICS" && -n "$TAGS" ]] || { echo "Field extraction failed — check $PROMPT_FILE structure"; exit 1; }

# Note: --exclude is accepted for compatibility but the CLI sends
# negative_tags empty — exclude enforcement needs the web UI.

# --- fire ---------------------------------------------------------------
mkdir -p audio runs
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
RESPONSE_FILE="runs/${TS}-no_lyrics_v4.5.response.json"

suno-pp-cli --json --yes generate create \
  --title "$TITLE" \
  --lyrics "$LYRICS" \
  --tags "$TAGS" \
  --exclude "$EXCLUDE" \
  --model "$MODEL" \
  --weirdness "$WEIRDNESS" --style-influence "$STYLE_INFLUENCE" \
  --instrumental \
  --wait | tee "$RESPONSE_FILE"

# --- per-clip download + take-aware rename (never --download) -----------
CLIP_IDS="$(jq -r '(.data.clips // .clips // [])[].id' "$RESPONSE_FILE")"
[[ -n "$CLIP_IDS" ]] || { echo "No clip ids in response — inspect $RESPONSE_FILE"; exit 1; }

n=0
for clip_id in $CLIP_IDS; do
  n=$((n+1))
  suno-pp-cli download "$clip_id" --out audio/
  newest="$(ls -t audio/*.mp3 | head -1)"
  target="audio/${SLUG}-${MODEL}-take${n}-${clip_id:0:8}.mp3"
  mv -- "$newest" "$target"
  echo "take $n -> $target"
done
echo "Verify: $(ls audio/${SLUG}-${MODEL}-take*.mp3 | wc -l) take file(s) on disk."

suno-pp-cli --agent sync --latest-only
echo "Credits after:"
suno-pp-cli --agent credits || true
echo "Done. Raw response: $RESPONSE_FILE — listen and judge the takes yourself."
