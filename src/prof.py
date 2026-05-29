from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import subprocess

from utils import ensure_dir, write_json


def parse_nsys_stats(run_dir: str) -> Dict[str, Any]:
    rd = Path(run_dir)
    rep = None
    for cand in rd.glob("nsys_report*.nsys-rep"):
        rep = cand
        break
    if rep is None:
        for cand in rd.glob("nsys_report*.qdrep"):
            rep = cand
            break
    if rep is None:
        return {"error": "No nsys report found in run dir"}

    out: Dict[str, Any] = {"report": str(rep)}
    try:
        txt = subprocess.check_output(["nsys", "stats", str(rep)], stderr=subprocess.STDOUT)
        out["nsys_stats_text"] = txt.decode("utf-8", errors="replace")
    except Exception as e:
        out["error"] = f"Failed to run nsys stats: {e}"
    return out


def save_profile_summary(run_dir: str) -> str:
    ensure_dir(run_dir)
    prof_dir = ensure_dir(Path(run_dir) / "profile")
    summary = parse_nsys_stats(run_dir)
    p = Path(prof_dir) / "nsys_stats.json"
    write_json(p, summary)
    return str(p)
