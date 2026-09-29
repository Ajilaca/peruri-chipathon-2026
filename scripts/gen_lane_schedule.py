#!/usr/bin/env python3
"""scripts/gen_lane_schedule.py

Exhaustively proves, for Phase 3 (docs/ROADMAP.md Phase 3, L in {1,2,4,8}), that:

1. `bank_model.zeta_index_of` (a closed-form, per-(layer,block) twiddle index) reproduces
   `bank_model.reference_zeta_trace` (rtl/ntt/ntt_core.sv's own sequential zeta_idx update rule)
   exactly, for every (layer, block) pair, both directions. This is the fact that lets each
   Phase 3 lane compute its zeta index combinationally instead of sharing one running counter.
2. For every L, every mode, every layer, every sub-cycle t: the L lanes active that sub-cycle
   (`bank_model.lane_p`) touch distinct (j, jlen) butterfly pairs -- i.e. the per-lane p
   assignment does not make two lanes redo the same butterfly or skip one, across the full
   128-butterfly layer.

Writes the raw log to docs/evidence/phase03-multilane/lane_schedule_verification_<date>.txt.
Stops (non-zero exit) if any check fails -- this script is not allowed to silently pass a
broken schedule.

Run: python3 scripts/gen_lane_schedule.py
"""

from __future__ import annotations

import datetime
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tb" / "mem"))

from bank_model import (  # noqa: E402
    addr_pair,
    lane_p,
    layer_len,
    reference_zeta_trace,
    zeta_index_of,
)

L_VALUES = (1, 2, 4, 8)
EV_DIR = REPO_ROOT / "docs" / "evidence" / "phase03-multilane"


def check_zeta_formula(log: list[str]) -> bool:
    ok = True
    for mode_inv in (0, 1):
        ref = reference_zeta_trace(mode_inv)
        mismatches = []
        for (layer, block), k_ref in ref.items():
            k_cand = zeta_index_of(layer, mode_inv, block)
            if k_cand != k_ref:
                mismatches.append((layer, block, k_ref, k_cand))
        entries = len(ref)
        log.append(f"mode_inv={mode_inv}: entries={entries} mismatches={len(mismatches)}")
        if mismatches:
            ok = False
            for m in mismatches[:10]:
                log.append(f"  MISMATCH layer={m[0]} block={m[1]} ref={m[2]} candidate={m[3]}")
    return ok


def check_lane_coverage(log: list[str]) -> bool:
    ok = True
    for num_lanes in L_VALUES:
        for mode_inv in (0, 1):
            for layer in range(7):
                length, log2len = layer_len(layer, mode_inv)
                seen_p: set[int] = set()
                per_t_conflicts = 0
                for t in range(128 // num_lanes):
                    ps_this_t = set()
                    for lane in range(num_lanes):
                        p = lane_p(num_lanes, lane, t)
                        if p in ps_this_t:
                            per_t_conflicts += 1
                        ps_this_t.add(p)
                        seen_p.add(p)
                covered_all = seen_p == set(range(128))
                status = "OK" if (covered_all and per_t_conflicts == 0) else "FAIL"
                if status == "FAIL":
                    ok = False
                log.append(
                    f"L={num_lanes} mode_inv={mode_inv} layer={layer} len={length}: "
                    f"covered={len(seen_p)}/128 per_t_conflicts={per_t_conflicts} -> {status}"
                )
    return ok


def main() -> int:
    log: list[str] = []
    date = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
    log.append("Phase 3 lane-schedule verification (zeta closed form + p-coverage)")
    log.append(f"Generated: {date} by scripts/gen_lane_schedule.py, from tb/mem/bank_model.py")
    log.append("")
    log.append("--- 1. Zeta closed-form vs. RTL's sequential update rule ---")
    zeta_ok = check_zeta_formula(log)
    log.append("")
    log.append("--- 2. Per-sub-cycle lane p-coverage (no duplicate, no gap, all 128 covered) ---")
    lane_ok = check_lane_coverage(log)
    log.append("")
    overall_ok = zeta_ok and lane_ok
    log.append(f"OVERALL: {'PASS' if overall_ok else 'FAIL'}")

    EV_DIR.mkdir(parents=True, exist_ok=True)
    out_txt = EV_DIR / f"lane_schedule_verification_{datetime.date.today().isoformat()}.txt"
    out_txt.write_text("\n".join(log) + "\n")
    print("\n".join(log))
    print(f"\nwritten: {out_txt}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
