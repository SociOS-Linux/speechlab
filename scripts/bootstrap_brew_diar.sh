#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "ERROR: Homebrew not found. Install it first: https://brew.sh" >&2
  exit 1
fi

brew update
brew install ffmpeg@7 libsndfile || (brew upgrade ffmpeg@7 libsndfile || true)

echo "OK: brew deps installed"
brew list --versions ffmpeg@7 libsndfile 2>/dev/null || true
