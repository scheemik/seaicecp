#!/usr/bin/env bash
set -euo pipefail

: "${SICP_DATA_DIR:?You must set SICP_DATA_DIR (e.g. export SICP_DATA_DIR=/Volumes/drive/path)}"

if [ ! -d "$SICP_DATA_DIR" ]; then
  echo "ERROR: SICP_DATA_DIR does not exist: $SICP_DATA_DIR"
  exit 1
fi

podman run -it --rm \
  -v "$(pwd)":/workspace \
  -v "${SICP_DATA_DIR}":/seaicecp_data \
  -w /workspace \
  seaicecp_0
#   bash -lc "uv sync && bash"