import glob
import json
import os

root = os.environ["OUTBASE"] + "/day3_sweep"
for mpath in sorted(glob.glob(root + "/*/manifest.json")):
    d = json.load(open(mpath))
    print("RUN:", mpath.split("/")[-2])
    print("  config:", d["larndsim"]["config"])
    print("  seed:", d["sim"]["rand_seed"])
    print("  n_events:", d["sim"]["n_events"])
    print("  git_commit:", d["larndsim"]["git"].get("commit"))
    print("  env:", d.get("env_applied"))
    print("  patch:", d.get("patch"))
