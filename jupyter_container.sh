#!/usr/bin/env bash
set -euo pipefail

IMAGE="seaicecp_0"
CONTAINER_NAME="sicp_cont"
WORKDIR="/workspace"

export SICP_DATA_DIR=/Volumes/BERGY_BITS/seaicecp_data/
SICP_DATA_DIR="${SICP_DATA_DIR:-}"

# ---- cleanup old container if it exists ----
podman rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

# ---- validate external data ----
if [[ -n "$SICP_DATA_DIR" ]]; then
  if [[ ! -d "$SICP_DATA_DIR" ]]; then
    echo "ERROR: SICP_DATA_DIR does not exist: $SICP_DATA_DIR"
    exit 1
  fi
fi

# ---- build volume args ----
VOLUMES=(-v "$(pwd)":"$WORKDIR")

if [[ -n "$SICP_DATA_DIR" ]]; then
  VOLUMES+=(-v "$SICP_DATA_DIR:/seaicecp_data")
fi

# ---- run container with Jupyter as main process ----
podman run -it \
  --name "$CONTAINER_NAME" \
  -p 8889:8888 \
  "${VOLUMES[@]}" \
  -w "$WORKDIR" \
  "$IMAGE" \
  bash -lc "
    set -e

    # Ensure reproducible env
    uv sync

    # Install kernel into uv environment (NOT /root)
    uv run python -m ipykernel install \
      --name python3 \
      --display-name 'Python (container)' \
      --sys-prefix

    # Start Jupyter as PID 1 (no nohup, no exec, no backgrounding)
    exec uv run jupyter lab \
      --ip=0.0.0.0 \
      --port=8888 \
      --no-browser \
      --allow-root \
      --ServerApp.token='' \
      --ServerApp.password=''
  "