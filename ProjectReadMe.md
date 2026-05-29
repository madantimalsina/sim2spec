# Project: sim2spec

## What you will learn

By working through this project, you will learn how to build and use a reproducible GPU workflow on Perlmutter using a real detector simulation pipeline. You will practice environment setup, baseline execution, QA, parameter sweeps, provenance tracking, and profiling.

## Before you begin

You will need a NERSC compute allocation and access to Perlmutter. For GPU work, request an interactive node or submit a batch job before running simulations.

```bash
salloc -C gpu -q interactive -t 00:30:00 -A <your_account> --gpus=1 --ntasks=1 --cpus-per-task=8
```

See [`README.md`](README.md) for the repo overview.

# Day 1 — Environment setup, install, and smoke test

Day 1 focuses on getting the full software stack working on Perlmutter. The goal is not yet to do detector analysis, but to make sure the workflow is reproducible and the dependencies are correct. By the end of this day, you should have a working GPU-enabled Python environment, `larnd-sim` installed from source, `sim2spec` installed as a wrapper workflow, and a minimal smoke test that confirms the end-to-end path is functional.

```bash
# Day 1 environment block
```

```bash
# Set up the working area and clone the repo
export MYWORKDIR=$PSCRATCH/HPC_intro
mkdir -p "$MYWORKDIR"
cd "$MYWORKDIR"

# Clone the project from GitHub
git clone https://github.com/madantimalsina/sim2spec.git
cd sim2spec
pwd
```

```bash
# Set up the environment (Install and creat python virtual environment)
source setup.sh
bash install.sh
```

```bash
# Validate the Python environment and the main dependencies
source setup.sh
source "$venv_name/bin/activate"

python -c "import fire; print('fire ok')"
python -c "import cupy as cp; print(int(cp.arange(10).sum()))"
```

```bash
# Validate larnd-sim install
python -c "import larndsim; print('larndsim ok')"
# python "$WORKDIR/larnd-sim/cli/simulate_pixels.py" --help | head
```

```bash
# Smoke test run
# This is a very small end-to-end test to make sure the workflow runs.
export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs
mkdir -p "$OUTBASE"

# NOTE: You will need a NERSC compute allocation and access to Perlmutter.
# For GPU work, request an interactive node or submit a batch job before running simulations.
salloc -C gpu -q interactive -t 00:30:00 -A <YOUR_ACCOUNT>


sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day1_smoke" \
  --n-events 1

sim2spec qa --run-dir "$OUTBASE/day1_smoke/run"
```

> **Alternatively**, if you prefer to submit the smoke test as a batch job instead of running it interactively, you can use the provided sbatch script. Make sure to replace `<your_account>` with your NERSC project account, then submit with:
>
> ```bash
> sbatch scripts/sbatch_day1_smoke.sh
> ```
>
> Outputs will be written to `$OUTBASE/day1_smoke_sbatch/run` and job logs will appear as `day1_smoke_<jobid>.out` / `.err` in the directory where you submitted the job.

```bash
# Check smoke test outputs
ls -R "$OUTBASE/day1_smoke/run"
cat "$OUTBASE/day1_smoke/run/qa/metrics.json" | head
```

### What to show on Day 1

- `python -c "import cupy..."` returning `45`
- `sim2spec --help`
- `simulate_pixels.py --help`
- optional smoke-test output and `qa/metrics.json`

### Achieved by end of Day 1

- GPU environment is working
- CUDA and CuPy are correctly installed
- `larnd-sim` and `sim2spec` are installed
- optional first smoke test completes

# Day 2 — Baseline run and first output validation

Day 2 establishes the first stable baseline simulation. The objective is to confirm that the pipeline works end to end, starting from the input HDF5 file and producing the expected output artifacts. After the run completes, the baseline output is checked with the QA tools so that participants can inspect packet counts, timing behavior, ADC-related summaries, and available plots. This creates the reference run that the rest of the project will build on.

```bash
# Day 2 environment block and baseline run

export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs

cd $WORKDIR
pwd

source setup.sh
source "$venv_name/bin/activate"

# NOTE: You will need a NERSC compute allocation and access to Perlmutter.
# For GPU work, request an interactive node or submit a batch job before running simulations.
salloc -C gpu -q interactive -t 00:30:00 -A <YOUR_ACCOUNT>

sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day2_baseline" \
  --n-events 5
```


> **Alternatively**, if you prefer to submit the baseline run as a batch job instead of running it interactively, you can use the provided sbatch script. Make sure to replace `<your_account>` with your NERSC project account, then submit with:
>
> ```bash
> sbatch scripts/sbatch_day2_baseline.sh
> ```
>
> Outputs will be written to `$OUTBASE/day2_baseline_sbatch/run` and job logs will appear as `day2_baseline_<jobid>.out` / `.err` in the directory where you submitted the job.

```bash
# Inspect the run directory
ls -R "$OUTBASE/day2_baseline/run"
```

```bash
# Run QA on the baseline
sim2spec qa --run-dir "$OUTBASE/day2_baseline/run"
```

```bash
# Inspect the manifest and QA metrics
cat "$OUTBASE/day2_baseline/run/manifest.json"
echo
cat "$OUTBASE/day2_baseline/run/qa/metrics.json"
```

```bash
## Save QA metrics from JSON to CSV for easy inspection/comparison (optional: for FUN!)
python - <<'PY'
import json, os, csv
path = os.environ["OUTBASE"] + "/day2_baseline/run/qa/metrics.json"
out  = os.environ["OUTBASE"] + "/day2_baseline/run/qa/metrics.csv"
d = json.load(open(path))
keys = sorted(d)
with open(out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerow(d)
print(f"Saved to {out}")
PY
```

```bash
# List QA files
find "$OUTBASE/day2_baseline/run/qa" -maxdepth 1 -type f
```

### What to compare and analyze

- Does `output.h5` exist?
- Is `n_packets` nonzero?
- Are ADC statistics present?
- Are timestamp ranges present?
- Are QA plots created?

### What to show on Day 2

- baseline run directory
- `manifest.json`
- `metrics.json`
- QA PNG files

### Achieved by end of Day 2

- baseline run is successful
- QA is generating metrics and plots
- a stable reference output exists

# Day 3 — From Simulation Output to Physical Interpretation

Day 3 is about turning the baseline output into something interpretable through visualization. This means reading the output file directly, producing validation plots, and interpreting what the charge deposits, hit distributions, and light waveforms are telling you about the simulation. By the end of the day, the baseline is a well-understood reference for later comparison.

```bash
# Re-run QA if needed (Day 2)
export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export OUTBASE=$WORKDIR/runs

cd $WORKDIR
pwd

source setup.sh
source "$venv_name/bin/activate"

# Run QA on the baseline (from day 2 to see the output.h5 file exists)
sim2spec qa --run-dir "$OUTBASE/day2_baseline/run"

# Save plots into day3 (new folder)
export OUTPLOTS="$OUTBASE/day3_baseline/run"
mkdir -p "$OUTPLOTS"
```

```bash

# Plot 1 — Charge vs. time
python - <<'PY'
import h5py, numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt

path    = os.path.join(os.environ["OUTBASE"], "day2_baseline", "run", "output.h5")
out_dir = os.environ["OUTPLOTS"]

with h5py.File(path, "r") as f:
    p = f["packets"][:]
    fig, ax = plt.subplots(figsize=(8,4))
    ax.scatter(p["timestamp"].astype(float), p["dataword"].astype(float), s=2, alpha=0.4, color="steelblue")
    ax.set_xlabel("Timestamp [ticks]"); ax.set_ylabel("Charge [ADC counts]")
    ax.set_title("Charge vs. Time"); fig.tight_layout()
    fig.savefig(f"{out_dir}/plot_charge_vs_time.png", dpi=150)
print("Saved: plot_charge_vs_time.png")
PY
```

```bash
# Plot 2 — Hits per event
python - <<'PY'
import h5py, numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt

path    = os.path.join(os.environ["OUTBASE"], "day2_baseline", "run", "output.h5")
out_dir = os.environ["OUTPLOTS"]

with h5py.File(path, "r") as f:
    seg = f["segments"][:]
    u, cnt = np.unique(seg["event_id"], return_counts=True)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(u, cnt, width=0.6, color="darkorange", alpha=0.85)
    ax.set_xlabel("Event ID"); ax.set_ylabel("Number of Segments (Hits)")
    ax.set_title("Hits per Event"); fig.tight_layout()
    fig.savefig(f"{out_dir}/plot_hits_per_event.png", dpi=150)
print("Saved: plot_hits_per_event.png")
PY
```

```bash
# Plot 3 — Single waveform  (5 triggers, 384 channels, 1000 samples)
python - <<'PY'
import h5py, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt

path    = os.path.join(os.environ["OUTBASE"], "day2_baseline", "run", "output.h5")
out_dir = os.environ["OUTPLOTS"]

with h5py.File(path, "r") as f:
    wvfm = f["light_wvfm"][0, 0, :]   # trigger 0, channel 0, 1000 samples
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(wvfm, color="mediumseagreen", lw=1)
    ax.set_xlabel("Sample index"); ax.set_ylabel("ADC counts")
    ax.set_title("Single Light Waveform (trigger 0, channel 0)"); fig.tight_layout()
    fig.savefig(f"{out_dir}/plot_single_waveform.png", dpi=150)
print("Saved: plot_single_waveform.png")
PY
```
#### You also produce the plot directly 
```bash
python plot_validation.py \
  "$OUTBASE/day2_baseline/run/output.h5" \
  --outdir "$OUTBASE/day3_baseline/run"
```
### What to compare and analyze

- **Charge vs. Time** — packets cluster at discrete timestamps (~0, 2, 4, 6, 8 × 10⁷ ticks) corresponding to individual neutrino events, with charge values mostly between 25–100 ADC and one outlier near 255 ADC
- **Hits per Event** — event activity is highly uneven; event 1 dominates with ~3600 segments while events 0, 3, and 4 are much smaller, reflecting varying complexity of neutrino interactions
- **Single Light Waveform** — noise-like fluctuations centered around 0 ADC (±20–30 counts) with one clear photon signal spike near sample 850 reaching ~52 ADC above the noise floor

### What to show on Day 3

- `plot_charge_vs_time.png` — charge deposits clustered by event time
- `plot_hits_per_event.png` — segment count per event showing interaction complexity
- `plot_single_waveform.png` — light signal with noise floor and photon spike visible

### Achieved by end of Day 3

- output file read and explored directly using Python and h5py
- three validation plots produced and physically interpreted
- charge clustering by event time identified and understood
- hit count variation across events connected to neutrino interaction physics
- light waveform noise floor and signal spike identified
- baseline fully characterized and ready for parameter variation studies in later days

# Day 4 — Parameter sweeps and provenance tracking

Day 4 expands the workflow from a single run into a controlled set of variants. Four runs are executed using the same pipeline, each with a different random seed (`base_seed + variant_index`). Because the simulation has stochastic components, each variant will produce slightly different outputs — different packet counts, ADC distributions, and light yields. Each run is packaged with provenance information such as the seed used, environment settings, and code version. The main goal is to make result comparison systematic and reproducible.

> **Note:** Each variant in `configs/sweep.yaml` uses an explicitly different random seed (42, 1337, 55555, 99999), so participants will see clear differences in packet counts and ADC distributions across the four runs in `comparison.csv`.

```bash
# Run a sweep
export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs

cd $WORKDIR
pwd

source setup.sh
source "$venv_name/bin/activate"

# NOTE: You will need a NERSC compute allocation and access to Perlmutter.
# For GPU work, request an interactive node or submit a batch job before running simulations.
salloc -C gpu -q interactive -t 00:60:00 -A <YOUR_ACCOUNT>


sim2spec sweep \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day4_sweep" \
  --sweep "$WORKDIR/configs/sweep.yaml" \
  --n-events 3
```

> **Alternatively**, if you prefer to submit the sweep as a batch job instead of running it interactively, you can use the provided sbatch script. Make sure to replace `<your_account>` with your NERSC project account, then submit with:
>
> ```bash
> sbatch scripts/sbatch_day4_sweep.sh
> ```
>
> Outputs will be written to `$OUTBASE/day4_sweep_sbatch/` and job logs will appear as `day4_sweep_<jobid>.out` / `.err` in the directory where you submitted the job. Update the root path in the comparison scripts below accordingly.

```bash
#Inspect run directories
ls "$OUTBASE/day4_sweep"
find "$OUTBASE/day4_sweep" -maxdepth 2 -name manifest.json
find "$OUTBASE/day4_sweep" -maxdepth 3 -name metrics.json
```

```bash
# Compare variant metrics
python - <<'PY'
import glob, json, os
root = os.environ["OUTBASE"] + "/day4_sweep"
rows = []
for mpath in sorted(glob.glob(root + "/*/qa/metrics.json")):
    d = json.load(open(mpath))
    variant = mpath.split("/")[-3]
    rows.append({
        "variant": variant,
        "n_packets": d.get("n_packets"),
        "adc_mean": d.get("adc_mean", d.get("adc_mean_guess")),
        "adc_std": d.get("adc_std", d.get("adc_std_guess")),
        "n_light_wvfm": d.get("n_light_wvfm"),
    })

for r in rows:
    print(r)
PY
```

```bash
# Extract provenance from manifests
python - <<'PY'
import glob, json, os
root = os.environ["OUTBASE"] + "/day4_sweep"
for mpath in sorted(glob.glob(root + "/*/manifest.json")):
    d = json.load(open(mpath))
    print("RUN:", mpath.split("/")[-2])
    print("  config:", d["larndsim"]["config"])
    print("  seed:", d["sim"]["rand_seed"])
    print("  n_events:", d["sim"]["n_events"])
    print("  git_commit:", d["larndsim"]["git"].get("commit"))
    print("  env:", d.get("env_applied"))
    print("  patch:", d.get("patch"))
PY
```

```bash
# Save comparison CSV
python - <<'PY'
import glob, json, os, csv

root = os.environ["OUTBASE"] + "/day4_sweep"
out  = root + "/comparison.csv"

rows = []
for mpath in sorted(glob.glob(root + "/*/qa/metrics.json")):
    variant  = mpath.split("/")[-3]
    run_dir  = os.path.dirname(os.path.dirname(mpath))
    mani     = os.path.join(run_dir, "manifest.json")

    d = json.load(open(mpath))
    m = json.load(open(mani)) if os.path.exists(mani) else {}

    larndsim = m.get("larndsim", {})
    sim      = m.get("sim", {})
    patch    = m.get("patch", {})

    rows.append({
        "variant"      : variant,
        "config"       : larndsim.get("config"),
        "seed"         : sim.get("rand_seed"),
        "n_events"     : sim.get("n_events"),
        "git_commit"   : larndsim.get("git", {}).get("commit"),
        "patch"        : str(patch),
        "n_packets"    : d.get("n_packets"),
        "adc_mean"     : d.get("adc_mean",    d.get("adc_mean_guess")),
        "adc_std"      : d.get("adc_std",     d.get("adc_std_guess")),
        "n_light_wvfm" : d.get("n_light_wvfm"),
    })

fields = ["variant", "config", "seed", "n_events", "git_commit", "patch",
          "n_packets", "adc_mean", "adc_std", "n_light_wvfm"]

with open(out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved: {out}")
PY
```

### What to compare and analyze

- packet counts across variants
- ADC mean and spread across variants
- whether any run is unexpectedly empty
- whether provenance is recorded consistently

### What to show on Day 4

- directory tree with multiple runs
- one `manifest.json`
- `comparison.csv`

### Achieved by end of Day 4

- multiple controlled runs are executed
- run metadata is captured
- outputs can be compared systematically

# Day 5 — Profiling and one measurable improvement

Day 5 adds observability and performance analysis to the workflow. Instead of just running the simulation, the goal is to understand how it behaves on the GPU and where time is being spent. Profiling a baseline run and one comparison run provides evidence that can support either a performance improvement or a reproducibility improvement. The goal is not deep kernel optimization, but to demonstrate that the workflow can be measured, compared, and improved in a disciplined way.

```bash
# Profile the baseline run with nsys
export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export LARNDSIM_DIR=$WORKDIR/larnd-sim
export INPUT_H5=$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5
export HDF5_USE_FILE_LOCKING=0
export LARNDSIM_DISABLE_CUPY_MEMPOOL=1
export OUTBASE=$WORKDIR/runs

cd $WORKDIR
pwd

source setup.sh
source "$venv_name/bin/activate"

# NOTE: You will need a NERSC compute allocation and access to Perlmutter.
# For GPU work, request an interactive node or submit a batch job before running simulations.
salloc -C gpu -q interactive -t 00:60:00 -A <YOUR_ACCOUNT>


sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day5_profile_baseline" \
  --n-events 10 \
  --profiler nsys

```

> **Alternatively**, if you prefer to submit the baseline profile run as a batch job, you can use the provided sbatch script. Make sure to replace `<your_account>` with your NERSC project account, then submit with:
>
> ```bash
> sbatch scripts/sbatch_day5_profile_baseline.sh
> ```
>
> Outputs will be written to `$OUTBASE/day5_profile_baseline_sbatch/run` and job logs will appear as `day5_profile_baseline_<jobid>.out` / `.err` in the directory where you submitted the job. The profile summary is generated automatically at the end of the script.

```bash

# Write profile summary
sim2spec profile --run-dir "$OUTBASE/day5_profile_baseline/run"

# Inspect profiling artifacts
ls "$OUTBASE/day5_profile_baseline/run"
cat "$OUTBASE/day5_profile_baseline/run/profile/nsys_stats.json" | head -n 40
```

### Profile one comparison run

For the comparison profiling case, participants should modify the CUDA thread-block setting in the `larnd-sim` source before running the second profile. Open the file [`larnd-sim/cli/simulate_pixels.py`](larnd-sim/cli/simulate_pixels.py) and go to **line 1280**, where the code currently sets:

```bash
TPB = 4
```
Change it to:

```bash
TPB = 128
```
Then rerun the profiling command for the comparison case. This gives a simple example of how changing a GPU execution parameter can affect runtime behavior and profiling results.

> **Alternatively**, if you prefer to submit the comparison profile run as a batch job, make sure you have applied the TPB change above first, then submit with:
>
> ```bash
> sbatch scripts/sbatch_day5_profile_compare.sh
> ```
>
> Outputs will be written to `$OUTBASE/day5_profile_compare_sbatch/run` and job logs will appear as `day5_profile_compare_<jobid>.out` / `.err` in the directory where you submitted the job. The profile summary is generated automatically at the end of the script.

```bash

sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day5_profile_compare" \
  --n-events 10 \
  --profiler nsys

# Write profile summary
sim2spec profile --run-dir "$OUTBASE/day5_profile_compare/run"
```

```bash
#Compare approximate wall time and output file size using file timestamps

python - <<'PY'
import os

base = os.environ["OUTBASE"]
runs = ["day5_profile_baseline", "day5_profile_compare"]

print("=== Run-level comparison ===")
for name in runs:
    run = f"{base}/{name}/run"
    manifest = f"{run}/manifest.json"
    output = f"{run}/output.h5"

    print(f"\n{name}")

    if os.path.exists(manifest) and os.path.exists(output):
        mt_manifest = os.path.getmtime(manifest)
        mt_output = os.path.getmtime(output)
        print("  approx_wall_seconds:", round(mt_output - mt_manifest, 2))
        print("  output_size_MB:", round(os.path.getsize(output) / (1024 * 1024), 2))
    else:
        print("  missing manifest or output.h5")
PY
```

```bash

# More Compare profiling test (Optional)
# Optional reproducibility improvement
mkdir -p "$OUTBASE/day5_profile_baseline/run/system_info"
mkdir -p "$OUTBASE/day5_profile_compare/run/system_info"

nvidia-smi -L | tee "$OUTBASE/day5_profile_baseline/run/system_info/gpu_list.txt"
nvidia-smi -L | tee "$OUTBASE/day5_profile_compare/run/system_info/gpu_list.txt"
```

### What to compare and analyze

- existence of profiling report files
- approximate baseline versus comparison runtime
- output file size for the baseline and comparison runs
- whether the code change or runtime setting affects performance behavior
- whether enough runtime environment information is captured for reproducibility

### What to show on Day 5

- `nsys_report*.nsys-rep`
- `profile/nsys_stats.json`
- a small comparison summary such as:
  - `approx_wall_seconds`
  - `output_size_MB`
- optional `system_info/` files

### Achieved by end of Day 5

- the workflow is profiled
- baseline and comparison runs are measured side by side
- one practical code or workflow change is evaluated
- one performance or reproducibility improvement is documented

### BEFORE YOU GO:
The profiling step in this project uses summary outputs such as `nsys stats`, but participants who want a more detailed visual view of GPU activity can also inspect the `.nsys-rep` files using **NVIDIA Nsight Systems**. In particular, the timeline view can be helpful for understanding kernel launches, memory transfers, and overall runtime behavior. Nsight Systems can be downloaded from [NVIDIA Nsight Systems – Get Started](https://developer.nvidia.com/nsight-systems/get-started).

For this project, the profiling reports are expected at:

- `runs/day5_profile_baseline/run/nsys_report.nsys-rep`
- `runs/day5_profile_compare/run/nsys_report.nsys-rep`

# Final cross-day comparison and summary

This final section pulls together the most important outputs from the whole bootcamp: baseline results, sweep comparisons, and profiling artifacts. It is useful for preparing the final presentation or for creating a compact end-of-bootcamp artifact bundle.

```bash
# Compare baseline vs sweep
export WORKDIR=$PSCRATCH/HPC_intro/sim2spec
export HDF5_USE_FILE_LOCKING=0
export OUTBASE=$WORKDIR/runs

source setup.sh
source "$venv_name/bin/activate"

python - <<'PY'
import os, glob, json

base = os.environ["OUTBASE"]

groups = {
    "baseline": f"{base}/day2_baseline/run/qa/metrics.json",
    "day4_sweep": f"{base}/day4_sweep/*/qa/metrics.json",
}

print("=== BASELINE ===")
p = groups["baseline"]
if os.path.exists(p):
    d = json.load(open(p))
    print("baseline", d.get("n_packets"), d.get("adc_mean", d.get("adc_mean_guess")))

print("\n=== DAY 4 SWEEP ===")
for p in sorted(glob.glob(groups["day4_sweep"])):
    d = json.load(open(p))
    print(p.split("/")[-3], d.get("n_packets"), d.get("adc_mean", d.get("adc_mean_guess")))
PY
```

```bash
# Collect final presentation artifacts
find "$OUTBASE" -maxdepth 4 \( -name "metrics.json" -o -name "manifest.json" -o -name "*.png" -o -name "nsys_stats.json" \) | sort
```

## Suggested final presentation structure

1. Day 1: environment and install validated  
2. Day 2–3: baseline output and QA sanity  
3. Day 4: controlled sweep and reproducibility  
4. Day 5: profiling and measurable improvement
