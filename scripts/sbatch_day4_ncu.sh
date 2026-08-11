#!/usr/bin/env bash
#SBATCH -J day4_ncu
#SBATCH -A <your_account>
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 00:30:00
#SBATCH --gpus 1
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 8
#SBATCH --output=day4_ncu_%j.out
#SBATCH --error=day4_ncu_%j.err

set -euo pipefail

export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs

# source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/setup.sh"
source setup.sh
source "$venv_name/bin/activate"

mkdir -p "$OUTBASE"

python -c "import cupy as cp; n=cp.cuda.runtime.getDeviceCount(); print(f'GPU check passed: {n} device(s) available')"

sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day4_ncu" \
  --n-events 3 \
  --profiler ncu
