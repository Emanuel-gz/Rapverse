#!/usr/bin/env bash
# Complete the photo integration and create the downloadable project in Codex.
set -euo pipefail

RAPVERSE_PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$RAPVERSE_PROJECT_DIR"

python3 tools/import-photos.py
node --check script.js
node --check gallery.js
node --check tools/sync-fallback.mjs
python3 tests/smoke.py -v
python3 tools/package.py --output "${1:-$RAPVERSE_PROJECT_DIR/../Rapverse-mejorado.zip}"

printf '\nProyecto listo. Para abrirlo:\npython3 -m http.server 8000 --bind 127.0.0.1\n'
