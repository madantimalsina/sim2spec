# DOE_HPC_Bootcamp_2026

This repository contains the `sim2spec` project for the DOE HPC Bootcamp. The broader bootcamp project context is listed under [NERSC Projects for the DOE Bootcamp](https://www.alcf.anl.gov/events/argonne-introduction-hpc-bootcamp).

## sim2spec

`sim2spec` is a lightweight workflow wrapper around [DUNE/larnd-sim](https://github.com/DUNE/larnd-sim) for running, validating, comparing, and profiling GPU-based detector simulations on Perlmutter.

This repository is designed for students who are new to HPC workflows and want a structured way to:
- install and run a GPU simulation workflow,
- generate QA summaries and plots,
- compare multiple run configurations,
- track provenance and reproducibility,
- and profile performance on Perlmutter (A100 GPU).

This project does **not** replace `larnd-sim`. Instead, it organizes the workflow around it.

## How to use this project

This repository is organized for HPC beginners. Start by reading the concept sections below, then open the daily project files as exercises. The goal is not to memorize every command; the goal is to understand what each command is asking the HPC system to do and how to check whether it worked.

```mermaid
flowchart LR
    A[Your laptop or browser] --> B[NERSC login node]
    B --> C[Slurm scheduler]
    C --> D[Perlmutter GPU compute node]
    D --> E[larnd-sim run]
    E --> F[output.h5]
    F --> G[QA metrics and plots]
    G --> H[Sweep comparison]
    H --> I[Profiling and final summary]
```

## Beginner concepts map

### HPC system

- **HPC** means high-performance computing: using shared supercomputing resources for work that is too large, slow, or specialized for a laptop.
- **Perlmutter** is the NERSC supercomputer used by this project.
- **Login node** is where you log in, edit files, submit jobs, and manage the project. Do not run heavy GPU simulations directly on login nodes.
- **Compute node** is where Slurm runs your actual job. GPU simulations should run on GPU compute nodes.
- **`$PSCRATCH`** is a high-performance scratch filesystem for active work and output files.

### Scheduling

- **Slurm** is the workload manager. It decides when and where your job runs.
- **`salloc`** requests an interactive allocation. Use it when you want a live shell on a compute node.
- **`sbatch`** submits a batch job script. Use it when you want the system to run the workflow without keeping an interactive shell open.
- **`srun`** launches work inside an allocation or asks Slurm to run one command on compute resources.

### Software environment

- **Environment modules** load site-provided software such as Python.
- **Python virtual environment** keeps this project's Python packages separate from other projects.
- **CUDA** is NVIDIA's GPU programming platform.
- **CuPy** provides NumPy-like arrays that run on NVIDIA GPUs.
- **Numba** is a Python JIT compiler often used in GPU and performance-oriented Python workflows.

### Simulation workflow

- **`larnd-sim`** is the detector simulation package that performs the core GPU-based simulation.
- **`sim2spec`** is the wrapper in this repository. It organizes `larnd-sim` runs, QA, sweeps, provenance, and profiling into a beginner-friendly workflow.
- **HDF5** is the file format used for large structured simulation input and output files.
- **`output.h5`** is the main simulation result file produced by a run.

### Validation and reproducibility

- **QA** means quality assurance: quick checks that the output exists and contains reasonable datasets, counts, ranges, and plots.
- **Validation plots** help connect numbers in QA metrics to physical behavior such as charge timing, event activity, and light waveforms.
- **Manifest** means a machine-readable record of how a run was produced.
- **Provenance** means the information needed to understand and reproduce a result: input file, code version, seed, environment, command, and output path.
- **Random seed** controls stochastic parts of a simulation so different variants can be compared systematically.

### Performance

- **Profiling** measures where time is spent.
- **Nsight Systems** is NVIDIA's timeline profiler for CPU/GPU applications.
- **Kernel** means a function launched on the GPU.
- **Wall time** is the elapsed time you wait for a run to finish.

## Exercise guides

- [Project_1_ReadMe.md](Project_1_ReadMe.md) — Day 1: environment setup, install, and smoke test
- [Project_2_ReadMe.md](Project_2_ReadMe.md) — Day 2: baseline run, QA, and validation plots
- [Project_3_ReadMe.md](Project_3_ReadMe.md) — Day 3: parameter sweeps and provenance tracking
- [Project_4_ReadMe.md](Project_4_ReadMe.md) — Day 4: profiling and one measurable improvement
- [Project_5_ReadMe.md](Project_5_ReadMe.md) — Day 5: final cross-day comparison and summary
- [sim2spec_perlmutter_bootcamp.ipynb](JNotebook/sim2spec_perlmutter_bootcamp.ipynb) — interactive notebook for participants who prefer to complete the exercises in Jupyter instead of the terminal. It is meant for the exercises only. Please still read daily `Project_N_ReadMe.md` for more HPC background and context.

## Quick start

### 1. Clone the repository

```bash
export MYWORKDIR=$PSCRATCH/HPC_intro
mkdir -p "$MYWORKDIR"
cd "$MYWORKDIR"

git clone https://github.com/madantimalsina/sim2spec.git
cd sim2spec
```

### 2. Set up the environment

```bash
source setup.sh
bash install.sh
```

### 3. Activate the virtual environment

```bash
source setup.sh
source "$venv_name/bin/activate"
```

### 4. Quick environment check

Run these checks before trying a real workflow step:

```bash
python -c "import fire; print('fire ok')"
python -c "import cupy as cp; print(int(cp.arange(10).sum()))"
python -c "import larndsim; print('larndsim ok')"
```

If these work, your Python environment is in good shape.

## Before you begin

You will need a NERSC compute allocation and access to Perlmutter. For GPU work, request an interactive node or submit a batch job before running simulations.

For short setup checks and baseline tests:

```bash
salloc -C gpu -q interactive -t 00:30:00 -A <your_account> --gpus=1 --ntasks=1 --cpus-per-task=8
```

For longer sweep or profiling work, request more time:

```bash
salloc -C gpu -q interactive -t 00:60:00 -A <your_account> --gpus=1 --ntasks=1 --cpus-per-task=8
```

## Basic workflow examples

Note: follow the matching daily guide for the block you are working on.

### Baseline run

```bash
export WORKDIR=$PWD
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs

mkdir -p "$OUTBASE"

sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day2_baseline" \
  --n-events 5
```

#### QA on an existing run

```bash
sim2spec qa --run-dir "$OUTBASE/day2_baseline/run"
```

### Sweep run

```bash
sim2spec sweep \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day3_sweep" \
  --sweep "$WORKDIR/configs/sweep.yaml" \
  --n-events 3
```

### Profiling run

```bash
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1

sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day4_profile_baseline" \
  --n-events 10 \
  --profiler nsys
```

#### Write profile summary

```bash
sim2spec profile --run-dir "$OUTBASE/day4_profile_baseline/run"
```

## Prefer batch jobs?

Every GPU step also has a corresponding sbatch script in `scripts/`. For example:

```bash
sbatch scripts/sbatch_day1_smoke.sh
sbatch scripts/sbatch_day2_baseline.sh
sbatch scripts/sbatch_day3_sweep.sh
sbatch scripts/sbatch_day4_profile_baseline.sh
sbatch scripts/sbatch_day4_profile_compare.sh
```

Remember to replace `<your_account>` with your NERSC project account before submitting.

## Repository structure

Below is a beginner-friendly explanation of the main files and folders in the repository.

### [`src/__init__.py`](src/__init__.py)

Very small file.  
It mainly defines the package version and marks `src/` as the Python package location.

Why it matters:
- helps Python treat the source code as an installable package
- provides a clean package entry point

---

### [`src/cli.py`](src/cli.py)

This is the main command-line entry point.

It defines the commands:
- `sim2spec run`
- `sim2spec sweep`
- `sim2spec qa`
- `sim2spec profile`

What each command does:

**`run`**
- runs a single `larnd-sim` job
- writes output to a run directory
- saves a manifest and command file

**`sweep`**
- loads multiple variants from a YAML file
- runs one simulation per variant
- automatically runs QA for each

**`qa`**
- reads one run directory
- generates metrics and plots

**`profile`**
- parses profiling outputs for one run

Why it matters:
- this file is the public interface of the project
- when a user types `sim2spec ...`, this is what executes

---

### [`src/runner.py`](src/runner.py)

This file is responsible for actually launching `larnd-sim`.

What it does:
- builds the command used to call `larnd-sim`
- creates the run directory
- saves the command and manifest
- optionally wraps the run with profiling tools such as `nsys`

Why it matters:
- this is the main bridge between `sim2spec` and `larnd-sim`
- if you want to understand how a run is executed, start here

---

### [`src/qa.py`](src/qa.py)

This is the quality-assurance module.

What it does:
- opens the output HDF5 file
- checks for expected datasets
- computes summary metrics such as:
  - packet counts
  - ADC statistics
  - timestamp range
  - light waveform counts if present
- creates quick plots for validation

Why it matters:
- this is the first layer of output validation
- it helps answer the question: "does this run look reasonable?"

---

### [`src/provenance.py`](src/provenance.py)

This module handles reproducibility metadata.

What it does:
- records timestamps and environment information
- records selected environment variables
- collects git information for the `larnd-sim` checkout
- helps build `manifest.json` for each run

Why it matters:
- reproducibility is a major part of the workflow
- this file makes each run easier to understand and reproduce later

---

### [`src/prof.py`](src/prof.py)

This is the profiling helper module.

What it does:
- finds profiling outputs, especially `nsys` results
- runs summary commands such as `nsys stats`
- saves a simplified JSON report

Why it matters:
- raw profiling outputs can be hard to read directly
- this module makes them easier to compare between runs

---

### [`src/config_patch.py`](src/config_patch.py)

This file handles sweep-related configuration logic.

What it does:
- reads YAML files
- loads sweep variants from [`configs/sweep.yaml`](configs/sweep.yaml)
- writes updated YAML if needed

Why it matters:
- the sweep workflow depends on a clean way to define multiple run variants

---

### [`src/utils.py`](src/utils.py)

This file contains small helper utilities used across the project.

Typical examples include:
- creating directories safely
- reading and writing JSON
- collecting timestamps
- merging dictionaries

Why it matters:
- it keeps repeated helper logic out of the main workflow files

---

### [`configs/sweep.yaml`](configs/sweep.yaml)

This file defines the parameter sweep used by `sim2spec sweep`.

What it does:
- lists four named variants, each with a distinct random seed
- the seed drives stochastic variation so each variant produces observably different outputs

Why it matters:
- this is how multiple runs are compared in a controlled, reproducible way

---

### [`input/`](input/)

This folder stores input files used for the workflow.

For this project, it is expected to contain:
- `MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5`

Why it matters:
- keeping the input in a predictable place makes the notebook and shell scripts easier to follow

---

### [`setup.sh`](setup.sh)

This is the lightweight environment setup script.

What it does:
- unloads any conflicting Python module
- loads `python/3.11`
- defines the virtual-environment name
- prepares shell variables used by `install.sh`

Why it matters:
- this is the recommended first command to source when starting a terminal session for the project

---

### [`install.sh`](install.sh)

This is the main installation script for terminal users.

What it does:
- creates a virtual environment
- installs Python dependencies
- installs `sim2spec`
- clones and installs `larnd-sim` (skips clone if already present)

Why it matters:
- this is the easiest way for terminal users to get started without following the full notebook

---

### [`plot_validation.py`](plot_validation.py)

Standalone script for producing validation plots directly from an output HDF5 file.

```bash
python plot_validation.py "$OUTBASE/day2_baseline/run/output.h5" --outdir "$OUTBASE/day2_baseline/run/validation_plots"
```

Why it matters:
- a quick way to visualise any run output without running the full QA pipeline

---

### [`README.md`](README.md)

This file is the top-level overview of the repository.

Why it matters:
- it gives a quick map of the project
- it points students to the detailed guides and notebooks

---

### [`Project_1_ReadMe.md`](Project_1_ReadMe.md) through [`Project_5_ReadMe.md`](Project_5_ReadMe.md)

These are the focused day-by-day project guides for terminal users.

What they contain:
- Day 1: environment setup, install, and smoke test
- Day 2: baseline run, QA, and validation plots
- Day 3: parameter sweeps and provenance tracking
- Day 4: profiling and one measurable improvement
- Day 5: final cross-day comparison and summary

Why they matter:
- each file keeps one bootcamp work block short, focused, and easier to follow during project time

---

### [`sim2spec_perlmutter_bootcamp.ipynb`](JNotebook/sim2spec_perlmutter_bootcamp.ipynb)

The main student-facing notebook. Mirrors the `Project_1_ReadMe.md` through `Project_5_ReadMe.md` day guides with executable cells and `srun`-based GPU dispatch so students can run everything from inside JupyterHub.

Why it matters:
- the recommended path for students who prefer notebooks over the terminal
- keeps the notebook path shorter than the readmes while producing the same core outputs

---

## Suggested reading order

If you are new to the repository, a good order is:

1. [README.md](README.md)
2. [Project_1_ReadMe.md](Project_1_ReadMe.md) through [Project_5_ReadMe.md](Project_5_ReadMe.md)
3. [sim2spec_perlmutter_bootcamp.ipynb](JNotebook/sim2spec_perlmutter_bootcamp.ipynb) — if you prefer notebooks
4. [src/cli.py](src/cli.py)
5. [src/runner.py](src/runner.py)
6. [src/qa.py](src/qa.py)
7. [src/provenance.py](src/provenance.py)
8. [configs/sweep.yaml](configs/sweep.yaml)

## References

Bootcamp and computing resources:
- [NERSC Projects for the DOE Bootcamp](https://www.alcf.anl.gov/events/argonne-introduction-hpc-bootcamp)
- [NERSC Documentation](https://docs.nersc.gov/)

Simulation and detector workflow resources:
- [2x2 Demonstrator literature record](https://inspirehep.net/literature/2620145)
- [DUNE larnd-sim documentation](https://dune.github.io/larnd-sim/larndsim.html)
- [DUNE/larnd-sim GitHub repository](https://github.com/DUNE/larnd-sim)
- [LBL neutrino larnd-sim example](https://github.com/lbl-neutrino/larnd-sim-example)
- [DUNE 2x2_sim GitHub repository](https://github.com/DUNE/2x2_sim)
- [Tutorial on running 2x2_sim, April 2024](https://github.com/DUNE/2x2_sim/wiki/Tutorial-on-running-2x2_sim-Apr2024)

Tools used by this workflow:
- [Python documentation](https://docs.python.org/3/)
- [Numba documentation](https://numba.readthedocs.io/)
- [CuPy documentation](https://docs.cupy.dev/)
- [h5py documentation](https://docs.h5py.org/)
- [Matplotlib documentation](https://matplotlib.org/stable/)
- [Slurm workload manager documentation](https://slurm.schedmd.com/documentation.html)
- [NVIDIA Nsight Systems](https://developer.nvidia.com/nsight-systems/get-started)
- [NVIDIA CUDA Toolkit documentation](https://docs.nvidia.com/cuda/)

## Notes

- This wrapper does not replace `larnd-sim`; it organizes and validates runs around it.
- The project is designed for Perlmutter-style Python 3.11 + venv usage.
- For Jupyter, it is best to register the venv as a notebook kernel so the interpreter matches the terminal environment.
