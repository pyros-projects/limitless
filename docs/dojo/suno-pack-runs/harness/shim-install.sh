#!/usr/bin/env bash
# Open a dojo test window: hold the real binary, install the shim.
set -euo pipefail
REAL=~/.local/bin/suno-pp-cli
HELD_DIR=~/.cache/dojo-suno-held
SHIM=/tmp/dojo-suno/shim/suno-pp-cli
if [[ -x "$REAL" ]] && ! "$REAL" --shim-check 2>/dev/null | grep -q DOJO-SHIM; then
  mkdir -p "$HELD_DIR"
  sha256sum "$REAL" > "$HELD_DIR/real.sha256"
  mv "$REAL" "$HELD_DIR/suno-pp-cli.real"
fi
cp "$SHIM" "$REAL" && chmod +x "$REAL"
"$REAL" --shim-check
echo "window OPEN — real binary held at $HELD_DIR"
