#!/usr/bin/env python3
"""Guard: ML-KEM-768 parameters in the golden model must equal the locked FIPS 203 values.

  check_params.py [--file tb/golden/params.py]
  check_params.py --selftest

Reads top-level NAME = <int> assignments with ast (never imports/executes the file).
Any mismatch is an ERROR (exit 1): changing q, n, k, eta, du, dv or the sizes creates a
different, unproven scheme (ADR 0002: the mathematics is locked).
If the file does not exist yet, it says so and exits 0.
"""
import argparse, ast, os, sys, tempfile

LOCKED = {          # name: (value, source status)
    "Q": (3329, "verified: IETF draft-cfrg-schwabe-kyber-03; FIPS 203"),
    "N": (256, "verified: same"),
    "ZETA": (17, "verified: primitive 256th root of unity mod q (tcgcrest notes)"),
    "K": (3, "FIPS 203 Table 2 (ML-KEM-768); confirm at Phase 0"),
    "ETA1": (2, "FIPS 203 Table 2; confirm at Phase 0"),
    "ETA2": (2, "FIPS 203 Table 2; confirm at Phase 0"),
    "DU": (10, "FIPS 203 Table 2; confirm at Phase 0"),
    "DV": (4, "FIPS 203 Table 2; confirm at Phase 0"),
    "EK_BYTES": (1184, "verified: IETF draft-sfluhrer ... Table 1"),
    "DK_BYTES": (2400, "verified: same"),
    "CT_BYTES": (1088, "verified: same"),
    "SS_BYTES": (32, "verified: same"),
}


def derived_ok():
    """Sizes follow from k, du, dv: ek=384k+32, dk=768k+96, ct=32(du*k+dv)."""
    k, du, dv = LOCKED["K"][0], LOCKED["DU"][0], LOCKED["DV"][0]
    return {"EK_BYTES": 384 * k + 32, "DK_BYTES": 768 * k + 96, "CT_BYTES": 32 * (du * k + dv)}


def read_constants(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                v = ast.literal_eval(node.value)
            except Exception:
                continue
            if isinstance(v, int) and not isinstance(v, bool):
                found[node.targets[0].id] = v
    return found


def check(path):
    problems = []
    for name, want in derived_ok().items():          # internal consistency of the lock itself
        assert LOCKED[name][0] == want, f"internal: {name} lock inconsistent with formula"
    found = read_constants(path)
    for name, (want, _) in LOCKED.items():
        if name not in found:
            problems.append(f"missing constant {name} (expected {want})")
        elif found[name] != want:
            problems.append(f"{name} = {found[name]} but FIPS 203 ML-KEM-768 requires {want}")
    return problems, found


def selftest():
    good = "\n".join(f"{n} = {v}" for n, (v, _) in LOCKED.items()) + "\n"
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "params.py")
        open(p, "w").write(good)
        probs, _ = check(p)
        assert probs == [], probs
        open(p, "w").write(good.replace("Q = 3329", "Q = 7681"))          # old Kyber q
        probs, _ = check(p)
        assert any(s.startswith("Q = 7681") for s in probs), probs
        open(p, "w").write("\n".join(l for l in good.splitlines() if not l.startswith("ETA1")) + "\n")
        probs, _ = check(p)
        assert any("missing constant ETA1" in s for s in probs), probs
    print("selftest OK (check_params.py)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="tb/golden/params.py")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not os.path.exists(a.file):
        print(f"check_params: {a.file} does not exist yet (golden model not created). Nothing to check.")
        return 0
    problems, found = check(a.file)
    for name, (want, src) in LOCKED.items():
        state = "ok" if found.get(name) == want else "MISMATCH"
        print(f"{state:9} {name:9} = {found.get(name, '-')}  (locked {want}; {src})")
    if problems:
        print("\nERROR: parameters differ from the locked ML-KEM-768 set:")
        for p in problems:
            print("  -", p)
        return 1
    print("\ncheck_params: all locked parameters match.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
