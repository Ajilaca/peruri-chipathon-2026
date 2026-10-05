# tb/golden/

Model acuan Python untuk ML-KEM-768 (FIPS 203), mandiri dari RTL.
`params.py` harus mendefinisikan persis: `Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES`
(konstanta dikunci, lihat ADR 0002). Hanya vektor KAT resmi; jangan mengarang vektor.
