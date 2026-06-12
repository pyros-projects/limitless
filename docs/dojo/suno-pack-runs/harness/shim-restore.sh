#!/usr/bin/env bash
# Close the dojo test window: restore and verify the real binary.
set -euo pipefail
REAL=~/.local/bin/suno-pp-cli
HELD_DIR=~/.cache/dojo-suno-held
if [[ ! -f "$HELD_DIR/suno-pp-cli.real" ]]; then echo "nothing held"; exit 1; fi
mv "$HELD_DIR/suno-pp-cli.real" "$REAL" && chmod +x "$REAL"
sha256sum -c "$HELD_DIR/real.sha256"
if "$REAL" --shim-check 2>/dev/null | grep -q DOJO-SHIM; then echo "FAIL: shim still in place"; exit 1; fi
echo "window CLOSED — real binary restored and checksum-verified"
