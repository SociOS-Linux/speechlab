#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -d ".venv-diar" ]]; then
  echo "ERROR: .venv-diar missing. Run: ./scripts/rebuild_diar_env.sh" >&2
  exit 1
fi

if [[ ! -x "./scripts/run_diar_python.sh" ]]; then
  echo "ERROR: ./scripts/run_diar_python.sh missing or not executable." >&2
  echo "Fix: chmod +x scripts/run_diar_python.sh" >&2
  exit 1
fi

if [[ ! -x "/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg" ]]; then
  echo "ERROR: ffmpeg@7 missing. Run: brew install ffmpeg@7" >&2
  exit 1
fi

echo "== brew ==" && (brew list --versions ffmpeg@7 libsndfile 2>/dev/null || true)
echo "== ffmpeg@7 ==" && (/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg -version | head -n 2 || true)

echo "== python interpreter (must be .venv-diar) =="
./scripts/run_diar_python.sh -c "import sys; print(sys.executable)"

echo "== python imports (all must succeed) =="
./scripts/run_diar_python.sh -c "import numpy, soundfile, torch, torchcodec; import pyannote.audio as p; print('OK', 'numpy', numpy.__version__, 'soundfile', soundfile.__version__, 'torch', torch.__version__, 'torchcodec', torchcodec.__version__, 'pyannote', p.__version__)"

echo "NOTE: If plain 'python' later says numpy is missing, you are OUTSIDE the venv. Use ./scripts/run_diar_python.sh."
