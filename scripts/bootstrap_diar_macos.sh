#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Homebrew deps (ffmpeg@7 for torchcodec dylibs; libsndfile for soundfile)
brew update >/dev/null
brew install ffmpeg@7 libsndfile >/dev/null || true

# Build venv from lock (uses pyenv python if present, else system python3)
type deactivate >/dev/null 2>&1 && deactivate || true

PY="${PYTHON_BIN:-}"
if [[ -z "${PY}" ]]; then
  if command -v pyenv >/dev/null 2>&1 && [[ -x "$(pyenv root)/versions/3.10.14/bin/python" ]]; then
    PY="$(pyenv root)/versions/3.10.14/bin/python"
  else
    PY="$(command -v python3)"
  fi
fi

rm -rf .venv-diar
"$PY" -m venv .venv-diar
source .venv-diar/bin/activate
python -m pip install -U pip setuptools wheel >/dev/null
python -m pip install -r locks/diar.lock.txt

# Make ffmpeg@7 visible for binaries + dylib resolution.
export PATH="/opt/homebrew/opt/ffmpeg@7/bin:/opt/homebrew/bin:${PATH}"
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/opt/ffmpeg@7/lib:/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"

# Verify + smoketest
./scripts/verify_diar_env.sh
./scripts/smoketest_audioio.sh

echo "bootstrap_diar_macos_ok"
