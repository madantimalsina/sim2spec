import glob
import json
import os
import csv

root = os.environ["OUTBASE"] + "/day3_sweep"
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
