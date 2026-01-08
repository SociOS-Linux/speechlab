#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv-diar/bin/activate
export PATH="/opt/homebrew/opt/ffmpeg@7/bin:/opt/homebrew/bin:${PATH}"
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@7/lib:/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
exec python "$@"
