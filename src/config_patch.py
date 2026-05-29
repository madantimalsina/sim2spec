from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import yaml

from utils import clamp


@dataclass(frozen=True)
class PatchProposal:
    name: str
    patch: Dict[str, Any]


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(obj: Dict[str, Any], path: str) -> None:
    import os

    os.makedirs(str(__import__("pathlib").Path(path).parent), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False)


# def generate_bounded_proposals(bounds_yaml: str) -> List[PatchProposal]:
#     """Generate conservative 1D patch proposals from a bounds YAML."""
#     cfg = load_yaml(bounds_yaml)
#     patches = cfg.get("patches", [])
#     out: List[PatchProposal] = []

#     for p in patches:
#         name = p["name"]
#         kind = p.get("kind", "scalar")
#         if kind != "scalar":
#             continue

#         tgt = p["target"]["key_path"]  # e.g. ["SIM_PROPERTIES", "pixel_threshold_adc"]
#         lo = float(p["min"])
#         hi = float(p["max"])
#         steps = int(p.get("steps", 3))

#         if steps < 2:
#             vals = [clamp((lo + hi) / 2, lo, hi)]
#         else:
#             vals = [lo + (hi - lo) * i / (steps - 1) for i in range(steps)]

#         for v in vals:
#             patch: Dict[str, Any] = {}
#             cur = patch
#             for k in tgt[:-1]:
#                 cur[k] = {}
#                 cur = cur[k]

#             # preserve int when bounds are int
#             if isinstance(p["min"], int) and isinstance(p["max"], int):
#                 cur[tgt[-1]] = int(round(v))
#             else:
#                 cur[tgt[-1]] = float(v)

#             out.append(PatchProposal(name=f"{name}_{cur[tgt[-1]]}", patch=patch))

#     # de-dup by name
#     seen = set()
#     unique: List[PatchProposal] = []
#     for pp in out:
#         if pp.name in seen:
#             continue
#         seen.add(pp.name)
#         unique.append(pp)
#     return unique


def load_sweep_variants(sweep_yaml: str) -> List[Tuple[str, Dict[str, Any], Optional[int]]]:
    cfg = load_yaml(sweep_yaml)
    variants = cfg.get("variants", [])
    out: List[Tuple[str, Dict[str, Any], Optional[int]]] = []
    for v in variants:
        out.append((v["name"], v.get("patch", {}) or {}, v.get("seed")))
    return out
