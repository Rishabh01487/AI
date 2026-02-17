#!/usr/bin/env bash
set -e
cd frontend
npm ci --legacy-peer-deps
npm run build
