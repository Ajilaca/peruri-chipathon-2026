"""tb/golden/crosscheck_kyberpy.py

Cross-checks tb/golden/mlkem.py's deterministic internal algorithms against
the independent implementation kyber-py
(https://github.com/GiacomoPope/kyber-py, license MIT OR Apache-2.0,
Copyright Giacomo Pope) on N pseudorandom inputs generated from a fixed
seed (reproducible).

kyber-py is used ONLY as a test-time oracle, installed in a throwaway
virtualenv OUTSIDE this repository (see
.claude/skills/mlkem-guard/reference/kat_sources.md, e.g.
~/.cache/chip2026-oracle). Its code is not copied into this repository and
it is not added to scripts/requirements-dev.txt.

Run with THAT venv's interpreter, e.g.:
    ~/.cache/chip2026-oracle/venv/bin/python3 tb/golden/crosscheck_kyberpy.py

If kyber_py is not importable in the interpreter running this script, it
stops immediately with SystemExit and a clear message -- it never reports
success without having actually run the comparison.

If a mismatch is found, this script does NOT decide which implementation
is right. It records both values and stops; resolving a mismatch is a
job for re-reading the FIPS 203 text and the official ACVP vectors
(tb/golden/run_kat.py), not for guessing.
"""

from __future__ import annotations

import datetime
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

try:
    from kyber_py.ml_kem import ML_KEM_768 as ORACLE
except ImportError as exc:
    raise SystemExit(
        "kyber_py is not importable in this Python interpreter.\n"
        "This script must be run with the throwaway oracle venv's python, e.g.:\n"
        "  ~/.cache/chip2026-oracle/venv/bin/python3 tb/golden/crosscheck_kyberpy.py\n"
        f"(import error: {exc})"
    )

from mlkem import (  # noqa: E402
    ml_kem_decaps_internal,
    ml_kem_encaps_internal,
    ml_kem_keygen_internal,
)
from params import CT_BYTES, DK_BYTES, EK_BYTES, SS_BYTES  # noqa: E402

N = 2000
SEED = 20260928  # fixed: this script is reproducible, not re-randomized per run

EVIDENCE_DIR = pathlib.Path(__file__).resolve().parents[2] / "evidence" / "phase00"


def _kyberpy_version() -> str:
    try:
        from importlib.metadata import version

        return version("kyber-py")
    except Exception as exc:  # pragma: no cover - diagnostic path only
        return f"unknown ({exc})"


def _random_bytes(rng: random.Random, n: int) -> bytes:
    return bytes(rng.getrandbits(8) for _ in range(n))


def run(n: int = N, seed: int = SEED) -> tuple[int, list[dict]]:
    rng = random.Random(seed)
    mismatches: list[dict] = []

    for i in range(n):
        d = _random_bytes(rng, 32)
        z = _random_bytes(rng, 32)
        m = _random_bytes(rng, 32)

        ek_ours, dk_ours = ml_kem_keygen_internal(d, z)
        ek_oracle, dk_oracle = ORACLE._keygen_internal(d, z)
        if ek_ours != ek_oracle or dk_ours != dk_oracle:
            mismatches.append(
                {
                    "trial": i,
                    "stage": "keygen_internal",
                    "ours": {"ek": ek_ours.hex(), "dk": dk_ours.hex()},
                    "oracle": {"ek": ek_oracle.hex(), "dk": dk_oracle.hex()},
                }
            )
            continue

        K_ours, c_ours = ml_kem_encaps_internal(ek_ours, m)
        K_oracle, c_oracle = ORACLE._encaps_internal(ek_oracle, m)
        if K_ours != K_oracle or c_ours != c_oracle:
            mismatches.append(
                {
                    "trial": i,
                    "stage": "encaps_internal",
                    "ours": {"K": K_ours.hex(), "c": c_ours.hex()},
                    "oracle": {"K": K_oracle.hex(), "c": c_oracle.hex()},
                }
            )
            continue

        Kp_ours = ml_kem_decaps_internal(dk_ours, c_ours)
        Kp_oracle = ORACLE._decaps_internal(dk_oracle, c_oracle)
        if Kp_ours != Kp_oracle:
            mismatches.append(
                {
                    "trial": i,
                    "stage": "decaps_internal (valid ciphertext)",
                    "ours": {"K": Kp_ours.hex()},
                    "oracle": {"K": Kp_oracle.hex()},
                }
            )
            continue

        byte_idx = rng.randrange(CT_BYTES)
        bit_idx = rng.randrange(8)
        c_bad = bytearray(c_ours)
        c_bad[byte_idx] ^= 1 << bit_idx
        c_bad = bytes(c_bad)

        Kb_ours = ml_kem_decaps_internal(dk_ours, c_bad)
        Kb_oracle = ORACLE._decaps_internal(dk_oracle, c_bad)
        if Kb_ours != Kb_oracle:
            mismatches.append(
                {
                    "trial": i,
                    "stage": "decaps_internal (modified ciphertext)",
                    "ours": {"K": Kb_ours.hex()},
                    "oracle": {"K": Kb_oracle.hex()},
                    "flip": {"byte_idx": byte_idx, "bit_idx": bit_idx},
                }
            )

    return n, mismatches


def main() -> None:
    n, mismatches = run()
    passed = n - len(mismatches)
    date_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    kyberpy_version = _kyberpy_version()

    lines = []
    lines.append("ML-KEM-768 golden model cross-check against kyber-py (MEASURED)")
    lines.append(f"Generated: {date_utc} UTC")
    lines.append("Oracle: kyber-py (https://github.com/GiacomoPope/kyber-py), "
                  "license MIT OR Apache-2.0, Copyright Giacomo Pope")
    lines.append(f"kyber-py version: {kyberpy_version}")
    lines.append("Installed in a throwaway virtualenv outside this repository "
                  "(not in scripts/requirements-dev.txt, not copied into the repo)")
    lines.append(f"N = {n} trials, fixed RNG seed = {SEED} (random.Random(seed), reproducible)")
    lines.append(
        "Per trial: fresh (d, z, m) from the seeded RNG -> compare keygen_internal, "
        "encaps_internal, decaps_internal (valid ciphertext), and decaps_internal on a "
        "randomly 1-bit-flipped ciphertext (implicit rejection path)."
    )
    lines.append("")
    lines.append(f"RESULT: {passed}/{n} trials fully matched kyber-py at every stage; "
                  f"{len(mismatches)} mismatch(es).")
    lines.append("")

    if mismatches:
        lines.append("MISMATCHES (both values reported; not adjudicated by this script):")
        for m in mismatches:
            lines.append(f"  trial {m['trial']}, stage: {m['stage']}")
            lines.append(f"    ours:   {m['ours']}")
            lines.append(f"    oracle: {m['oracle']}")
            if "flip" in m:
                lines.append(f"    bit flipped: {m['flip']}")
    else:
        lines.append("No mismatches. This is not exhaustive coverage: it is N "
                      "pseudorandom trials from one fixed seed, not a proof.")

    text = "\n".join(lines) + "\n"
    print(text)

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = EVIDENCE_DIR / f"crosscheck_kyberpy_{date_utc}.txt"
    out_path.write_text(text)
    print(f"Log saved to {out_path}")

    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
