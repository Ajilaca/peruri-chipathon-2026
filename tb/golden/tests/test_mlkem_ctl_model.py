"""tb/golden/tests/test_mlkem_ctl_model.py -- Phase 9c test plan V2: the micro-programs of tb/golden/mlkem_ctl_model.py reproduce every pinned ACVP vector of ML-KEM-768 and the unmodified golden ml_kem_*_internal functions."""
import random

import mlkem_ctl_model as CM
from fetch_acvp_vectors import dest_path
from mlkem import ml_kem_decaps_internal, ml_kem_encaps_internal, ml_kem_keygen_internal
from params import CT_BYTES

import json


def _groups(subdir, fn):
    doc = json.loads(dest_path(subdir).read_text())
    return [tg for tg in doc["testGroups"] if tg["parameterSet"] == "ML-KEM-768" and tg["tests"] and fn(tg)]


def test_static_checks():
    assert CM.check_static()


def test_keygen_matches_acvp():
    n = 0
    for tg in _groups("ML-KEM-keyGen-FIPS203", lambda tg: True):
        for t in tg["tests"]:
            ek, dk = CM.keygen(bytes.fromhex(t["d"]), bytes.fromhex(t["z"]))
            assert ek.hex() == t["ek"].lower() and dk.hex() == t["dk"].lower(), t["tcId"]
            n += 1
    assert n == 25


def test_encaps_and_decaps_match_acvp():
    ne = nd = 0
    for tg in _groups("ML-KEM-encapDecap-FIPS203", lambda tg: tg["function"] == "encapsulation"):
        for t in tg["tests"]:
            k, c = CM.encaps(bytes.fromhex(t["ek"]), bytes.fromhex(t["m"]))
            assert c.hex() == t["c"].lower() and k.hex() == t["k"].lower(), t["tcId"]
            ne += 1
    for tg in _groups("ML-KEM-encapDecap-FIPS203", lambda tg: tg["function"] == "decapsulation"):
        for t in tg["tests"]:
            assert CM.decaps(bytes.fromhex(t["dk"]), bytes.fromhex(t["c"])).hex() == t["k"].lower(), t["tcId"]
            nd += 1
    assert (ne, nd) == (25, 10)


def test_random_equals_unmodified_golden_and_roundtrip():
    rng = random.Random(970)
    for _ in range(3):
        d, z, m = (bytes(rng.randrange(256) for _ in range(32)) for _ in range(3))
        ek, dk = CM.keygen(d, z)
        assert (ek, dk) == ml_kem_keygen_internal(d, z)
        k, c = CM.encaps(ek, m)
        assert (k, c) == ml_kem_encaps_internal(ek, m)
        assert CM.decaps(dk, c) == k == ml_kem_decaps_internal(dk, c)
        for pos in (0, CT_BYTES - 1, 960, rng.randrange(CT_BYTES)):
            bad = bytearray(c)
            bad[pos] ^= 1 << rng.randrange(8)
            assert CM.decaps(dk, bytes(bad)) == ml_kem_decaps_internal(dk, bytes(bad)) != k
