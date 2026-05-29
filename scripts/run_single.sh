#!/usr/bin/env bash
set -euo pipefail

: "${LARNDSIM_DIR:?set LARNDSIM_DIR}"
: "${INPUT_H5:?set INPUT_H5}"
: "${OUTDIR:=runs/single}"
: "${CONFIG:=2x2}"

source .venv/bin/activate || true

export HDF5_USE_FILE_LOCKING=${HDF5_USE_FILE_LOCKING:-0}

sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config "$CONFIG" \
  --input "$INPUT_H5" \
  --outdir "$OUTDIR"
