# tb/golden/

Model acuan Python untuk ML-KEM-768 (FIPS 203), mandiri dari RTL.
`params.py` harus mendefinisikan persis: `Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES`
(diperiksa oleh `python3 .claude/skills/mlkem-guard/scripts/check_params.py`). Hanya vektor KAT resmi; jangan mengarang vektor.
