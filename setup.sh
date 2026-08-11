#!/usr/bin/env bash
module unload python 2>/dev/null
module load cudatoolkit/12.9
module load python/3.11

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export REPO_DIR="$repo_dir"
export WORKDIR="${WORKDIR:-$repo_dir}"
export SIM2SPEC_DIR="$repo_dir"
export LARNDSIM_DIR="${LARNDSIM_DIR:-$WORKDIR/larnd-sim}"
export INPUT_H5="${INPUT_H5:-$repo_dir/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5}"
export OUTBASE="${OUTBASE:-$repo_dir/runs}"
export HDF5_USE_FILE_LOCKING="${HDF5_USE_FILE_LOCKING:-0}"
export LARNDSIM_DISABLE_CUPY_MEMPOOL="${LARNDSIM_DISABLE_CUPY_MEMPOOL:-1}"
# Override notebook-inherited inline backends. CLI/compute-node workflows here
# need a non-interactive backend.
export MPLBACKEND="Agg"
venv_name="sim2spec.venv"
export venv_name
