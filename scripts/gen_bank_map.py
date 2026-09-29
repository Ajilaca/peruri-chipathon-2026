#!/usr/bin/env python3
"""scripts/gen_bank_map.py

1. Exhaustively proves the Phase 2 bank-mapping scheme (tb/mem/bank_model.py) conflict-free for
   L in {1,2,4,8}, per docs/evidence/phase02-memory/test_plan.md ("Bank-mapping conflict-freedom
   proof"). Writes the raw log to
   docs/evidence/phase02-memory/bank_scheme_exploration_<date>.txt. Stops (non-zero exit) if any
   check fails -- this script is not allowed to silently pass a broken scheme.
2. Generates rtl/mem/bank_map_rom.sv (never hand-typed) from the same golden model.

Run: python3 scripts/gen_bank_map.py
"""

from __future__ import annotations

import datetime
import pathlib
import sys
from collections import Counter

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tb" / "mem"))

from bank_model import N, addr_pair, bank_of, build_maps, lane_p, log2_of  # noqa: E402

L_VALUES = (1, 2, 4, 8)
EV_DIR = REPO_ROOT / "docs" / "evidence" / "phase02-memory"
ROM_OUT = REPO_ROOT / "rtl" / "mem" / "bank_map_rom.sv"


def check_own_pair(log: list[str]) -> bool:
    ok = True
    for L in L_VALUES:
        bad = []
        for mode_inv in (0, 1):
            for layer in range(7):
                for p in range(128):
                    j, jlen = addr_pair(layer, mode_inv, p)
                    if L > 1 and bank_of(j, L) == bank_of(jlen, L):
                        bad.append((mode_inv, layer, p, j, jlen))
        log.append(f"L={L}: own-pair collisions = {len(bad)}" + (f"  FIRST BAD: {bad[0]}" if bad else ""))
        ok &= (len(bad) == 0)
    return ok


def check_balance(log: list[str]) -> bool:
    ok = True
    for L in L_VALUES:
        c = Counter(bank_of(a, L) for a in range(N))
        balanced = len(c) == L and all(v == N // L for v in c.values())
        log.append(f"L={L}: bank sizes = {dict(sorted(c.items()))}  balanced={balanced}")
        ok &= balanced
    return ok


def check_bijective(log: list[str]) -> bool:
    ok = True
    for L in L_VALUES:
        bank_arr, off_arr, addr_of = build_maps(L)
        pairs = set(zip(bank_arr, off_arr))
        bijective = len(pairs) == N
        in_range = all(b < L for b in bank_arr) and all(o < N // L for o in off_arr)
        log.append(f"L={L}: bijective={bijective}  addresses={N}  distinct(bank,offset)={len(pairs)}  in_range={in_range}")
        ok &= bijective and in_range
    return ok


def check_multilane(log: list[str]) -> bool:
    ok = True
    for L in (2, 4, 8):
        for scheme_name, p_fn in (("block", lambda L, m, t: lane_p(L, m, t)),
                                   ("interleave", lambda L, m, t: t * L + m)):
            worst = 0
            worst_detail = None
            for mode_inv in (0, 1):
                for layer in range(7):
                    per_lane = 128 // L
                    for t in range(per_lane):
                        addrs = []
                        for m in range(L):
                            p = p_fn(L, m, t)
                            j, jlen = addr_pair(layer, mode_inv, p)
                            addrs += [j, jlen]
                        c = Counter(bank_of(a, L) for a in addrs)
                        mx = max(c.values())
                        if mx > worst:
                            worst, worst_detail = mx, (mode_inv, layer, t, addrs, dict(c))
            cap_ok = worst <= 2
            log.append(f"L={L} grouping={scheme_name}: worst accesses/bank/cycle = {worst}"
                        f"  (<=2 M10K dual-port capacity: {'OK' if cap_ok else 'EXCEEDED'})")
            if scheme_name == "block":
                ok &= cap_ok  # this is the grouping actually used (tb/mem/bank_model.py:lane_p)
            else:
                log.append(f"    (interleave is a documented negative control, not used; "
                            f"detail: {worst_detail})")
    return ok


def rom_body(l_value: int) -> str:
    bank_arr, off_arr, _ = build_maps(l_value)
    log2l = log2_of(l_value)
    bank_w = max(1, log2l)
    off_w = max(1, (N // l_value - 1).bit_length())
    lines = []
    for a in range(N):
        lines.append(f"      8'd{a}: begin bank_o = {bank_w}'d{bank_arr[a]}; "
                      f"offset_o = {off_w}'d{off_arr[a]}; end")
    return "\n".join(lines), bank_w, off_w


def main() -> int:
    log: list[str] = []
    log.append("Phase 2 bank-mapping scheme: exhaustive conflict-freedom proof")
    log.append(f"Generated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC "
               "by scripts/gen_bank_map.py, from tb/mem/bank_model.py")
    log.append("")
    log.append("--- 1. Own-pair check (bank(j) != bank(jlen), every L, every layer, every p) ---")
    ok1 = check_own_pair(log)
    log.append("")
    log.append("--- 2. Bank balance (every bank holds exactly N/L addresses) ---")
    ok2 = check_balance(log)
    log.append("")
    log.append("--- 3. Offset bijectivity + address range ---")
    ok3 = check_bijective(log)
    log.append("")
    log.append("--- 4. Multi-lane capacity (<=2 accesses/bank/cycle, contiguous-block grouping) ---")
    ok4 = check_multilane(log)
    log.append("")
    all_ok = ok1 and ok2 and ok3 and ok4
    log.append(f"RESULT: {'ALL CHECKS PASS' if all_ok else 'FAILED -- scheme is NOT conflict-free, do not use'}")

    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    EV_DIR.mkdir(parents=True, exist_ok=True)
    out_txt = EV_DIR / f"bank_scheme_exploration_{date}.txt"
    out_txt.write_text("\n".join(log) + "\n")
    print("\n".join(log))
    print(f"\nwrote {out_txt}")

    if not all_ok:
        return 1

    # --- generate the ROM ---
    parts = []
    gens = []
    for L in L_VALUES:
        body, bank_w, off_w = rom_body(L)
        # Plain always_comb + case per L, not a function: Icarus Verilog does not accept
        # `output` function arguments (an SV extension Verilator/slang support but Icarus
        # rejects at elaboration), so each L gets its own always_comb block instead, selected
        # at elaboration time by the generate-if below.
        parts.append(f"""
  // L={L}: bank width {bank_w} bit(s), offset width {off_w} bit(s)
  generate
    if (NUM_BANKS == {L}) begin : g_l{L}
      always_comb begin
        unique case (addr_i)
{body}
          default: begin bank_o = '0; offset_o = '0; end
        endcase
      end
    end
  endgenerate
""")
    content = f"""`default_nettype none
`timescale 1ns/1ps
// rtl/mem/bank_map_rom.sv
// GENERATED by scripts/gen_bank_map.py on {date} UTC from tb/mem/bank_model.py. Do not
// hand-edit; re-run the generator instead.
//
// Conflict-free bank mapping for the 256-entry polynomial memory (docs/ROADMAP.md Phase 2).
// addr_i (0..255, a logical coefficient index -- the same "j"/"jlen" used throughout
// rtl/ntt/ntt_core.sv) maps to (bank_o, offset_o) for a compile-time bank count L in
// {{1,2,4,8}}, selected by the NUM_BANKS parameter. Exhaustively proven conflict-free (own-pair,
// balance, bijectivity, multi-lane capacity) in
// docs/evidence/phase02-memory/bank_scheme_exploration_{date}.txt; scheme documented in
// tb/mem/bank_model.py.

module bank_map_rom #(
    parameter int NUM_BANKS = 1
) (
    input  wire  [7:0] addr_i,
    output logic [(NUM_BANKS > 1 ? $clog2(NUM_BANKS) : 1) - 1 : 0] bank_o,
    output logic [$clog2(256 / NUM_BANKS) - 1 : 0] offset_o
);
{"".join(parts)}


endmodule
`default_nettype wire
"""
    ROM_OUT.write_text(content)
    print(f"wrote {ROM_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
