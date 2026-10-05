"""tb/golden/mlkem_ctl_model2.py

Phase 9F step S1b (evidence/phase9m/batch1/9f1b/test_plan_9f1b.md): the controller micro-programs of tb/golden/mlkem_ctl_model.py with the hash that does not depend on the work next to it moved into a background job:
two new micro-operations ("BGS", pc) start the job whose words (HST, HFD..., HGT, END) are stored after the main program at word pc, and ("JN",) waits until the job has finished (including the write of the digest).
Functionally the job is computed when it starts (the result is the same as in the Phase 9 programs); `check_static2` proves that the program never uses the hash unit, the job's destination registers or a word range that the job reads between BGS and JN, so that the order of execution cannot change a value.
Independent of any RTL. The Phase 9 model is not changed.
"""
from __future__ import annotations

import mlkem_ctl_model as CM
from mlkem_ctl_model import (CB2R, CBR, K, KB, KB_W, OFF_EK, OFF_H, OFF_RHO, OFF_Z, PROG_ID, RFR, R_D, R_HH, R_K, R_KBAR, R_M, R_RHO, R_SD, R_Z, SRC_CONST, G_SEL, H_SEL, J_SEL, ENGINE, State, _reencrypt)

OPC = {**CM.OPC, "BGS": 11, "JN": 12}


def _keygen():
    p = [("HST", G_SEL, 33), ("HFD", RFR, 4 * R_D, 4), ("HFD", SRC_CONST, 0, 1), ("HGT", R_RHO, R_SD), ("SDL",), ("RUN", ENGINE["keygen"])]
    p += [("STP", 3 + i, KB, OFF_EK + 48 * i, 12) for i in range(K)]       # t_hat -> ek
    p += [("WR32", R_RHO, OFF_RHO), ("BGS", None)]                         # H(ek) in the background during the stores of s_hat
    p += [("STP", i, KB, 48 * i, 12) for i in range(K)]                    # s_hat -> dk_pke
    p += [("JN",), ("WR32", R_HH, OFF_H), ("WR32", R_Z, OFF_Z), ("END",)]
    job = [("HST", H_SEL, 1184), ("HFD", KB, OFF_EK, 148), ("HGT", R_HH, 0), ("END",)]
    return p, [job]


def _encaps():
    p = [("BGS", None), ("RD32", R_RHO, OFF_RHO)]                          # H(ek) in the background during the loads
    p += [("LDP", 7 + j, KB, OFF_EK + 48 * j, 12) for j in range(K)]
    p += [("LDP", 11, RFR, 4 * R_M, 1), ("JN",)]
    p += [("HST", G_SEL, 64), ("HFD", RFR, 4 * R_M, 4), ("HFD", RFR, 4 * R_HH, 4), ("HGT", R_K, R_SD)]
    p += [("SDL",), ("RUN", ENGINE["encrypt"])]
    p += [("STP", 3 + i, CBR, 40 * i, 10) for i in range(K)] + [("STP", 10, CBR, 120, 4), ("END",)]
    job = [("HST", H_SEL, 1184), ("HFD", KB, OFF_EK, 148), ("HGT", R_HH, 0), ("END",)]
    return p, [job]


def _decaps():
    p = [("BGS", None)]                                                    # J(z || c) in the background during the loads and the decryption
    p += [("LDP", 3 + i, CBR, 40 * i, 10) for i in range(K)]
    p += [("LDP", 10, CBR, 120, 4)]
    p += [("LDP", i, KB, 48 * i, 12) for i in range(K)]
    p += [("RUN", ENGINE["decrypt"]), ("STP", 10, RFR, 4 * R_M, 1), ("JN",)]
    p += [("HST", G_SEL, 64), ("HFD", RFR, 4 * R_M, 4), ("HFD", KB, OFF_H, 4), ("HGT", R_K, R_SD)]
    p += _reencrypt(CB2R) + [("CMP",), ("END",)]
    job = [("HST", J_SEL, 1120), ("HFD", KB, OFF_Z, 4), ("HFD", CBR, 0, 136), ("HGT", R_KBAR, 0), ("END",)]
    return p, [job]


def build():
    """Returns {name: (main ops with BGS resolved to the word address of its job, job words)}; the layout is main program, then the job."""
    out = {}
    for name, f in (("keygen", _keygen), ("encaps", _encaps), ("decaps", _decaps)):
        main, jobs = f()
        base = len(main)
        res = []
        for op in main:
            res.append(("BGS", base) if op[0] == "BGS" else op)
        flat = res + [w for j in jobs for w in j]
        out[name] = (flat, base)
    return out


PROGRAMS2 = {n: v[0] for n, v in build().items()}
JOB_PC = {n: v[1] for n, v in build().items()}


def split(prog):
    """(main part up to the first END, job words after it)."""
    i = [k for k, op in enumerate(prog) if op[0] == "END"][0]
    return prog[: i + 1], prog[i + 1:]


def run2(prog, st: State):
    """Runs a program of this model: BGS computes the job at once (same values), JN is a marker."""
    main, job = split(prog)
    n = 0
    for op in main:
        n += 1
        if op[0] == "BGS":
            pc = op[1] - len(main)
            CM.run(_job_slice(job, pc), st)
        elif op[0] == "JN":
            continue
        else:
            CM.run([op], st)
    return n


def _job_slice(job, pc):
    out = []
    for op in job[pc:]:
        out.append(op)
        if op[0] == "END":
            break
    return out


def encode(op) -> int:
    o = op[0]
    if o == "BGS":
        assert 0 <= op[1] < 64
        return (OPC["BGS"] << 36) | (op[1] << 30)
    if o == "JN":
        return OPC["JN"] << 36
    return CM.encode(op)


def check_static2():
    """Static checks of test_plan_9f1b.md section 2 item 7."""
    sizes = {KB: KB_W, CBR: CM.CB_W, CB2R: CM.CB2_W, RFR: CM.RF_W}
    for name, prog in PROGRAMS2.items():
        main, job = split(prog)
        assert len(prog) <= 64, name
        assert all(op[0] != "END" for op in main[:-1]), name
        bgs = [k for k, op in enumerate(main) if op[0] == "BGS"]
        jn = [k for k, op in enumerate(main) if op[0] == "JN"]
        assert len(bgs) == len(jn) == 1 and bgs[0] < jn[0] < len(main) - 1, name
        pc = main[bgs[0]][1] - len(main)
        jb = _job_slice(job, pc)
        assert jb[-1][0] == "END" and [o[0] for o in jb[:-1]][0] == "HST" and jb[-2][0] == "HGT", (name, jb)
        assert all(o[0] in ("HST", "HFD", "HGT", "END") for o in jb), (name, jb)
        hl, fed, reads, dst = 0, 0, [], []
        for op in jb:
            encode(op)
            if op[0] == "HST":
                hl = op[2]
            if op[0] == "HFD":
                fed += 8 if op[1] == SRC_CONST else 8 * op[3]
                if op[1] != SRC_CONST:
                    assert op[2] + op[3] <= sizes[op[1]], (name, op)
                    reads.append((op[1], op[2], op[2] + op[3]))
            if op[0] == "HGT":
                assert fed >= hl, (name, op)
                dst = [op[1]] + ([op[2]] if jb[0][1] == G_SEL else [])
        between = main[bgs[0] + 1: jn[0]]
        for op in between:
            assert op[0] not in ("HST", "HFD", "HGT"), (name, "main hash while the job runs", op)
            if op[0] in ("WR32", "RD32"):
                assert op[1] not in dst or False, (name, "job destination register touched", op)
                if op[0] == "WR32":
                    assert not any(r == KB and op[2] < hi and op[2] + 4 > lo for r, lo, hi in reads), (name, "write into a word range the job reads", op)
            if op[0] == "STP":
                assert not any(r == op[2] and op[3] < hi and op[3] + 4 * op[4] > lo for r, lo, hi in reads), (name, "store into a word range the job reads", op)
        # registers: nothing between BGS and JN reads or writes a destination register of the job (SDL reads registers 3 and 4, RUN is independent of them after SDL)
        for op in between:
            if op[0] == "SDL":
                assert not set(dst) & {R_RHO, R_SD}, (name, op)
            if op[0] == "LDP" and op[2] == RFR:
                assert op[3] // 4 not in dst, (name, op)
            if op[0] == "STP" and op[2] == RFR:
                assert op[3] // 4 not in dst, (name, op)
            if op[0] == "CMP":
                raise AssertionError((name, "CMP between BGS and JN"))
        # after JN a result register may be read; before BGS the job's inputs must be final: no later main write to the inputs (checked on the main part after BGS above for stores; registers are not inputs of the jobs)
    return True


def keygen(d, z):
    st = State()
    st.set_reg(R_D, d)
    st.set_reg(R_Z, z)
    run2(PROGRAMS2["keygen"], st)
    from params import DK_BYTES, EK_BYTES
    return bytes(st.mem[KB][8 * OFF_EK: 8 * OFF_EK + EK_BYTES]), bytes(st.mem[KB][:DK_BYTES])


def encaps(ek, m):
    from params import CT_BYTES, EK_BYTES  # noqa: F401
    st = State()
    st.mem[KB][8 * OFF_EK: 8 * OFF_EK + len(ek)] = ek
    st.set_reg(R_M, m)
    run2(PROGRAMS2["encaps"], st)
    return st.reg(R_K), bytes(st.mem[CBR][:CT_BYTES])


def decaps(dk, c):
    from params import CT_BYTES, DK_BYTES
    st = State()
    st.mem[KB][:DK_BYTES] = dk
    st.mem[CBR][:CT_BYTES] = c
    run2(PROGRAMS2["decaps"], st)
    return st.reg(R_K)
