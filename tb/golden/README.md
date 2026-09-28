# tb/golden/
Python golden model of ML-KEM-768 (FIPS 203), independent of the RTL.
`params.py` must define exactly: `Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES`
(checked by `python3 .claude/skills/mlkem-guard/scripts/check_params.py`). Official KAT vectors only;
never invent vectors.
