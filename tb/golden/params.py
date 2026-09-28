# tb/golden/params.py
# Locked ML-KEM-768 parameters (FIPS 203, Section 8, Table 2 and Table 3).
# Source and cross-check: docs/evidence/golden/fips203_errata_2026-09-28.md,
# docs/decisions/0003-fips-203-errata-findings-and-golden-model-handling.md.
# This file defines ML-KEM-768 ONLY (see mlkem-guard SKILL.md); do not add 512/1024.
# Names are exactly the ones checked by
# .claude/skills/mlkem-guard/scripts/check_params.py.

# Section 2.3: constants, fixed for all ML-KEM parameter sets.
Q = 3329        # q = 2^8 * 13 + 1
N = 256

# Section 4.3: zeta is a primitive n-th (256-th) root of unity modulo q.
ZETA = 17

# Section 8, Table 2 (ML-KEM-768 row): k, eta1, eta2, du, dv.
K = 3
ETA1 = 2
ETA2 = 2
DU = 10
DV = 4

# Section 8, Table 3 (ML-KEM-768 row): sizes in bytes.
EK_BYTES = 1184
DK_BYTES = 2400
CT_BYTES = 1088
SS_BYTES = 32
