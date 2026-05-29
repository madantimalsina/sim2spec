from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import h5py
# Force a non-interactive backend before importing matplotlib. Notebook
# subprocesses may inherit MPLBACKEND=module://matplotlib_inline..., which is
# not valid in this CLI environment on Perlmutter compute nodes.
os.environ["MPLBACKEND"] = "Agg"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from utils import ensure_dir, write_json


@dataclass
class QASummary:
    metrics: Dict[str, Any]
    plots: Dict[str, str]


def _safe_len(ds) -> int:
    try:
        return int(ds.shape[0])
    except Exception:
        return int(len(ds))


def compute_basic_metrics(out_h5: str) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {"file": str(out_h5)}

    with h5py.File(out_h5, "r") as f:
        metrics["datasets"] = list(f.keys())

        for k in ["packets", "mc_packets_assn", "tracks", "events", "light_wvfm", "light_trig", "light_dat"]:
            if k in f:
                metrics[f"n_{k}"] = _safe_len(f[k])

        if "packets" in f:
            pkt = f["packets"]
            if hasattr(pkt, "dtype") and pkt.dtype.names:
                names = set(pkt.dtype.names)

                # timestamps
                if "timestamp" in names:
                    ts = pkt["timestamp"][:]
                    metrics["timestamp_min"] = int(np.min(ts)) if ts.size else None
                    metrics["timestamp_max"] = int(np.max(ts)) if ts.size else None

                # adc
                if "adc" in names:
                    adc = pkt["adc"][:]
                    if adc.size:
                        metrics["adc_min"] = float(np.min(adc))
                        metrics["adc_max"] = float(np.max(adc))
                        metrics["adc_mean"] = float(np.mean(adc))
                        metrics["adc_std"] = float(np.std(adc))
                elif "dataword" in names:
                    dw = pkt["dataword"][:].astype(np.uint32)
                    adc = (dw & np.uint32(0x3FF)).astype(np.int32)  # heuristic 10-bit
                    if adc.size:
                        metrics["adc_min_guess"] = float(np.min(adc))
                        metrics["adc_max_guess"] = float(np.max(adc))
                        metrics["adc_mean_guess"] = float(np.mean(adc))
                        metrics["adc_std_guess"] = float(np.std(adc))

    return metrics


def make_plots(out_h5: str, outdir: str) -> Dict[str, str]:
    od = ensure_dir(outdir)
    plots: Dict[str, str] = {}

    with h5py.File(out_h5, "r") as f:
        if "packets" in f:
            pkt = f["packets"]
            if hasattr(pkt, "dtype") and pkt.dtype.names:
                names = set(pkt.dtype.names)

                adc = None
                if "adc" in names:
                    adc = pkt["adc"][:]
                elif "dataword" in names:
                    dw = pkt["dataword"][:].astype(np.uint32)
                    adc = (dw & np.uint32(0x3FF)).astype(np.int32)

                if adc is not None and adc.size:
                    plt.figure()
                    plt.hist(adc, bins=100)
                    plt.xlabel("ADC (or ADC guess)")
                    plt.ylabel("Counts")
                    p = od / "adc_hist.png"
                    plt.savefig(p, dpi=150, bbox_inches="tight")
                    plt.close()
                    plots["adc_hist"] = str(p)

                if "timestamp" in names:
                    ts = pkt["timestamp"][:]
                    if ts.size:
                        plt.figure()
                        plt.hist(ts, bins=200)
                        plt.xlabel("timestamp")
                        plt.ylabel("counts")
                        p = od / "timestamp_hist.png"
                        plt.savefig(p, dpi=150, bbox_inches="tight")
                        plt.close()
                        plots["timestamp_hist"] = str(p)

        if "light_wvfm" in f:
            w = f["light_wvfm"]
            if w.shape and w.shape[0] > 0:
                arr = np.array(w[0]).ravel()
                if arr.size:
                    plt.figure()
                    plt.plot(arr)
                    plt.xlabel("sample")
                    plt.ylabel("ADC")
                    p = od / "light_wvfm0.png"
                    plt.savefig(p, dpi=150, bbox_inches="tight")
                    plt.close()
                    plots["light_wvfm0"] = str(p)

    return plots


def qa_run(run_dir: str) -> QASummary:
    rd = Path(run_dir)
    manifest = rd / "manifest.json"
    if not manifest.exists():
        raise FileNotFoundError(f"Missing {manifest}; run sim2spec run first.")

    import json

    m = json.loads(manifest.read_text(encoding="utf-8"))
    out_h5 = m["io"]["output"]

    if not Path(out_h5).exists():
        failed = rd / "run_failed.json"
        hint = f" Check {failed} for the exit code." if failed.exists() else \
               " The simulation may have failed — check its output for errors."
        raise FileNotFoundError(
            f"Simulation output not found: {out_h5}\n"
            f"  Run 'sim2spec run ...' first and make sure it completes successfully.{hint}"
        )

    qa_dir = ensure_dir(rd / "qa")
    metrics = compute_basic_metrics(out_h5)
    plots = make_plots(out_h5, str(qa_dir))

    write_json(qa_dir / "metrics.json", metrics)
    return QASummary(metrics=metrics, plots=plots)
