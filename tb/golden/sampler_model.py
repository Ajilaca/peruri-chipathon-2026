"""tb/golden/sampler_model.py

Golden model of the Phase 8b streaming samplers (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md), independent of any RTL.
The coefficients and the byte counts come from the same algorithms as FIPS 203 Algorithm 7 (SampleNTT) and Algorithm 8 (SamplePolyCBD_eta, eta = 2 here: ETA1 = ETA2 = 2 for ML-KEM-768), but written
to work on an arbitrary byte stream and to report how many stream bytes were consumed; they are checked against the unmodified golden `primitives.sample_ntt` and `primitives.sample_poly_cbd`
in tb/golden/tests/test_sampler_model.py.
"""
from params import N, Q


def sample_ntt_stream(stream: bytes) -> tuple[list[int], int, int]:
    """SampleNTT over a byte stream. Returns (256 coefficients, bytes consumed, triples consumed) or raises ValueError when the stream ends first.
    Consumption is 3 bytes per triple, counting the triple that completes the polynomial (also when its second candidate is not used)."""
    a = []
    pos = 0
    while len(a) < N:
        if pos + 3 > len(stream):
            raise ValueError("stream too short")
        b0, b1, b2 = stream[pos], stream[pos + 1], stream[pos + 2]
        pos += 3
        d1 = b0 + 256 * (b1 % 16)
        d2 = (b1 // 16) + 16 * b2
        if d1 < Q:
            a.append(d1)
        if d2 < Q and len(a) < N:
            a.append(d2)
    return a, pos, pos // 3


def cbd2(b: bytes) -> list[int]:
    """SamplePolyCBD_2 over 128 bytes: coefficient i uses bits 4i..4i+3 (x = bit0 + bit1, y = bit2 + bit3, f = x - y mod q); byte k gives coefficients 2k (low nibble) and 2k + 1 (high nibble)."""
    assert len(b) == 128
    out = []
    for byte in b:
        for nib in (byte & 15, byte >> 4):
            x = (nib & 1) + ((nib >> 1) & 1)
            y = ((nib >> 2) & 1) + ((nib >> 3) & 1)
            out.append((x - y) % Q)
    return out
