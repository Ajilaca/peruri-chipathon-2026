"""tb/golden/keccak.py

Golden Keccak-f[1600] and sponge (FIPS 202), independent of any RTL (Phase 7, docs/evidence/phase07-keccak/test_plan.md).

State: 25 lanes of 64 bit, lane index x + 5y (FIPS 202 Section 3.1.2 with A[x, y] = lane[x + 5y]). Byte i of the state string is byte (i mod 8)
of lane (i div 8), little endian (FIPS 202 Section 3.1.3). The round constants are computed with the rc(t) LFSR (Algorithm 5) and the rho offsets with
Algorithm 2; neither table is typed in. Everything is checked against hashlib in tb/golden/tests/test_keccak.py; no number here is a measurement.
"""

M64 = (1 << 64) - 1
ROUNDS = 24

# (name, rate in bytes, domain-separation byte, fixed output length in bytes or None for an XOF); FIPS 202 Table 3 and Section 6.
MODES = {
    "sha3_256": (136, 0x06, 32),
    "sha3_512": (72, 0x06, 64),
    "shake_128": (168, 0x1F, None),
    "shake_256": (136, 0x1F, None),
}


def rol(v: int, n: int) -> int:
    n %= 64
    return ((v << n) | (v >> (64 - n))) & M64 if n else v


def _rc_bit(t: int) -> int:
    """FIPS 202 Algorithm 5, rc(t)."""
    t %= 255
    if t == 0:
        return 1
    r = [1, 0, 0, 0, 0, 0, 0, 0]  # R = 10000000, R[0] first
    for _ in range(t):
        r = [0] + r  # 0 || R
        r[0] ^= r[8]
        r[4] ^= r[8]
        r[5] ^= r[8]
        r[6] ^= r[8]
        r = r[:8]
    return r[0]


def _round_constant(ir: int) -> int:
    """FIPS 202 Algorithm 6, RC[ir] as a 64-bit lane."""
    rc = 0
    for j in range(7):
        rc |= _rc_bit(j + 7 * ir) << ((1 << j) - 1)
    return rc


def _rho_offsets() -> list[int]:
    """FIPS 202 Algorithm 2: offset of lane x + 5y."""
    off = [0] * 25
    x, y = 1, 0
    for t in range(24):
        off[x + 5 * y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    return off


RC = [_round_constant(i) for i in range(ROUNDS)]
RHO = _rho_offsets()


def theta(a: list[int]) -> list[int]:
    c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
    d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
    return [a[i] ^ d[i % 5] for i in range(25)]


def rho(a: list[int]) -> list[int]:
    return [rol(a[i], RHO[i]) for i in range(25)]


def pi(a: list[int]) -> list[int]:
    out = [0] * 25
    for x in range(5):
        for y in range(5):
            out[y + 5 * ((2 * x + 3 * y) % 5)] = a[x + 5 * y]  # B[y, 2x + 3y] = A[x, y]
    return out


def chi(a: list[int]) -> list[int]:
    out = [0] * 25
    for y in range(5):
        for x in range(5):
            out[x + 5 * y] = a[x + 5 * y] ^ ((~a[(x + 1) % 5 + 5 * y] & M64) & a[(x + 2) % 5 + 5 * y])
    return out


def iota(a: list[int], ir: int) -> list[int]:
    out = list(a)
    out[0] ^= RC[ir]
    return out


def keccak_round(a: list[int], ir: int) -> list[int]:
    return iota(chi(pi(rho(theta(a)))), ir)


def keccak_f1600(a: list[int]) -> list[int]:
    assert len(a) == 25
    for ir in range(ROUNDS):
        a = keccak_round(a, ir)
    return a


def keccak_trace(a: list[int]) -> list[list[int]]:
    """State after each of the 24 rounds (index ir = state after round ir)."""
    out = []
    for ir in range(ROUNDS):
        a = keccak_round(a, ir)
        out.append(a)
    return out


def state_to_bytes(a: list[int]) -> bytes:
    return b"".join(v.to_bytes(8, "little") for v in a)


def bytes_to_state(b: bytes) -> list[int]:
    assert len(b) == 200
    return [int.from_bytes(b[8 * i: 8 * i + 8], "little") for i in range(25)]


def pad(rate: int, ds: int, length: int) -> bytes:
    """Padding bytes appended to a message of `length` bytes (pad10*1 with the domain bits folded into `ds`): total length becomes a multiple of rate."""
    n = rate - (length % rate)
    if n == 1:
        return bytes([ds | 0x80])
    return bytes([ds]) + bytes(n - 2) + b"\x80"


def sponge(rate: int, ds: int, msg: bytes, outlen: int) -> bytes:
    st = bytes(200)
    m = msg + pad(rate, ds, len(msg))
    for off in range(0, len(m), rate):
        blk = bytes(a ^ b for a, b in zip(st[:rate], m[off: off + rate])) + st[rate:]
        st = state_to_bytes(keccak_f1600(bytes_to_state(blk)))
    out = b""
    while True:
        out += st[:rate]
        if len(out) >= outlen:
            return out[:outlen]
        st = state_to_bytes(keccak_f1600(bytes_to_state(st)))


def _digest(mode: str, msg: bytes, outlen: int | None) -> bytes:
    rate, ds, fixed = MODES[mode]
    if fixed is not None:
        assert outlen is None or outlen == fixed
        outlen = fixed
    assert outlen is not None
    return sponge(rate, ds, msg, outlen)


def sha3_256(msg: bytes) -> bytes:
    return _digest("sha3_256", msg, None)


def sha3_512(msg: bytes) -> bytes:
    return _digest("sha3_512", msg, None)


def shake_128(msg: bytes, outlen: int) -> bytes:
    return _digest("shake_128", msg, outlen)


def shake_256(msg: bytes, outlen: int) -> bytes:
    return _digest("shake_256", msg, outlen)


def num_perms(mode: str, length: int, outlen: int | None = None) -> int:
    """Number of Keccak-f permutations a hash call uses: floor(len / rate) + 1 absorb, plus ceil(out / rate) - 1 extra squeeze (0 when out <= rate)."""
    rate, _, fixed = MODES[mode]
    out = fixed if fixed is not None else outlen
    assert out is not None
    squeeze = max(0, -(-out // rate) - 1)
    return length // rate + 1 + squeeze
