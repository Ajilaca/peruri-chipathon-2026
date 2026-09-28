"""tb/golden/fetch_acvp_vectors.py

Downloads the two ML-KEM ACVP "internalProjection.json" vector files
(NIST's official Cryptographic Algorithm Validation Program test vectors,
which include ML-KEM-768 groups among other parameter sets) from a pinned
commit of the NIST ACVP-Server repository, and verifies each downloaded
file's sha256 against the value recorded in
`.claude/skills/mlkem-guard/reference/kat_sources.md` before saving it.

If a hash does not match, this script stops (raises SystemExit) without
saving the file and without using it as a test vector -- per project rule,
we never invent or silently accept an unverified vector.

The saved JSON files go to tb/vectors/acvp/ and are NOT committed to git
(tb/vectors/acvp/*.json is in .gitignore).
"""

from __future__ import annotations

import hashlib
import pathlib
import urllib.request

PINNED_COMMIT = "975de31eb83d87039ec88934fdc47d8c312b892d"
BASE_URL = (
    f"https://raw.githubusercontent.com/usnistgov/ACVP-Server/{PINNED_COMMIT}"
    "/gen-val/json-files"
)

# (directory under gen-val/json-files, expected sha256), both from
# .claude/skills/mlkem-guard/reference/kat_sources.md
FILES = [
    (
        "ML-KEM-keyGen-FIPS203",
        "d7a62a2c3476957f56dd8d24f9004ea6776ccfe995ffe71a65bb9506dc9c7b1b",
    ),
    (
        "ML-KEM-encapDecap-FIPS203",
        "a556952ce869bb89c3a3196a701dad89647c193a34c86eafb61a9d710d5b810f",
    ),
]

DEST_DIR = pathlib.Path(__file__).resolve().parents[1] / "vectors" / "acvp"


def dest_path(subdir: str) -> pathlib.Path:
    return DEST_DIR / f"{subdir}.internalProjection.json"


def fetch_and_verify() -> list[pathlib.Path]:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    saved = []
    for subdir, expected_sha256 in FILES:
        url = f"{BASE_URL}/{subdir}/internalProjection.json"
        print(f"fetching {url}")
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
        actual_sha256 = hashlib.sha256(data).hexdigest()
        if actual_sha256 != expected_sha256:
            raise SystemExit(
                f"sha256 mismatch for {url}\n"
                f"  expected (kat_sources.md): {expected_sha256}\n"
                f"  actual (downloaded):       {actual_sha256}\n"
                "Stopping: NOT saving an unverified vector file. Do not lower "
                "this check; if the pinned commit's content genuinely changed, "
                "that is a decision for the team, not this script."
            )
        dest = dest_path(subdir)
        dest.write_bytes(data)
        print(f"  sha256 OK ({actual_sha256}), saved to {dest} ({len(data)} bytes)")
        saved.append(dest)
    return saved


if __name__ == "__main__":
    fetch_and_verify()
