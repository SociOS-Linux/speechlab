#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -d ".venv-diar" ]]; then
  echo "ERROR: .venv-diar missing. Run: ./scripts/rebuild_diar_env.sh" >&2
  exit 1
fi

if [[ ! -x "/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg" ]]; then
  echo "ERROR: ffmpeg@7 missing. Run: brew install ffmpeg@7" >&2
  exit 1
fi

source .venv-diar/bin/activate

# Make keg-only ffmpeg@7 visible for binaries + dylib resolution.
export PATH="/opt/homebrew/opt/ffmpeg@7/bin:/opt/homebrew/bin:${PATH}"
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@7/lib:/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"

export PS1="(diar) \u@\h:\w\$ "

echo "diar_shell: $(python -V)  exe=$(python -c 'import sys; print(sys.executable)')"
exec bash --noprofile --norc
