"""tb/golden/mlkem_ctl_model.py

Golden model of the Phase 9c controller micro-programs (docs/evidence/phase09-integration/9c/test_plan_9c.md): the schedules of ML-KEM.KeyGen_internal, Encaps_internal and Decaps_internal (FIPS 203 Algorithms 16-18) as straight-line
lists of micro-operations on byte buffers, registers and the K-PKE engine slots, run with the unmodified golden primitives (`primitives`), the codec model of 9a (`codec_model`), the comparison model of 9b (`fo_model`) and the K-PKE program model of 8d (`kpke_smp_model`, OVERLAP).
The same program lists are turned into the RTL ROM by scripts/gen_mlkem_ctl_rom.py. Independent of any RTL.

Memories (64-bit words, byte k of word w is byte 8w + k): KB 300 words (the layout of dk: dk_pke word 0, ek word 144, rho of ek word 288, H(ek) word 292, z word 296), CB 136 words (ciphertext), CB2 136 words (re-encrypted ciphertext),
RF 32 words = registers 0 d, 1 z, 2 m, 3 rho, 4 sigma / r, 5 K, 6 K_bar, 7 H(ek) of 4 words each. Engine slots: 12 hardware slots (hardware slot = Phase 6 logical slot - 9).
Micro-operations (tuples): ("LDP", slot, region, woff, d) / ("STP", ...), ("HST", sel, len), ("HFD", src, woff, nwords), ("HGT", dstA, dstB), ("SDL",), ("RUN", prog), ("WR32", reg, woff), ("RD32", reg, woff), ("CMP",), ("END",).
"""
from __future__ import annotations

import hashlib

import codec_model as C
import fo_model as F
import kpke_smp_model as M
from params import DK_BYTES, CT_BYTES, EK_BYTES

KB_W, CB_W, CB2_W, RF_W = 300, 136, 136, 32
KB, CBR, CB2R, RFR = 0, 1, 2, 3                       # region codes (CBR / CB2R to avoid clashing with the buffer names)
SRC_CONST = 4                                         # HFD source: the constant word 0x03
R_D, R_Z, R_M, R_RHO, R_SD, R_K, R_KBAR, R_HH = range(8)
H_SEL, G_SEL, J_SEL = 0, 1, 2
DSEL = {1: 0, 4: 1, 10: 2, 12: 3}
OPC = {"END": 0, "LDP": 1, "STP": 2, "HST": 3, "HFD": 4, "HGT": 5, "SDL": 6, "RUN": 7, "WR32": 8, "RD32": 9, "CMP": 10}
PROG_ID = {"keygen": 0, "encaps": 1, "decaps": 2}
ENGINE = {"keygen": 0, "encrypt": 1, "decrypt": 2}
OFF_EK, OFF_RHO, OFF_H, OFF_Z = 144, 288, 292, 296    # KB word offsets
K = 3


def _prog_keygen():
    p = [("HST", G_SEL, 33), ("HFD", RFR, 4 * R_D, 4), ("HFD", SRC_CONST, 0, 1), ("HGT", R_RHO, R_SD), ("SDL",), ("RUN", ENGINE["keygen"])]
    p += [("STP", 3 + i, KB, OFF_EK + 48 * i, 12) for i in range(K)]       # t_hat -> ek
    p += [("STP", i, KB, 48 * i, 12) for i in range(K)]                    # s_hat -> dk_pke
    p += [("WR32", R_RHO, OFF_RHO), ("HST", H_SEL, 1184), ("HFD", KB, OFF_EK, 148), ("HGT", R_HH, 0), ("WR32", R_HH, OFF_H), ("WR32", R_Z, OFF_Z), ("END",)]
    return p


def _reencrypt(dst):
    """Encrypt of the engine from ek in KB, the message polynomial in register 2 and sigma / r in register 4, ciphertext into region dst."""
    p = [("RD32", R_RHO, OFF_RHO)]
    p += [("LDP", 7 + j, KB, OFF_EK + 48 * j, 12) for j in range(K)]
    p += [("LDP", 11, RFR, 4 * R_M, 1), ("SDL",), ("RUN", ENGINE["encrypt"])]
    p += [("STP", 3 + i, dst, 40 * i, 10) for i in range(K)]
    p += [("STP", 10, dst, 120, 4)]
    return p


def _prog_encaps():
    p = [("HST", H_SEL, 1184), ("HFD", KB, OFF_EK, 148), ("HGT", R_HH, 0)]
    p += [("HST", G_SEL, 64), ("HFD", RFR, 4 * R_M, 4), ("HFD", RFR, 4 * R_HH, 4), ("HGT", R_K, R_SD)]
    p += _reencrypt(CBR) + [("END",)]
    return p


def _prog_decaps():
    p = [("LDP", 3 + i, CBR, 40 * i, 10) for i in range(K)]
    p += [("LDP", 10, CBR, 120, 4)]
    p += [("LDP", i, KB, 48 * i, 12) for i in range(K)]
    p += [("RUN", ENGINE["decrypt"]), ("STP", 10, RFR, 4 * R_M, 1)]
    p += [("HST", G_SEL, 64), ("HFD", RFR, 4 * R_M, 4), ("HFD", KB, OFF_H, 4), ("HGT", R_K, R_SD)]
    p += [("HST", J_SEL, 1120), ("HFD", KB, OFF_Z, 4), ("HFD", CBR, 0, 136), ("HGT", R_KBAR, 0)]
    p += _reencrypt(CB2R) + [("CMP",), ("END",)]
    return p


PROGRAMS = {"keygen": _prog_keygen(), "encaps": _prog_encaps(), "decaps": _prog_decaps()}


class State:
    def __init__(self):
        self.mem = {KB: bytearray(8 * KB_W), CBR: bytearray(8 * CB_W), CB2R: bytearray(8 * CB2_W), RFR: bytearray(8 * RF_W)}
        self.slots = M.empty_slots(M.OVERLAP)
        self.eng_rho = self.eng_sd = bytes(32)
        self.msg = b""
        self.hsel = None
        self.hlen = 0
        self.digest = b""

    def reg(self, r):
        return bytes(self.mem[RFR][32 * r: 32 * r + 32])

    def set_reg(self, r, b):
        assert len(b) == 32
        self.mem[RFR][32 * r: 32 * r + 32] = b


def run(program, st: State):
    """Runs a micro-program. Returns the number of micro-operations executed (the program is straight-line)."""
    n = 0
    for op in program:
        n += 1
        o = op[0]
        if o == "LDP":
            _, slot, rgn, woff, d = op
            data = bytes(st.mem[rgn][8 * woff: 8 * woff + 32 * d])
            st.slots[slot] = C.unpack_poly(d, data)
        elif o == "STP":
            _, slot, rgn, woff, d = op
            st.mem[rgn][8 * woff: 8 * woff + 32 * d] = C.pack_poly(d, st.slots[slot])
        elif o == "HST":
            st.hsel, st.hlen, st.msg = op[1], op[2], b""
        elif o == "HFD":
            _, src, woff, nw = op
            st.msg += (bytes([3]) + bytes(7)) if src == SRC_CONST else bytes(st.mem[src][8 * woff: 8 * (woff + nw)])
        elif o == "HGT":
            _, da, db = op
            m = st.msg[: st.hlen]
            assert len(m) == st.hlen, "message shorter than the hash length"
            if st.hsel == H_SEL:
                st.set_reg(da, hashlib.sha3_256(m).digest())
            elif st.hsel == G_SEL:
                dg = hashlib.sha3_512(m).digest()
                st.set_reg(da, dg[:32])
                st.set_reg(db, dg[32:])
            else:
                st.set_reg(da, hashlib.shake_256(m).digest(32))
        elif o == "SDL":
            st.eng_rho, st.eng_sd = st.reg(R_RHO), st.reg(R_SD)
        elif o == "RUN":
            name = {v: k for k, v in ENGINE.items()}[op[1]]
            M.run(M.programs(M.OVERLAP)[name], st.slots, st.eng_rho, st.eng_sd)
        elif o == "WR32":
            _, r, woff = op
            st.mem[KB][8 * woff: 8 * woff + 32] = st.reg(r)
        elif o == "RD32":
            _, r, woff = op
            st.set_reg(r, bytes(st.mem[KB][8 * woff: 8 * woff + 32]))
        elif o == "CMP":
            st.set_reg(R_K, F.fo_select(bytes(st.mem[CBR]), bytes(st.mem[CB2R]), st.reg(R_K), st.reg(R_KBAR)))
        elif o == "END":
            break
        else:
            raise ValueError(op)
    return n


def keygen(d: bytes, z: bytes):
    st = State()
    st.set_reg(R_D, d)
    st.set_reg(R_Z, z)
    run(PROGRAMS["keygen"], st)
    ek, dk = bytes(st.mem[KB][8 * OFF_EK: 8 * OFF_EK + EK_BYTES]), bytes(st.mem[KB][: DK_BYTES])
    return ek, dk


def encaps(ek: bytes, m: bytes):
    st = State()
    st.mem[KB][8 * OFF_EK: 8 * OFF_EK + EK_BYTES] = ek
    st.set_reg(R_M, m)
    run(PROGRAMS["encaps"], st)
    return st.reg(R_K), bytes(st.mem[CBR][:CT_BYTES])


def decaps(dk: bytes, c: bytes):
    st = State()
    st.mem[KB][:DK_BYTES] = dk
    st.mem[CBR][:CT_BYTES] = c
    run(PROGRAMS["decaps"], st)
    return st.reg(R_K)


def encode(op) -> int:
    """40-bit micro-instruction word of an operation (field layout of rtl/mlkem/mlkem_ctl_rom.sv)."""
    o = op[0]
    w = OPC[o] << 36
    if o in ("LDP", "STP"):
        _, slot, rgn, woff, d = op
        assert 0 <= slot < 12 and 0 <= rgn < 4 and 0 <= woff < 512 and d in DSEL
        w |= (slot << 32) | (rgn << 30) | (woff << 21) | (DSEL[d] << 19)
    elif o == "HST":
        _, sel, ln = op
        assert 0 <= sel < 3 and 0 <= ln < 2048
        w |= (sel << 34) | (ln << 23)
    elif o == "HFD":
        _, src, woff, nw = op
        assert 0 <= src <= 4 and 0 <= woff < 512 and 0 <= nw < 512
        w |= (src << 33) | (woff << 24) | (nw << 15)
    elif o == "HGT":
        _, da, db = op
        assert 0 <= da < 8 and 0 <= db < 8
        w |= (da << 33) | (db << 30)
    elif o in ("WR32", "RD32"):
        _, r, woff = op
        assert 0 <= r < 8 and 0 <= woff < 512
        w |= (r << 33) | (woff << 24)
    elif o == "RUN":
        assert 0 <= op[1] < 3
        w |= op[1] << 34
    return w


def check_static(programs=None):
    """Static checks of the micro-programs: straight-line, one END at the end, fields in range (encode asserts), HFD supplies at least the hash length, regions stay inside their memory."""
    sizes = {KB: KB_W, CBR: CB_W, CB2R: CB2_W, RFR: RF_W}
    for name, prog in (programs or PROGRAMS).items():
        assert prog[-1][0] == "END" and all(op[0] != "END" for op in prog[:-1]), name
        hl, fed = 0, 0
        for op in prog:
            encode(op)
            if op[0] in ("LDP", "STP"):
                assert op[3] + 4 * op[4] <= sizes[op[2]], (name, op)
            if op[0] == "HST":
                hl, fed = op[2], 0
            if op[0] == "HFD":
                fed += 8 if op[1] == SRC_CONST else 8 * op[3]
                if op[1] != SRC_CONST:
                    assert op[2] + op[3] <= sizes[op[1]], (name, op)
            if op[0] == "HGT":
                assert fed >= hl, (name, op)
            if op[0] in ("WR32", "RD32"):
                assert op[2] + 4 <= KB_W
    return True
