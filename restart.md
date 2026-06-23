# Restart Notes

Use this file to resume the `sim2spec` bootcamp documentation work.

## Current goal

The repository is being shaped into a beginner-friendly DOE HPC Bootcamp project for new HPC users. The project now has:

- a top-level `README.md` overview
- five separate daily terminal guides:
  - `Project_1_ReadMe.md`
  - `Project_2_ReadMe.md`
  - `Project_3_ReadMe.md`
  - `Project_4_ReadMe.md`
  - `Project_5_ReadMe.md`
- a Jupyter notebook path:
  - `JNotebook/sim2spec_perlmutter_bootcamp.ipynb`

The intended participant message is:

> There are two ways to follow the project: terminal guides or the notebook. Both run the same workflow and produce the same outputs. Choose one path unless a mentor asks you to switch.

## What changed today

### Overall structure

- Removed the old single `ProjectReadMe.md` approach.
- Split the project into five daily readmes.
- Updated `README.md` to act as the main project overview and index.
- Added `DOE_HPC_Bootcamp_2026` at the top of `README.md`.
- Added the NERSC Projects for DOE Bootcamp link:
  - https://www.alcf.anl.gov/events/argonne-introduction-hpc-bootcamp
- Added `Before you begin` before the basic workflow examples.
- Added project references/resources in `README.md`, including NERSC, DUNE, `larnd-sim`, `2x2_sim`, Python, Numba, CUDA, CuPy, h5py, Matplotlib, Slurm, and Nsight Systems.

### Day 1: `Project_1_ReadMe.md`

Added beginner-friendly background before commands:

- What HPC is.
- What Perlmutter is.
- Login node vs compute node.
- What Slurm is.
- What `salloc`, `sbatch`, and `srun` do.
- What `$PSCRATCH` is.
- What a Python virtual environment is.
- What CUDA, GPU, CuPy, and `larnd-sim` are.
- CPU vs GPU explanation.
- Basic Linux commands table.
- Common Slurm commands table, including:

```bash
sacct -j <JOBID> --format=JobID,JobName,NTasks,NNodes,Elapsed,TotalCPU
```

Added visual:

- `assets/cpu_vs_gpu.png`

### Day 2: `Project_2_ReadMe.md`

Added beginner physics and output-validation context:

- What a neutrino is.
- What DUNE is.
- Short DUNE collaboration and detector summary.
- DUNE physics goals.
- What HDF5 is.
- What detector simulation output is.
- What packets, ADC, timestamps, segments, and waveforms are.
- What QA means.
- Why validation plots are useful.
- What a manifest is.

Added visuals:

- `assets/standard_model_particles.png`
- `assets/dune_long_baseline.png`
- Day 2 example plot images:
  - `assets/day2_adc_hist.png`
  - `assets/day2_timestamp_hist.png`
  - `assets/day2_plot_charge_vs_time.png`
  - `assets/day2_plot_hits_per_event.png`
  - `assets/day2_light_wvfm0.png`
  - `assets/day2_plot_single_waveform.png`

Updated validation plot workflow so plots are saved into:

```bash
$OUTBASE/day2_baseline/run/validation_plots
```

Removed the old “Alternatively: You can also produce the plots step-by-step” style section.

### Day 3: `Project_3_ReadMe.md`

Added beginner explanation for:

- parameter sweeps
- variants
- random seeds
- stochastic simulations
- provenance
- manifests
- CSV comparison tables
- why reproducibility matters in HPC

The Day 3 workflow now uses the current `day3_sweep` naming.

### Day 4: `Project_4_ReadMe.md`

Added beginner profiling context:

- what profiling is
- wall time vs GPU time
- kernels
- memory transfers
- GPU occupancy
- Nsight Systems
- TPB / threads per block
- why changing TPB can affect performance
- performance improvement vs reproducibility improvement

Added visual:

- `assets/day4_nsight_systems_timeline.png`

Commented out the Nsight Compute summary view section instead of deleting it. The asset remains:

- `assets/day4_nsight_compute_summary.png`

Updated Day 4 instructions so students do not rely on a brittle line number. Instead of “go to line 1280,” it now says to search for:

```python
TPB = 4
```

and change it to:

```python
TPB = 128
```

Updated `scripts/sbatch_day4_profile_compare.sh` with the same search-based TPB instruction.

Added practical Nsight Systems note:

- Install NVIDIA Nsight Systems on a local laptop.
- Download the `.nsys-rep` file from Perlmutter.
- Open the `.nsys-rep` locally for the GUI timeline view.

Expected reports:

```text
runs/day4_profile_baseline/run/nsys_report.nsys-rep
runs/day4_profile_compare/run/nsys_report.nsys-rep
```

### Day 5: `Project_5_ReadMe.md`

Added minimal consistency improvements:

- clearer title
- short intro
- `What you will learn`
- `Big picture`
- final story diagram
- what makes a good final project summary
- evidence checklist
- suggested presentation template
- final artifact checklist

Kept Day 5 intentionally lightweight.

### Notebook updates made

`JNotebook/sim2spec_perlmutter_bootcamp.ipynb` was updated to avoid drift:

- It now refers to `Project_1_ReadMe.md` through `Project_5_ReadMe.md`.
- Removed old `ProjectReadMe.md` wording.
- Updated Day 4 TPB instruction to search for `TPB = 4` instead of using line 1280.
- Updated the final notebook checklist wording to match Day 5.
- Made the notebook role explicit: terminal path or notebook path, both producing the same core outputs.
- Removed the terminal `salloc` example from the notebook `Before You Begin` section to avoid confusing notebook users.
- Added inline Day 2 plotting cells that read `output.h5`, display the plots in Jupyter, and save the PNG files under `validation_plots`.
- Moved the notebook into `JNotebook/`.
- The notebook JSON was validated with:

```bash
python -m json.tool JNotebook/sim2spec_perlmutter_bootcamp.ipynb >/dev/null
```

## Consistency checks already run

These checks passed:

```bash
git diff --check
python -m json.tool JNotebook/sim2spec_perlmutter_bootcamp.ipynb >/dev/null
```

Scans were run for stale references such as:

- `ProjectReadMe`
- `day3_baseline`
- `<YOUR_ACCOUNT>`
- `line 1280`
- old duplicate headings

No important stale references remained in the readmes/scripts after cleanup.

## Current notebook status

`JNotebook/sim2spec_perlmutter_bootcamp.ipynb` has been audited and updated.

### Recommended role for each document

- `README.md`: top-level project overview and path chooser.
- `Project_N_ReadMe.md`: detailed terminal workflow for each day.
- `JNotebook/sim2spec_perlmutter_bootcamp.ipynb`: executable JupyterHub workflow for students who prefer notebooks.

Important: the notebook should not duplicate every explanation from the daily readmes. It should be shorter and executable, with links/callouts to the readmes for deeper background.

### Notebook structure target

Use this structure:

```text
# DOE HPC Bootcamp 2026: sim2spec on Perlmutter

## Choose your path
## Before you begin
## Day 1: Setup and smoke test
## Day 2: Baseline, QA, and validation plots
## Day 3: Sweeps and provenance
## Day 4: Profiling
## Day 5: Final comparison and summary
```

Each day should have:

- short goal
- what students will run
- key outputs
- executable cells
- quick sanity check
- “what to show” summary

### Notebook work completed

1. Audited the current notebook top to bottom.
2. Compared each notebook section against the matching `Project_N_ReadMe.md`.
3. Made the notebook role explicit: notebook path vs terminal path.
4. Kept beginner explanations short and pointed to readmes for details.
5. Standardized account handling.
6. Standardized Jupyter GPU execution pattern:
   - setup/check cells can run directly
   - GPU simulation cells should use `srun` unless already on a compute node
7. Updated Day 1 notebook cells:
   - clone/setup
   - environment creation
   - dependency checks
   - smoke test
   - QA check
8. Updated Day 2 notebook cells:
   - baseline run
   - QA
   - manifest/metrics inspection
   - JSON-to-CSV conversion
   - inline validation plot generation, display, and save cells
9. Updated Day 3 notebook cells:
   - sweep run
   - manifest discovery
   - metrics comparison
   - `comparison.csv` creation/display
10. Updated Day 4 notebook cells:
   - baseline profiling
   - TPB change instruction
   - comparison profiling
   - `nsys_stats.json` inspection
   - local Nsight Systems `.nsys-rep` note
11. Updated Day 5 notebook cells:
   - baseline vs sweep comparison
   - artifact discovery
   - final artifact checklist
   - short presentation template
12. Validated:
   - notebook JSON parses
   - `git diff --check`
   - no stale `ProjectReadMe.md`
   - no stale `day3_baseline`
   - no brittle `line 1280`
   - all paths match the current daily readmes

## Important consistency choices

- Keep `<your_account>` in markdown terminal commands.
- In notebook cells, decide whether to use:

```bash
export ACCOUNT=<your_account>
```

or a clearly marked placeholder/default.

- Keep `00:30:00` for shorter Day 1/Day 2 interactive examples.
- Keep `00:60:00` where the user explicitly wanted it preserved in terminal readmes.
- Existing notebook `srun` cells may use `01:00:00`; review tomorrow for consistency with the notebook execution style.

## Git state reminder

Before committing or pushing, check:

```bash
git status --short
git diff --check
python -m json.tool JNotebook/sim2spec_perlmutter_bootcamp.ipynb >/dev/null
```

Current work includes new daily readmes, assets, README updates, notebook updates, `.gitignore` changes, and deletion of `ProjectReadMe.md`.
