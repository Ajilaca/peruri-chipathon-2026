"""tb/golden/mlkem_ctl_model3.py

Phase 9I item 4 (docs/evidence/phase09m-optimisation/9i4/test_plan_9i4.md): the controller micro-programs of tb/golden/mlkem_ctl_model2.py (background hash) with the loads that the K-PKE engine needs only later moved behind the start of the engine:
("RUNS", prog, mask) starts the engine program and continues at once, mask = the engine slots whose load follows (bit s = slot s, 12 bits); the LDP micro-operations after it load those slots while the engine runs; ("RUNJ",) waits until the engine is done.
Functionally the engine program is run at RUNJ after the loads have been done (the values are the same as in the programs of model2: the hardware interlock only starts an engine operation after the load of every slot it uses is complete); `check_static3` proves the structure.
Independent of any RTL. The models of Phase 9 and 9F are not changed.
"""
from __future__ import annotations

import mlkem_ctl_model as CM
import mlkem_ctl_model2 as M2
from mlkem_ctl_model import (CB2R, CBR, K, KB, OFF_EK, OFF_H, OFF_RHO, OFF_Z, PROG_ID, RFR, R_D, R_HH, R_K, R_KBAR, R_M, R_RHO, R_SD, R_Z, SRC_CONST, G_SEL, H_SEL, J_SEL, ENGINE, State)

OPC = {**M2.OPC, "RUNS": 13, "RUNJ": 14}


def _mask(loads):
    m = 0
    for op in loads:
        assert op[0] == "LDP"
        m |= 1 << op[1]
    return m


def _keygen():
    return M2._keygen()


def _encaps():
    # H(ek) in the background during RD32 and the first load; the other loads run behind the engine (t_hat is first used by the 31st operation of the engine program, the message polynomial by the last)
    later = [("LDP", 8, KB, OFF_EK + 48, 12), ("LDP", 9, KB, OFF_EK + 96, 12), ("LDP", 11, RFR, 4 * R_M, 1)]
    p = [("BGS", None), ("RD32", R_RHO, OFF_RHO), ("LDP", 7, KB, OFF_EK, 12), ("JN",)]
    p += [("HST", G_SEL, 64), ("HFD", RFR, 4 * R_M, 4), ("HFD", RFR, 4 * R_HH, 4), ("HGT", R_K, R_SD)]
    p += [("SDL",), ("RUNS", ENGINE["encrypt"], _mask(later))] + later + [("RUNJ",)]
    p += [("STP", 3 + i, CBR, 40 * i, 10) for i in range(K)] + [("STP", 10, CBR, 120, 4), ("END",)]
    job = [("HST", H_SEL, 1184), ("HFD", KB, OFF_EK, 148), ("HGT", R_HH, 0), ("END",)]
    return p, [job]


def _reencrypt3(dst):
    later = [("LDP", 7 + j, KB, OFF_EK + 48 * j, 12) for j in range(K)] + [("LDP", 11, RFR, 4 * R_M, 1)]
    p = [("RD32", R_RHO, OFF_RHO), ("SDL",), ("RUNS", ENGINE["encrypt"], _mask(later))] + later + [("RUNJ",)]
    p += [("STP", 3 + i, dst, 40 * i, 10) for i in range(K)] + [("STP", 10, dst, 120, 4)]
    return p


def _decaps():
    # J(z || c) in the background; the decryption starts after the first polynomial of the ciphertext, the other inputs are loaded behind it (in the order in which the engine program uses them)
    later = [("LDP", 4, CBR, 40, 10), ("LDP", 5, CBR, 80, 10)] + [("LDP", i, KB, 48 * i, 12) for i in range(K)] + [("LDP", 10, CBR, 120, 4)]
    p = [("BGS", None), ("LDP", 3, CBR, 0, 10), ("RUNS", ENGINE["decrypt"], _mask(later))] + later + [("RUNJ",)]
    p += [("STP", 10, RFR, 4 * R_M, 1), ("JN",)]
    p += [("HST", G_SEL, 64), ("HFD", RFR, 4 * R_M, 4), ("HFD", KB, OFF_H, 4), ("HGT", R_K, R_SD)]
    p += _reencrypt3(CB2R) + [("CMP",), ("END",)]
    job = [("HST", J_SEL, 1120), ("HFD", KB, OFF_Z, 4), ("HFD", CBR, 0, 136), ("HGT", R_KBAR, 0), ("END",)]
    return p, [job]


def build():
    out = {}
    for name, f in (("keygen", _keygen), ("encaps", _encaps), ("decaps", _decaps)):
        main, jobs = f()
        base = len(main)
        res = [("BGS", base) if op[0] == "BGS" else op for op in main]
        out[name] = (res + [w for j in jobs for w in j], base)
    return out


PROGRAMS3 = {n: v[0] for n, v in build().items()}
split = M2.split
_job_slice = M2._job_slice


def run3(prog, st: State):
    """Runs a program of this model; RUNS ... RUNJ: the loads are done first, then the engine program (the result of the hardware: same values)."""
    main, job = split(prog)
    n, i = 0, 0
    while i < len(main):
        op = main[i]
        n += 1
        if op[0] == "BGS":
            CM.run(_job_slice(job, op[1] - len(main)), st)
        elif op[0] in ("JN", "RUNJ"):
            pass
        elif op[0] == "RUNS":
            j = i + 1
            while main[j][0] != "RUNJ":
                assert main[j][0] == "LDP"
                CM.run([main[j]], st)
                j += 1
            CM.run([("RUN", op[1])], st)
            n += j - i - 1
            i = j
            continue
        else:
            CM.run([op], st)
        i += 1
    return n


def encode(op) -> int:
    o = op[0]
    if o == "RUNS":
        _, prog, mask = op
        assert 0 <= prog < 4 and 0 <= mask < 4096
        return (OPC["RUNS"] << 36) | (prog << 34) | (mask << 22)
    if o == "RUNJ":
        return OPC["RUNJ"] << 36
    return M2.encode(op)


def check_static3():
    """Static checks of test_plan_9i4.md section 2 item 6: the checks of model2 on these programs, plus the structure of RUNS / LDP / RUNJ."""
    saved = M2.PROGRAMS2
    M2.PROGRAMS2 = PROGRAMS3
    try:
        M2.check_static2()
    finally:
        M2.PROGRAMS2 = saved
    import kpke_smp_model as KM
    eng = KM.programs(KM.OVERLAP)
    names = {v: k for k, v in ENGINE.items()}
    for name, prog in PROGRAMS3.items():
        main, _ = split(prog)
        opens = [k for k, op in enumerate(main) if op[0] == "RUNS"]
        closes = [k for k, op in enumerate(main) if op[0] == "RUNJ"]
        assert len(opens) == len(closes), name
        for a, b in zip(opens, closes):
            assert a < b, name
            between = main[a + 1: b]
            assert all(op[0] == "LDP" for op in between), (name, "only loads between RUNS and RUNJ", between)
            slots = [op[1] for op in between]
            assert len(set(slots)) == len(slots), (name, "a slot loaded twice")
            assert main[a][2] == _mask(between), (name, "the mask is not the set of loaded slots")
            # a loaded slot is not written by the engine program before... every engine operation that touches it waits for the load (hardware); here: the slot is used by the engine program at all
            ep = eng[names[main[a][1]]]
            used = {x for op in ep for x in (op[1], op[2], op[3]) if op[0] in (1, 2, 3, 4, 5, 6, 7, 8)}
            assert all(s in used for s in slots), (name, "a loaded slot that the engine program never uses", slots)
        # no run of the engine without a join, and END only after the last join
        assert not closes or closes[-1] < len(main) - 1, name
        for a, b in zip(opens, closes):
            for op in main[a:b + 1]:
                assert op[0] not in ("STP", "SDL", "RUN", "HST", "HFD", "HGT", "WR32", "RD32", "CMP", "END"), (name, op)
        assert len(prog) <= 64, name
    return True


def keygen(d, z):
    st = State()
    st.set_reg(R_D, d)
    st.set_reg(R_Z, z)
    run3(PROGRAMS3["keygen"], st)
    from params import DK_BYTES, EK_BYTES
    return bytes(st.mem[KB][8 * OFF_EK: 8 * OFF_EK + EK_BYTES]), bytes(st.mem[KB][:DK_BYTES])


def encaps(ek, m):
    st = State()
    st.mem[KB][8 * OFF_EK: 8 * OFF_EK + len(ek)] = ek
    st.set_reg(R_M, m)
    run3(PROGRAMS3["encaps"], st)
    from params import CT_BYTES
    return st.reg(R_K), bytes(st.mem[CBR][:CT_BYTES])


def decaps(dk, c):
    from params import CT_BYTES, DK_BYTES
    st = State()
    st.mem[KB][:DK_BYTES] = dk
    st.mem[CBR][:CT_BYTES] = c
    run3(PROGRAMS3["decaps"], st)
    return st.reg(R_K)
