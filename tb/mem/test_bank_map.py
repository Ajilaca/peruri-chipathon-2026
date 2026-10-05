"""tb/mem/test_bank_map.py - cocotb bit-exact test for rtl/mem/bank_map_rom.sv against the
golden model tb/mem/bank_model.py, exhaustive over all 256 addresses, for every NUM_BANKS in
{1, 2, 4, 8}. One cocotb test module per NUM_BANKS value (cocotb build-time parameters are set
per simulation run, not per test, so tb/mem/run_mem_tests.py builds this module four times).

Corner cases and exhaustive coverage per evidence/phase02/test_plan.md
("Unit: bank_map_rom").
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cocotb
from cocotb.triggers import Timer

from bank_model import N, bank_of, build_maps

NUM_BANKS = int(os.environ.get("BANK_MAP_L", "1"))


@cocotb.test()
async def test_bank_map_exhaustive(dut):
    bank_arr, off_arr, _ = build_maps(NUM_BANKS)
    for addr in range(N):
        dut.addr_i.value = addr
        await Timer(1, unit="ns")
        exp_bank, exp_off = bank_arr[addr], off_arr[addr]
        act_bank, act_off = int(dut.bank_o.value), int(dut.offset_o.value)
        assert (act_bank, act_off) == (exp_bank, exp_off), (
            f"NUM_BANKS={NUM_BANKS} addr={addr}: expected (bank={exp_bank}, offset={exp_off}), "
            f"got (bank={act_bank}, offset={act_off})"
        )


@cocotb.test()
async def test_bank_map_corners(dut):
    bank_arr, off_arr, _ = build_maps(NUM_BANKS)
    for addr in (0, N - 1, 128, 127, 129):
        dut.addr_i.value = addr
        await Timer(1, unit="ns")
        exp_bank, exp_off = bank_arr[addr], off_arr[addr]
        act_bank, act_off = int(dut.bank_o.value), int(dut.offset_o.value)
        assert (act_bank, act_off) == (exp_bank, exp_off), f"corner addr={addr} mismatch"
        assert bank_of(addr, NUM_BANKS) == exp_bank
