# sim2spec

`sim2spec` is a lightweight workflow wrapper around [DUNE/larnd-sim](https://github.com/DUNE/larnd-sim) for running, validating, comparing, and profiling GPU-based detector simulations on Perlmutter.

This repository is designed for students who are new to HPC workflows and want a structured way to:
- install and run a GPU simulation workflow,
- generate QA summaries and plots,
- compare multiple run configurations,
- track provenance and reproducibility,
- and profile performance on Perlmutter (A100 -GPU).

This project does **not** replace `larnd-sim`. Instead, it organizes the workflow around it.

## Repository guides

- [ProjectReadMe.md](ProjectReadMe.md) — student-facing day-by-day guide (terminal workflow)
- [sim2spec_perlmutter_bootcamp.ipynb](sim2spec_perlmutter_bootcamp.ipynb) — interactive notebook for notebook users

## Quick start

### 1. Set up the environment

```bash
source setup.sh
bash install.sh
```

### 2. Activate the virtual environment

```bash
source setup.sh
source "$venv_name/bin/activate"
```

### 3. Quick environment check

Run these checks before trying a real workflow step:

```bash
python -c "import fire; print('fire ok')"
python -c "import cupy as cp; print(int(cp.arange(10).sum()))"
python -c "import larndsim; print('larndsim ok')"
```

If these work, your Python environment is in good shape.

## Basic workflow examples

### Baseline run

```bash
export WORKDIR=$PWD
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs

mkdir -p "$OUTBASE"

sim2spec run   --larndsim-dir "$LARNDSIM_DIR"   --config 2x2   --input "$INPUT_H5"   --outdir "$OUTBASE/day2_baseline"   --n-events 5
```

### QA on an existing run

```bash
sim2spec qa --run-dir "$OUTBASE/day2_baseline/run"
```

### Sweep run

```bash
sim2spec sweep   --larndsim-dir "$LARNDSIM_DIR"   --config 2x2   --input "$INPUT_H5"   --outdir "$OUTBASE/day4_sweep"   --sweep "$WORKDIR/configs/sweep.yaml"   --n-events 5
```

### Profiling run

```bash
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1

sim2spec run   --larndsim-dir "$LARNDSIM_DIR"   --config 2x2   --input "$INPUT_H5"   --outdir "$OUTBASE/day5_profile_baseline"   --n-events 10   --profiler nsys

sim2spec profile --run-dir "$OUTBASE/day5_profile_baseline/run"
```

## Prefer batch jobs?

Every GPU step also has a corresponding sbatch script in `scripts/`. For example:

```bash
sbatch scripts/sbatch_day1_smoke.sh
sbatch scripts/sbatch_day2_baseline.sh
sbatch scripts/sbatch_day4_sweep.sh
sbatch scripts/sbatch_day5_profile_baseline.sh
sbatch scripts/sbatch_day5_profile_compare.sh
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
- it helps answer the question: “does this run look reasonable?”

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

### [`scripts/`](scripts/)

This folder contains the student-facing sbatch submission scripts, one per day that requires GPU compute.

Contents:
- `sbatch_day1_smoke.sh` — smoke test (1 event)
- `sbatch_day2_baseline.sh` — baseline run (5 events)
- `sbatch_day4_sweep.sh` — parameter sweep (3 events per variant)
- `sbatch_day5_profile_baseline.sh` — profiling baseline (10 events, nsys)
- `sbatch_day5_profile_compare.sh` — profiling comparison (10 events, nsys, TPB=128)

Why it matters:
- students who prefer batch submission over interactive nodes can use these directly
- each script includes a GPU pre-flight check and structured output directories

---

### [`setup.sh`](setup.sh)

This is the lightweight environment setup script.

It follows the style of `setup.inc.sh` from `larnd-sim-example`.

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

It follows the style of `install_larnd_sim.sh` from `larnd-sim-example`.

What it does:
- creates a virtual environment
- installs Python dependencies
- installs `sim2spec`
- clones and installs `larnd-sim` (skips clone if already present)

Why it matters:
- this is the easiest way for terminal users to get started without following the full notebook

---

### [`README.md`](README.md)

This file is the top-level overview of the repository.

Why it matters:
- it gives a quick map of the project
- it points students to the detailed guides and notebooks

---

### [`ProjectReadMe.md`](ProjectReadMe.md)

This is the student-facing project guide.

What it contains:
- a short summary of what students will learn
- a note about NERSC compute allocation
- a day-by-day breakdown
- guided instructions for students to attempt on their own

Why it matters:
- this is the main file students should read first

### [`sim2spec_perlmutter_bootcamp.ipynb`](sim2spec_perlmutter_bootcamp.ipynb)

The main student-facing notebook. Mirrors `ProjectReadMe.md` day by day with executable cells, live run outputs, and `srun`-based GPU dispatch so students can run everything from inside JupyterHub.

Why it matters:
- the recommended path for students who prefer notebooks over the terminal
- includes real Perlmutter output examples so students know what to expect

---

### [`plot_validation.py`](plot_validation.py)

Standalone script for producing validation plots directly from an output HDF5 file.

```bash
python plot_validation.py "$OUTBASE/day2_baseline/run/output.h5" --outdir "$OUTBASE/day3_baseline/run"
```

Why it matters:
- a quick way to visualise any run output without running the full QA pipeline

## Suggested reading order

If you are new to the repository, a good order is:

1. [ProjectReadMe.md](ProjectReadMe.md)
2. [README.md](README.md)
3. [sim2spec_perlmutter_bootcamp.ipynb](sim2spec_perlmutter_bootcamp.ipynb) — if you prefer notebooks
4. [src/cli.py](src/cli.py)
5. [src/runner.py](src/runner.py)
6. [src/qa.py](src/qa.py)
7. [src/provenance.py](src/provenance.py)
8. [configs/sweep.yaml](configs/sweep.yaml)

## Notes

- This wrapper does not replace `larnd-sim`; it organizes and validates runs around it.
- The project is designed for Perlmutter-style Python 3.11 + venv usage.
- For Jupyter, it is best to register the venv as a notebook kernel so the interpreter matches the terminal environment.
