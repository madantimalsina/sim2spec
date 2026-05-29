from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from utils import now_iso


def _run(cmd: list[str], cwd: Optional[str] = None) -> str:
    try:
        out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="replace").strip()
    except Exception as e:
        return f"ERROR: {e}"


def git_info(repo_dir: str) -> Dict[str, Any]:
    p = Path(repo_dir)
    if not (p / ".git").exists():
        return {"is_git_repo": False}
    return {
        "is_git_repo": True,
        "commit": _run(["git", "rev-parse", "HEAD"], cwd=repo_dir),
        "status": _run(["git", "status", "--porcelain=v1"], cwd=repo_dir),
        "describe": _run(["git", "describe", "--tags", "--always"], cwd=repo_dir),
    }


def runtime_info() -> Dict[str, Any]:
    return {
        "timestamp_utc": now_iso(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "env": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "CUDA_HOME": os.environ.get("CUDA_HOME"),
            "HDF5_USE_FILE_LOCKING": os.environ.get("HDF5_USE_FILE_LOCKING"),
            "LARNDSIM_DISABLE_CUPY_MEMPOOL": os.environ.get("LARNDSIM_DISABLE_CUPY_MEMPOOL"),
        },
    }
