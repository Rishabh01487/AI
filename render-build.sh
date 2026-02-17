#!/usr/bin/env bash
set -e
# Wrapper at repo root so Render can execute a single script
if [ -x ./frontend/render-build.sh ]; then
  ./frontend/render-build.sh
else
  bash ./frontend/render-build.sh
fi
