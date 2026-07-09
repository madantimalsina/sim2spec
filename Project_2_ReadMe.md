# Project 2: Baseline run and first output validation

Day 2 establishes the first stable baseline simulation and turns it into an interpretable reference run. The objective is to confirm that the pipeline works end to end, starting from the input HDF5 file and producing the expected output artifacts. After the run completes, QA checks summarize packet counts, timing behavior, ADC-related quantities, and basic output plots. The validation plotting helper then reads `output.h5` directly and saves a small set of plots that connect those QA metrics to the physical interpretation of charge timing, event activity, and light-waveform behavior before moving on to parameter sweeps.

## What you will learn

- How to run the first stable baseline simulation.
- How to inspect the run directory, manifest, and QA metrics.
- How to save QA metrics in JSON and CSV formats.
- How to create baseline validation plots from `output.h5` using `plot_validation.py`.

## Physics context: neutrinos and DUNE

A **neutrino** is a very light, electrically neutral elementary particle. Neutrinos interact only rarely with matter, so experiments need intense beams, large detectors, and careful simulation to understand what detector signals should look like.

<img src="assets/standard_model_particles.png" alt="Standard Model of elementary particles with neutrinos" width="520">

Source: [Neutrino properties, IN2P3 neutrino history site](https://neutrino-history.in2p3.fr/neutrino-properties/).

**DUNE** is the Deep Underground Neutrino Experiment: an international, U.S.-hosted long-baseline neutrino experiment with more than 2000 scientists and engineers from over 200 institutions in 36 countries and 7 U.S. DOE national laboratories. DUNE will use an intense neutrino beam from Fermilab, a high-rate near detector, and massive liquid-argon far detector modules located nearly a mile underground in South Dakota.

<img src="assets/dune_long_baseline.png" alt="DUNE long-baseline neutrino experiment concept" width="680">

Source: DUNE long-baseline experiment concept, [arXiv:2002.02967](https://doi.org/10.48550/arXiv.2002.02967).

DUNE physics goals include:

- measuring CP violation in the lepton sector, connected to the question of why matter dominates over antimatter
- determining neutrino mass ordering and mixing parameters, which describe how neutrinos transform among flavors (`nu_e`, `nu_mu`, `nu_tau`)
- detecting neutrinos from supernovae
- searching for proton decay and physics beyond the Standard Model

## From simulation output to QA

Day 2 is where the simulation output becomes something you can inspect. The basic workflow is:

```mermaid
flowchart LR
    subgraph row1[" "]
        direction LR
        A[input HDF5] --> B[larnd-sim]
        B --> C[output.h5]
        C --> D[sim2spec QA]
        D --> E[metrics.json]
        D --> F[QA plots]
        C --> G[validation plots]
    end
```

## Key terms

- **Track:** the simulated path of a particle as it moves through the detector. A track shows where the particle traveled and is often broken into smaller segments for simulation.
- **Charge deposit:** the ionization charge left behind when a particle passes through the detector material. These deposits are the starting point for simulating the detector’s charge response.
- **Pixel:** a small readout element in the detector’s charge readout system. Pixels collect charge locally and help determine where the signal appeared in the detector.
- **Packet:** a unit of simulated detector readout data, similar to a digitized electronics record. A packet usually contains information such as channel or pixel ID, ADC value, and timing.
- **Waveform:** a time series of signal values, such as a light detector response or electronics signal sampled over time. Waveforms are useful for studying timing structure and detector response shape.
- **HDF5 file:** a file format designed for large structured datasets. In this project, both the input and simulation output are HDF5 files.
- **Detector simulation output:** the simulated detector response after particles pass through the detector model.
- **ADC:** analog-to-digital converter value; a digitized charge or signal amplitude.
- **Timestamp:** the simulated time associated with a packet or signal.
- **Segment:** a simulated piece of a particle trajectory or deposited energy in the detector.
- **QA:** quality assurance; quick checks that outputs exist and contain reasonable counts, ranges, and plots.
- **Validation plot:** a plot used to connect QA numbers to physical behavior, such as charge versus time or hits per event.
- **Manifest:** a JSON record of how a run was produced, including inputs, output path, configuration, seed, environment settings, and code provenance.

## Packet, timestamp, and ADC mental model

For the baseline output, imagine each packet as one row in a detector readout table:

| Packet field | Beginner meaning |
| --- | --- |
| `timestamp` | When the simulated signal happened. |
| `dataword` or `adc` | How large the digitized signal was. |
| packet count | How many detector readout records were produced. |

The charge vs time plot uses this idea directly: timestamp on one axis and charge-like ADC information on the other.

## Example plots

These are example outputs from the Day 2 QA and validation workflow. Your plots may differ slightly if the input, random seed, software version, or number of events changes.

### ADC histogram

<img src="assets/day2_adc_hist.png" alt="ADC histogram" width="420">

**ADC histogram:** shows the distribution of digitized signal amplitudes in the output packets. It helps you see whether most signals are small, whether there is a long high-signal tail, and whether the ADC values look reasonable overall.

### Timestamp histogram

<img src="assets/day2_timestamp_hist.png" alt="Timestamp histogram" width="420">

**Timestamp histogram:** shows when simulated packets occur in time. It is useful for checking whether the signal activity is concentrated in a narrow time window or spread across a broader range, and whether the timing distribution looks physically reasonable.

### Charge vs. time

<img src="assets/day2_plot_charge_vs_time.png" alt="Charge versus time validation plot" width="520">

**Charge vs. time:** shows how charge-related packet values change with timestamp. This helps connect the detector response to physical behavior by showing when charge arrives and how strong the signal is over time.

### Hits per event

<img src="assets/day2_plot_hits_per_event.png" alt="Hits per event validation plot" width="520">

**Hits per event:** shows how many detector hits or readout records appear in each event. It is useful for understanding event activity and for spotting events that look unusually empty or unusually busy.

### Light waveform QA

<img src="assets/day2_light_wvfm0.png" alt="Light waveform QA plot" width="420">

**Light waveform QA:** gives a quick quality-assurance view of light-detector waveform data. It helps confirm that light information exists, has the expected shape, and is not obviously empty or corrupted.

### Single light waveform

<img src="assets/day2_plot_single_waveform.png" alt="Single light waveform validation plot" width="520">

**Single light waveform:** shows one example waveform in detail as a time series. This is useful for understanding what an individual light signal looks like in the simulation and for checking its timing and shape more closely.

Source: example plots generated by the `sim2spec qa` and `plot_validation.py` workflows in this project.

## Resources

- [DUNE larnd-sim documentation](https://dune.github.io/larnd-sim/larndsim.html)
- [HDF5 documentation](https://support.hdfgroup.org/documentation/hdf5/latest/_u_g.html)
- [h5py documentation](https://docs.h5py.org/)
- [Matplotlib documentation](https://matplotlib.org/stable/)
- [Neutrino properties, IN2P3](https://neutrino-history.in2p3.fr/neutrino-properties/)
- [DUNE long-baseline neutrino experiment concept](https://doi.org/10.48550/arXiv.2002.02967)

## Exercise

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
```

```bash
# Validate the Python environment and the main dependencies
source setup.sh
source "$venv_name/bin/activate"
```

```bash
# NOTE: You will need a NERSC compute allocation and access to Perlmutter.
# For GPU work, request an interactive node or submit a batch job before running simulations.
salloc -C gpu -q interactive -t 00:20:00 -A <your_account> --gpus=1 --ntasks=1 --cpus-per-task=8
```

```bash
# run simulation workflow
sim2spec run \
  --larndsim-dir "$LARNDSIM_DIR" \
  --config 2x2 \
  --input "$INPUT_H5" \
  --outdir "$OUTBASE/day2_baseline" \
  --n-events 5
```


> **Alternatively:** Use [sim2spec_perlmutter_bootcamp.ipynb](JNotebook/sim2spec_perlmutter_bootcamp.ipynb), the interactive notebook for participants who prefer to complete the exercises in Jupyter instead of the terminal. Find the corresponding Project 2 (Day 2) section in the Jupyter notebook.
>
> **Extended/optional:** If you prefer to submit the baseline run as a batch job instead of running it interactively, you can use the provided sbatch script. Make sure to replace `<your_account>` with your NERSC project account, then submit with:
>
> ```bash
> sbatch scripts/sbatch_day2_baseline.sh
> ```
>
> Outputs will be written to `$OUTBASE/day2_baseline_sbatch/run`, QA metrics and QA plots will be generated automatically, and job logs will appear as `day2_baseline_<jobid>.out` / `.err` in the directory where you submitted the job.

> **Warning for reruns:** `larnd-sim` will not overwrite an existing `output.h5`. If you rerun the baseline with the same `--outdir` and see an error like `Output file ... already exists`, remove the old output file first or choose a new output directory:
>
> ```bash
> rm "$OUTBASE/day2_baseline/run/output.h5"
> ```

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
# Save QA metrics from JSON to CSV for easy inspection and comparison
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

### Baseline validation plots

Use the plotting helper to save the Day 2 validation plots.

```bash
# Save validation plots with the Day 2 baseline
export OUTPLOTS="$OUTBASE/day2_baseline/run/validation_plots"
mkdir -p "$OUTPLOTS"
```

```bash
python plot_validation.py \
  "$OUTBASE/day2_baseline/run/output.h5" \
  --outdir "$OUTPLOTS"
```

### Example output

Your absolute path, node name, timestamps, and exact counts may differ, but a successful five-event baseline should look similar to this.

```text
# Inspect the run directory
<compute-node>:sim2spec > ls -R "$OUTBASE/day2_baseline/run"
$OUTBASE/day2_baseline/run:
command.json  manifest.json  output.h5
```

```text
# Run QA on the baseline
<compute-node>:sim2spec > sim2spec qa --run-dir "$OUTBASE/day2_baseline/run"
{
  "metrics": {
    "file": "$OUTBASE/day2_baseline/run/output.h5",
    "datasets": [
      "_header",
      "configs",
      "light_dat",
      "light_trig",
      "light_wvfm",
      "light_wvfm_mc_assn",
      "mc_hdr",
      "mc_packets_assn",
      "mc_stack",
      "messages",
      "packets",
      "segments",
      "trajectories",
      "vertices"
    ],
    "n_packets": 7004,
    "n_mc_packets_assn": 7004,
    "n_light_wvfm": 5,
    "n_light_trig": 5,
    "n_light_dat": 4,
    "timestamp_min": 0,
    "timestamp_max": 10000000,
    "adc_min_guess": 0.0,
    "adc_max_guess": 255.0,
    "adc_mean_guess": 22.472872644203314,
    "adc_std_guess": 24.093075296481327
  },
  "plots": {
    "adc_hist": "$OUTBASE/day2_baseline/run/qa/adc_hist.png",
    "timestamp_hist": "$OUTBASE/day2_baseline/run/qa/timestamp_hist.png",
    "light_wvfm0": "$OUTBASE/day2_baseline/run/qa/light_wvfm0.png"
  }
}
```

```text
# Inspect the manifest and QA metrics
<compute-node>:sim2spec > cat "$OUTBASE/day2_baseline/run/manifest.json"
{
  "env_applied": {},
  "io": {
    "input": "$WORKDIR/input/MiniRun5_1E19_RHC.convert2h5.0000123.EDEPSIM.hdf5",
    "output": "$OUTBASE/day2_baseline/run/output.h5"
  },
  "larndsim": {
    "config": "2x2",
    "dir": "$WORKDIR/larnd-sim",
    "git": {
      "commit": "<larnd-sim commit>",
      "describe": "<larnd-sim version>",
      "is_git_repo": true,
      "status": ""
    }
  },
  "patch": {},
  "runtime": {
    "env": {
      "CUDA_HOME": "<cuda path>",
      "CUDA_VISIBLE_DEVICES": "<visible gpu ids>",
      "HDF5_USE_FILE_LOCKING": "0",
      "LARNDSIM_DISABLE_CUPY_MEMPOOL": "1"
    },
    "hostname": "<compute-node>",
    "platform": "<perlmutter linux platform>",
    "python": "3.11.7",
    "timestamp_utc": "<run timestamp>"
  },
  "sim": {
    "n_events": 5,
    "rand_seed": 321
  }
}
```

```text
<compute-node>:sim2spec > cat "$OUTBASE/day2_baseline/run/qa/metrics.json"
{
  "adc_max_guess": 255.0,
  "adc_mean_guess": 22.472872644203314,
  "adc_min_guess": 0.0,
  "adc_std_guess": 24.093075296481327,
  "datasets": [
    "_header",
    "configs",
    "light_dat",
    "light_trig",
    "light_wvfm",
    "light_wvfm_mc_assn",
    "mc_hdr",
    "mc_packets_assn",
    "mc_stack",
    "messages",
    "packets",
    "segments",
    "trajectories",
    "vertices"
  ],
  "file": "$OUTBASE/day2_baseline/run/output.h5",
  "n_light_dat": 4,
  "n_light_trig": 5,
  "n_light_wvfm": 5,
  "n_mc_packets_assn": 7004,
  "n_packets": 7004,
  "timestamp_max": 10000000,
  "timestamp_min": 0
}
```

```text
# Save QA metrics from JSON to CSV for easy inspection and comparison
<compute-node>:sim2spec > python - <<'PY'
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
Saved to $OUTBASE/day2_baseline/run/qa/metrics.csv
```

```text
# List QA files
<compute-node>:sim2spec > find "$OUTBASE/day2_baseline/run/qa" -maxdepth 1 -type f
$OUTBASE/day2_baseline/run/qa/metrics.json
$OUTBASE/day2_baseline/run/qa/light_wvfm0.png
$OUTBASE/day2_baseline/run/qa/metrics.csv
$OUTBASE/day2_baseline/run/qa/adc_hist.png
$OUTBASE/day2_baseline/run/qa/timestamp_hist.png
```

```text
# Save validation plots with the Day 2 baseline
<compute-node>:sim2spec > export OUTPLOTS="$OUTBASE/day2_baseline/run/validation_plots"
<compute-node>:sim2spec > mkdir -p "$OUTPLOTS"
<compute-node>:sim2spec > python plot_validation.py \
>   "$OUTBASE/day2_baseline/run/output.h5" \
>   --outdir "$OUTPLOTS"
Reading : $OUTBASE/day2_baseline/run/output.h5
Saving  : $OUTBASE/day2_baseline/run/validation_plots
Plot 1: Charge vs. Time ...
Saved: $OUTBASE/day2_baseline/run/validation_plots/plot_charge_vs_time.png
Plot 2: Hits per Event ...
Saved: $OUTBASE/day2_baseline/run/validation_plots/plot_hits_per_event.png
Plot 3: Single Waveform ...
Saved: $OUTBASE/day2_baseline/run/validation_plots/plot_single_waveform.png

All plots done.
```

### What to compare and analyze

- Does `output.h5` exist?
- Is `n_packets` nonzero?
- Are ADC statistics present?
- Are timestamp ranges present?
- Are QA plots created?
- **Charge vs. Time** — packets cluster at discrete timestamps (~0, 2, 4, 6, 8 × 10⁷ ticks) corresponding to individual neutrino events, with charge values mostly between 25–100 ADC and one outlier near 255 ADC
- **Hits per Event** — event activity is highly uneven; event 1 dominates with ~3600 segments while events 0, 3, and 4 are much smaller, reflecting varying complexity of neutrino interactions
- **Single Light Waveform** — noise-like fluctuations centered around 0 ADC (±20–30 counts) with one clear photon signal spike near sample 850 reaching ~52 ADC above the noise floor

### What to show

- baseline run directory
- `manifest.json`
- `metrics.json`
- QA PNG files
- `plot_charge_vs_time.png` — charge deposits clustered by event time
- `plot_hits_per_event.png` — segment count per event showing interaction complexity
- `plot_single_waveform.png` — light signal with noise floor and photon spike visible

### Achieved by end of Day

- baseline run is successful
- QA is generating metrics and plots
- a stable reference output exists
- `output.h5` is read directly by `plot_validation.py`
- baseline validation plots are saved in `$OUTBASE/day2_baseline/run/validation_plots`
- baseline fully characterized and ready for parameter variation studies in later days
