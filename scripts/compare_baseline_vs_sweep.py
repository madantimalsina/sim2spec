import os
import glob
import json

base = os.environ["OUTBASE"]

groups = {
    "baseline": f"{base}/day2_baseline/run/qa/metrics.json",
    "day3_sweep": f"{base}/day3_sweep/*/qa/metrics.json",
}

print("=== BASELINE ===")
p = groups["baseline"]
if os.path.exists(p):
    d = json.load(open(p))
    print("baseline", d.get("n_packets"), d.get("adc_mean", d.get("adc_mean_guess")))

print("\n=== DAY 3 SWEEP ===")
for p in sorted(glob.glob(groups["day3_sweep"])):
    d = json.load(open(p))
    print(p.split("/")[-3], d.get("n_packets"), d.get("adc_mean", d.get("adc_mean_guess")))
