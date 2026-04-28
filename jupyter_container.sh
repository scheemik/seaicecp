#!/usr/bin/env bash
set -euo pipefail

# ---- config ----
IMAGE="seaicecp_0"
CONTAINER_NAME="sicp_cont"
WORKDIR="/workspace"

# Export path of external data directory
export SICP_DATA_DIR=/Volumes/BERGY_BITS/seaicecp_data/
SICP_DATA_DIR="${SICP_DATA_DIR:-}"

# ---- cleanup old container if it exists ----
podman rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

# ---- build image (optional, comment out if already built) ----
# podman build -f .devcontainer/Containerfile -t "$IMAGE" .

# ---- run container ----
RUN_ARGS=(
  -dit
  --name "$CONTAINER_NAME"
  -p 8888:8888
  -v "$(pwd)":"$WORKDIR"
  -w "$WORKDIR"
)

# mount external data if provided
if [[ -n "$SICP_DATA_DIR" ]]; then
  if [[ ! -d "$SICP_DATA_DIR" ]]; then
    echo "ERROR: SICP_DATA_DIR does not exist: $SICP_DATA_DIR"
    exit 1
  fi
  RUN_ARGS+=(-v "$SICP_DATA_DIR:/seaicecp_data")
fi

podman run -it --rm "${RUN_ARGS[@]}" "$IMAGE"

# ---- install dependencies + start Jupyter inside container ----
podman exec "$CONTAINER_NAME" bash -lc "
  set -e
  uv sync
  uv run python -m ipykernel install --user --name python3
  exec uv run jupyter lab \
    --ip=0.0.0.0 \
    --no-browser \
    --allow-root \
    --ServerApp.token='dev-token' \
    --ServerApp.password=''
"