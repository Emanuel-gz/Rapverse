#!/usr/bin/env bash
# Validate the bundled photographs and package the complete project in Codex.
set -euo pipefail

RAPVERSE_PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$RAPVERSE_PROJECT_DIR"

python3 tools/import-photos.py --from-directory assets/photos
node tools/sync-fallback.mjs
node --check script.js
node --check gallery.js
node --check fx.js
node --check tools/sync-fallback.mjs
python3 tests/smoke.py -v
python3 tools/package.py --output "${1:-$RAPVERSE_PROJECT_DIR/../Rapverse-mejorado.zip}"

printf '\nProyecto listo. Para abrirlo:\npython3 tools/serve.py --port 8000\n'
