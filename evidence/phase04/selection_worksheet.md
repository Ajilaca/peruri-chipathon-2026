| P | bit-exact | siklus konstan | ALM | ≤ 10.478? | slack setup / hold terburuk @ 40,000 ns | timing terpenuhi? | siklus_NTT | siklus_INTT | Fmax per slow corner (MHz) | Fmax(P) = terendah | t_NTT (µs) | t_INTT (µs) | kandidat? | d(P) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | PASS | PASS | 9,723 / 41,910 | ya | -90.653 / 0.207 | tidak | 113 | 369 | Slow 1100mV 100C: 7.65; Slow 1100mV -40C: 7.68 | 7.65 | 14.771 | 48.235 | tidak | - |
| 2 | PASS | PASS | 9,696 / 41,910 | ya | -0.368 / 0.174 | tidak | 115 | 371 | Slow 1100mV 100C: 25.04; Slow 1100mV -40C: 24.77 | 24.77 | 4.643 | 14.978 | tidak | - |
| 4 | PASS | PASS | 10,439 / 41,910 | ya | 8.734 / 0.157 | ya | 117 | 373 | Slow 1100mV 100C: 32.60; Slow 1100mV -40C: 31.98 | 31.98 | 3.659 | 11.664 | ya | 0.0000 |
| 6 | PASS | PASS | 10,505 / 41,910 | tidak | 10.753 / 0.140 | ya | 119 | 375 | Slow 1100mV 100C: 34.19; Slow 1100mV -40C: 34.50 | 34.19 | 3.481 | 10.968 | tidak | - |

Sumber daya lain (MEASURED): P=0: register 3097, DSP 9 / 112, blok RAM 0 / 553; P=2: register 3817, DSP 9 / 112, blok RAM 16 / 553; P=4: register 4145, DSP 9 / 112, blok RAM 26 / 553; P=6: register 4168, DSP 9 / 112, blok RAM 29 / 553
File evidence: quartus_C3-P0.md, quartus_C3-P2.md, quartus_C3-P4.md, quartus_C3-P6.md, verification_status.json

Himpunan kandidat C = {4}
t_min = 3.658537 us; dalam 5 % dari t_min: {4}
HASIL: P_terpilih = 4 (kandidat terkecil dengan d(P) <= 0.05). Dicatat di ADR baru oleh tim.
