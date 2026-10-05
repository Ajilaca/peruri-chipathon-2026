#!/usr/bin/env python3
"""scripts/test/pipeline_hazard_slack.py

Phase 4 planning aid (no RTL involved): for the existing lane schedule (tb/mem/bank_model.py:
lane_p, addr_pair), computes how deep a butterfly pipeline can be before a read-after-write hazard
appears at a layer boundary, for L in {1, 2, 4, 8} and both directions.

Model: layer k issues its butterflies at sub-cycles t = 0..T-1 (T = 128/L); layer k+1 starts at the
next cycle. With a pipeline of depth P, a butterfly issued at cycle t writes at t+P and the value is
readable from t+P+1. An address written by layer k at t_w and first read by layer k+1 at sub-cycle
t_r is therefore safe without any stall iff  T + t_r - t_w - 1 >= P.  "Slack" below is the minimum
of the left-hand side over all 256 addresses.

The same test is applied to the boundary between the last INTT layer and the x3303 scaling pass.

Within a layer there is no such hazard: every address is read and written exactly once per layer
(checked by the assertion).

Usage: python3 scripts/test/pipeline_hazard_slack.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tb" / "mem"))
from bank_model import addr_pair, lane_p  # noqa: E402


def main() -> int:
    print("Layer-boundary slack (cycles) of the current lane schedule; a pipeline of depth P needs no")
    print("stall at a boundary iff slack >= P.")
    for num_lanes in (1, 2, 4, 8):
        t_per_layer = 128 // num_lanes
        for mode, name in ((0, "NTT"), (1, "INTT")):
            slacks = []
            for layer in range(6):
                t_write, t_read = {}, {}
                for t in range(t_per_layer):
                    for lane in range(num_lanes):
                        p = lane_p(num_lanes, lane, t)
                        for a in addr_pair(layer, mode, p):
                            t_write[a] = t
                        for a in addr_pair(layer + 1, mode, p):
                            t_read[a] = t
                assert len(t_write) == 256 and len(t_read) == 256, "each address once per layer"
                slacks.append(min(t_per_layer + t_read[a] - t_write[a] - 1 for a in range(256)))
            print(f"L={num_lanes} {name:4s} T={t_per_layer:3d}: slack per boundary {slacks} "
                  f"-> largest stall-free P = {min(slacks)}")
        # INTT only: boundary between the last butterfly layer and the x3303 scaling pass, which reads
        # address a at cycle a (one address per cycle, addresses 0..255 in order).
        t_write = {}
        for t in range(t_per_layer):
            for lane in range(num_lanes):
                for a in addr_pair(6, 1, lane_p(num_lanes, lane, t)):
                    t_write[a] = t
        assert len(t_write) == 256
        scale_slack = min(t_per_layer + a - t_write[a] - 1 for a in range(256))
        print(f"L={num_lanes} INTT last layer -> scaling pass: slack {scale_slack} "
              f"(no stall before the scaling pass iff slack >= P)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
