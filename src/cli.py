from __future__ import annotations

import argparse
import json

from runner import run_larndsim
from utils import ensure_dir, write_json


def _common_env_from_args(args: argparse.Namespace) -> dict[str, str]:
    extra_env: dict[str, str] = {}
    if getattr(args, "disable_cupy_mempool", False):
        extra_env["LARNDSIM_DISABLE_CUPY_MEMPOOL"] = "1"
    if getattr(args, "hdf5_no_lock", False):
        extra_env["HDF5_USE_FILE_LOCKING"] = "0"
    return extra_env


def cmd_run(args: argparse.Namespace) -> int:
    outdir = ensure_dir(args.outdir)
    run_dir = outdir / "run"
    out_h5 = str(run_dir / "output.h5")

    return run_larndsim(
        larndsim_dir=args.larndsim_dir,
        config_name=args.config,
        input_path=args.input,
        output_path=out_h5,
        run_dir=str(run_dir),
        rand_seed=args.seed,
        n_events=args.n_events,
        patch={},
        extra_env=_common_env_from_args(args),
        profiler=args.profiler,
    )



def cmd_sweep(args: argparse.Namespace) -> int:
    from config_patch import load_sweep_variants
    from qa import qa_run

    variants = load_sweep_variants(args.sweep)
    outdir = ensure_dir(args.outdir)

    rc_all = 0
    for i, (name, patch, seed_override) in enumerate(variants):
        run_dir = outdir / f"{i:03d}_{name}"
        out_h5 = str(run_dir / "output.h5")
        rand_seed = seed_override if seed_override is not None else args.seed + i

        rc = run_larndsim(
            larndsim_dir=args.larndsim_dir,
            config_name=args.config,
            input_path=args.input,
            output_path=out_h5,
            run_dir=str(run_dir),
            rand_seed=rand_seed,
            n_events=args.n_events,
            patch=patch,
            extra_env=_common_env_from_args(args),
            profiler=args.profiler,
        )
        rc_all = rc_all or rc

        try:
            qa_run(str(run_dir))
        except Exception as e:
            write_json(run_dir / "qa_error.json", {"error": str(e)})

    return int(rc_all)



def cmd_qa(args: argparse.Namespace) -> int:
    from qa import qa_run

    s = qa_run(args.run_dir)
    print(json.dumps({"metrics": s.metrics, "plots": s.plots}, indent=2))
    return 0



def cmd_profile(args: argparse.Namespace) -> int:
    from prof import save_profile_summary

    p = save_profile_summary(args.run_dir)
    print(f"Wrote profile summary: {p}")
    return 0



def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sim2spec")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("run", help="Run a single larnd-sim job")
    pr.add_argument("--larndsim-dir", required=True, help="Path to larnd-sim checkout")
    pr.add_argument("--config", required=True, help="larnd-sim config keyword (for example 2x2)")
    pr.add_argument("--input", required=True, help="Input HDF5")
    pr.add_argument("--outdir", required=True, help="Output directory")
    pr.add_argument("--seed", type=int, default=321)
    pr.add_argument("--n-events", type=int, default=None)
    pr.add_argument("--disable-cupy-mempool", action="store_true")
    pr.add_argument("--hdf5-no-lock", action="store_true", help="Set HDF5_USE_FILE_LOCKING=0")
    pr.add_argument("--profiler", choices=["nsys"], default=None)
    pr.set_defaults(func=cmd_run)

    ps = sub.add_parser("sweep", help="Run a sweep of YAML patch variants")
    ps.add_argument("--larndsim-dir", required=True)
    ps.add_argument("--config", required=True)
    ps.add_argument("--input", required=True)
    ps.add_argument("--outdir", required=True)
    ps.add_argument("--sweep", required=True, help="Sweep YAML (variants)")
    ps.add_argument("--seed", type=int, default=321)
    ps.add_argument("--n-events", type=int, default=None)
    ps.add_argument("--disable-cupy-mempool", action="store_true")
    ps.add_argument("--hdf5-no-lock", action="store_true", help="Set HDF5_USE_FILE_LOCKING=0")
    ps.add_argument("--profiler", choices=["nsys"], default=None)
    ps.set_defaults(func=cmd_sweep)

    pq = sub.add_parser("qa", help="Compute QA metrics and plots for a run directory")
    pq.add_argument("--run-dir", required=True)
    pq.set_defaults(func=cmd_qa)

    pf = sub.add_parser("profile", help="Parse profiling outputs in a run directory")
    pf.add_argument("--run-dir", required=True)
    pf.set_defaults(func=cmd_profile)

    return p



def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    rc = args.func(args)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
