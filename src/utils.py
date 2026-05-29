from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def ensure_dir(p: str | Path) -> Path:
    path = Path(p)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: str | Path, obj: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def read_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def env_or_default(key: str, default: str | None = None) -> str | None:
    v = os.environ.get(key)
    return v if v is not None else default


def now_iso() -> str:
    from datetime import datetime

    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def deep_update(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively update nested dictionaries: base <- patch."""
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_update(base[k], v)
        else:
            base[k] = v
    return base
