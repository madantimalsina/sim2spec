from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from provenance import git_info, runtime_info
from utils import ensure_dir, write_json


def build_run_manifest(
    larndsim_dir: str,
    config_name: str,
    input_path: str,
    output_path: str,
    rand_seed: int,
    n_events: Optional[int],
    extra_env: Dict[str, str],
    patch: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "larndsim": {
            "dir": larndsim_dir,
            "git": git_info(larndsim_dir),
            "config": config_name,
        },
        "io": {"input": input_path, "output": output_path},
        "sim": {"rand_seed": rand_seed, "n_events": n_events},
        "patch": patch,
        "runtime": runtime_info(),
        "env_applied": extra_env,
    }


def run_larndsim(
    larndsim_dir: str,
    config_name: str,
    input_path: str,
    output_path: str,
    run_dir: str,
    rand_seed: int = 321,
    n_events: Optional[int] = None,
    patch: Optional[Dict[str, Any]] = None,
    extra_env: Optional[Dict[str, str]] = None,
    profiler: Optional[str] = None,  # None | "nsys"
) -> int:
    """Run larnd-sim via cli/simulate_pixels.py.

    NOTE: patch is recorded for provenance; automatic YAML patch-injection is a planned extension.
    """

    patch = patch or {}
    extra_env = extra_env or {}

    rd = ensure_dir(run_dir)

    env = os.environ.copy()
    env.update(extra_env)
    env.setdefault("HDF5_USE_FILE_LOCKING", "0")

    simulate_py = Path(larndsim_dir) / "cli" / "simulate_pixels.py"
    if not simulate_py.exists():
        raise FileNotFoundError(f"Could not find {simulate_py}")

    cmd = [
        "python3",
        str(simulate_py),
        config_name,
        "--input_filename",
        str(input_path),
        "--output_filename",
        str(output_path),
        "--rand_seed",
        str(rand_seed),
    ]
    if n_events is not None:
        cmd.extend(["--n_events", str(n_events)])

    manifest = build_run_manifest(
        larndsim_dir=larndsim_dir,
        config_name=config_name,
        input_path=str(input_path),
        output_path=str(output_path),
        rand_seed=rand_seed,
        n_events=n_events,
        extra_env=extra_env,
        patch=patch,
    )
    write_json(rd / "manifest.json", manifest)
    write_json(rd / "command.json", {"cmd": cmd})

    if profiler == "nsys":
        cmd = [
            "nsys",
            "profile",
            "-o",
            str(Path(rd) / "nsys_report"),
            "--force-overwrite=true",
            "--trace=cuda,nvtx,osrt",
            "--cuda-memory-usage=true",
            "--python-backtrace=cuda",
            "--python-sampling=true",
        ] + cmd
        write_json(rd / "command_profiled.json", {"cmd": cmd})

    proc = subprocess.run(cmd, env=env, cwd=str(rd))
    if proc.returncode != 0:
        write_json(rd / "run_failed.json", {"returncode": proc.returncode, "cmd": cmd})
        print(
            f"\n[sim2spec] ERROR: larnd-sim exited with code {proc.returncode}.\n"
            f"  Run directory : {rd}\n"
            f"  Failure record: {rd / 'run_failed.json'}\n"
            f"  Check the output above for CUDA or Python errors."
        )
    return int(proc.returncode)
