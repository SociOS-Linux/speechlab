#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# If we're inside the venv, deactivate before deleting it.
type deactivate >/dev/null 2>&1 && deactivate || true

# Ensure ffmpeg@7 is used (keg-only).
export PATH="/opt/homebrew/opt/ffmpeg@7/bin:/opt/homebrew/bin:${PATH}"
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@7/lib:/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"

# Deterministic Python: prefer pyenv 3.10.14 if present, else python3 on PATH.
if command -v pyenv >/dev/null 2>&1 && [[ -x "$(pyenv root)/versions/3.10.14/bin/python" ]]; then
  PY="$(pyenv root)/versions/3.10.14/bin/python"
else
  PY="$(command -v python3)"
fi

rm -rf .venv-diar
"$PY" -m venv .venv-diar
source .venv-diar/bin/activate

python -m pip install -U pip setuptools wheel
python -m pip install -r locks/diar.lock.txt

python -c "import numpy, soundfile, torch, torchcodec; import pyannote.audio as p; print('OK', 'numpy', numpy.__version__, 'soundfile', soundfile.__version__, 'torch', torch.__version__, 'torchcodec', torchcodec.__version__, 'pyannote', p.__version__)"
