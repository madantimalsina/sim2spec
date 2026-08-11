import os

base = os.environ["OUTBASE"]
runs = ["day3_profile_baseline", "day4_profile_tpb64"]

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
