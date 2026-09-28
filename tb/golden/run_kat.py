"""tb/golden/run_kat.py

Compares the ML-KEM-768 golden model (tb/golden/mlkem.py) bit-exactly
against NIST's official ACVP known-answer test vectors, using ONLY the
ML-KEM-768 test groups from the two files fetched by
tb/golden/fetch_acvp_vectors.py (tb/vectors/acvp/*.json).

Five ACVP functions are checked, each against the model function that
implements the same FIPS 203 algorithm:
  - keyGen                  -> ml_kem_keygen_internal(d, z)            (Alg 16)
  - encapsulation            -> ml_kem_encaps_internal(ek, m)           (Alg 17)
  - decapsulation             -> ml_kem_decaps_internal(dk, c)          (Alg 18,
    including "modified ciphertext" cases, which exercise implicit rejection)
  - encapsulationKeyCheck    -> check_encapsulation_key(ek)             (Sec 7.2)
  - decapsulationKeyCheck    -> check_decapsulation_input(dk, <dummy c
    of the correct length>) (Sec 7.3; the ACVP decapsulationKeyCheck test
    supplies no ciphertext, so only the dk-length and H(ek_PKE) checks are
    exercised here -- the dummy c's content is irrelevant, only its length
    32*(du*k+dv) matters to the check)

Hex strings are compared case-insensitively. Nothing here changes the
vectors, the comparison, or adds any tolerance; a mismatch is reported,
not hidden.

Usage: python3 tb/golden/run_kat.py
Requires tb/vectors/acvp/*.json to already exist (run
tb/golden/fetch_acvp_vectors.py first).
"""

from __future__ import annotations

import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from fetch_acvp_vectors import BASE_URL, FILES, PINNED_COMMIT, dest_path  # noqa: E402
from mlkem import (  # noqa: E402
    check_decapsulation_input,
    check_encapsulation_key,
    ml_kem_decaps_internal,
    ml_kem_encaps_internal,
    ml_kem_keygen_internal,
)
from params import CT_BYTES  # noqa: E402

PARAMETER_SET = "ML-KEM-768"


def _hex_eq(a: str, b: str) -> bool:
    return a.lower() == b.lower()


def _load(subdir: str) -> dict:
    path = dest_path(subdir)
    if not path.exists():
        raise SystemExit(
            f"{path} not found. Run: python3 tb/golden/fetch_acvp_vectors.py"
        )
    return json.loads(path.read_text())


def _groups_for(doc: dict, parameter_set: str = PARAMETER_SET) -> list[dict]:
    return [tg for tg in doc["testGroups"] if tg["parameterSet"] == parameter_set]


def run_keygen_group(tg: dict) -> dict:
    results = []
    for t in tg["tests"]:
        d = bytes.fromhex(t["d"])
        z = bytes.fromhex(t["z"])
        ek, dk = ml_kem_keygen_internal(d, z)
        ok = _hex_eq(ek.hex(), t["ek"]) and _hex_eq(dk.hex(), t["dk"])
        results.append((t["tcId"], ok))
    return _summarize(tg, "keyGen", results)


def run_encapsulation_group(tg: dict) -> dict:
    results = []
    for t in tg["tests"]:
        ek = bytes.fromhex(t["ek"])
        m = bytes.fromhex(t["m"])
        K, c = ml_kem_encaps_internal(ek, m)
        ok = _hex_eq(c.hex(), t["c"]) and _hex_eq(K.hex(), t["k"])
        results.append((t["tcId"], ok))
    return _summarize(tg, "encapsulation", results)


def run_decapsulation_group(tg: dict) -> dict:
    results = []
    for t in tg["tests"]:
        dk = bytes.fromhex(t["dk"])
        c = bytes.fromhex(t["c"])
        K = ml_kem_decaps_internal(dk, c)
        ok = _hex_eq(K.hex(), t["k"])
        results.append((t["tcId"], ok, t.get("reason", "")))
    return _summarize(tg, "decapsulation", results)


def run_encapsulation_key_check_group(tg: dict) -> dict:
    results = []
    for t in tg["tests"]:
        ek = bytes.fromhex(t["ek"])
        our = check_encapsulation_key(ek)
        ok = our == t["testPassed"]
        results.append((t["tcId"], ok, t.get("reason", "")))
    return _summarize(tg, "encapsulationKeyCheck", results)


def run_decapsulation_key_check_group(tg: dict) -> dict:
    dummy_c = bytes(CT_BYTES)  # only its length (CT_BYTES) is checked
    results = []
    for t in tg["tests"]:
        dk = bytes.fromhex(t["dk"])
        our = check_decapsulation_input(dk, dummy_c)
        ok = our == t["testPassed"]
        results.append((t["tcId"], ok, t.get("reason", "")))
    return _summarize(tg, "decapsulationKeyCheck", results)


def _summarize(tg: dict, function: str, results: list[tuple]) -> dict:
    total = len(results)
    failed = [r for r in results if not r[1]]
    return {
        "tgId": tg["tgId"],
        "function": function,
        "testType": tg["testType"],
        "total": total,
        "passed": total - len(failed),
        "failed": len(failed),
        "failed_details": failed,  # list of (tcId, ok, [reason])
    }


def main() -> list[dict]:
    keygen_doc = _load("ML-KEM-keyGen-FIPS203")
    encapdecap_doc = _load("ML-KEM-encapDecap-FIPS203")

    all_results = []
    for tg in _groups_for(keygen_doc):
        all_results.append(run_keygen_group(tg))

    for tg in _groups_for(encapdecap_doc):
        func = tg["function"]
        if func == "encapsulation":
            all_results.append(run_encapsulation_group(tg))
        elif func == "decapsulation":
            all_results.append(run_decapsulation_group(tg))
        elif func == "encapsulationKeyCheck":
            all_results.append(run_encapsulation_key_check_group(tg))
        elif func == "decapsulationKeyCheck":
            all_results.append(run_decapsulation_key_check_group(tg))
        else:
            raise SystemExit(f"unrecognized function {func!r} in tgId {tg['tgId']}")

    for r in all_results:
        print(
            f"tgId={r['tgId']:<3} {r['function']:<24} {r['testType']:<4} "
            f"total={r['total']:<3} passed={r['passed']:<3} failed={r['failed']}"
        )
        if r["failed"]:
            for detail in r["failed_details"]:
                print(f"    FAILED tcId={detail[0]} {detail[2:] if len(detail) > 2 else ''}")

    return all_results, keygen_doc.get("isSample"), encapdecap_doc.get("isSample")


if __name__ == "__main__":
    main()
