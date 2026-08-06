import glob
import json
import os

root = os.environ["OUTBASE"] + "/day3_sweep"
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
