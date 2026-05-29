#!/usr/bin/env python3
"""
Plot_validation.py
------------------
Quick validation plots from sim2spec output.h5:
  1. Charge (ADC) vs. timestamp
  2. Hits per event
  3. A single light waveform
Usage:
    python Plot_validation.py <output.h5>
"""

import sys, os
import h5py
import numpy as np
# Keep plotting non-interactive even when launched from a notebook shell that
# exports MPLBACKEND=module://matplotlib_inline.backend_inline.
os.environ["MPLBACKEND"] = "Agg"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── input ──────────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    print("Usage: python Plot_validation.py <output.h5>")
    sys.exit(1)

h5path  = sys.argv[1]
out_dir = os.path.dirname(os.path.abspath(h5path))

print(f"Reading : {h5path}")
print(f"Saving  : {out_dir}")

# ── 1. Charge vs. time ─────────────────────────────────────────────────────
print("Plot 1: Charge vs. Time ...")
with h5py.File(h5path, "r") as f:
    timestamp = f["packets"]["timestamp"][:].astype(float)
    dataword  = f["packets"]["dataword"][:].astype(float)

fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(timestamp, dataword, s=2, alpha=0.4, color="steelblue")
ax.set_xlabel("Timestamp [ticks]")
ax.set_ylabel("Charge [ADC counts]")
ax.set_title("Charge vs. Time")
fig.tight_layout()
p1 = os.path.join(out_dir, "plot_charge_vs_time.png")
fig.savefig(p1, dpi=150)
plt.close(fig)
del timestamp, dataword
print(f"Saved: {p1}")

# ── 2. Hits per event ──────────────────────────────────────────────────────
print("Plot 2: Hits per Event ...")
with h5py.File(h5path, "r") as f:
    event_id = f["segments"]["event_id"][:]

unique, cnt = np.unique(event_id, return_counts=True)
del event_id

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(unique, cnt, width=0.6, color="darkorange", alpha=0.85)
ax.set_xlabel("Event ID")
ax.set_ylabel("Number of Segments (Hits)")
ax.set_title("Hits per Event")
fig.tight_layout()
p2 = os.path.join(out_dir, "plot_hits_per_event.png")
fig.savefig(p2, dpi=150)
plt.close(fig)
del unique, cnt
print(f"Saved: {p2}")

# ── 3. Single light waveform ───────────────────────────────────────────────
print("Plot 3: Single Waveform ...")
with h5py.File(h5path, "r") as f:
    wvfm = f["light_wvfm"][0, 0, :]    # trigger 0, channel 0, 1000 samples

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(wvfm, color="mediumseagreen", lw=1)
ax.set_xlabel("Sample index")
ax.set_ylabel("ADC counts")
ax.set_title("Single Light Waveform (trigger 0, channel 0)")
fig.tight_layout()
p3 = os.path.join(out_dir, "plot_single_waveform.png")
fig.savefig(p3, dpi=150)
plt.close(fig)
del wvfm
print(f"Saved: {p3}")

print("\nAll plots done.")
