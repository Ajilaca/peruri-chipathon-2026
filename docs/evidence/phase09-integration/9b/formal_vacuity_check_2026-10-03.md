# Check of the free signals (`(* anyseq *)`) of the formal stubs, 2026-10-03

Why: while proving `mlkem_hash` (Phase 9b) a proof returned PASS although the sponge stub never reached its squeeze state (test plan 9b, Amendment A1, item 2). The other formal stubs in the repository that use `(* anyseq *)` were checked with cover statements (scratch copies, repository files unchanged). All results below are MEASURED with SymbiYosys (cover mode, boolector).

| Stub / proof | What was covered | Result |
|---|---|---|
| `formal/phase09-integration/9b/keccak_sponge_r2_stub.sv`, signals declared `logic` (first version) | squeeze state, a digest word after 3 words, `done_o` | **not reached** (the free `f_go` was a constant): that proof was vacuous and was discarded |
| the same with the signals declared `wire` (the repository version) | the same | all reached (steps 3-9); the proof and its controls were rerun |
| `formal/phase08-keccak-stream/8c/keccak_sampler_stub.sv` (signals declared `logic`, read in continuous assignments), top of `kpke_sched_smp_formal_top.sv`, depth 20 and 140 | sampler busy, a beat offered (`smp_cvalid`), a beat written into the store (`smp_wr`), the sampling state, `smp_in_ready`, `smp_clast`, `smp_bytes != 0` | all reached by step 5, so the stub's free signals are free in 8c; the PWMS state (`st == SPwms`) was **not reached within depth 140**: that is a depth effect (the first PWMS comes after six sampled polynomials of at least 128 beats each), not evidence of vacuity; the PWMS properties of 8c are inductive and are not shown by a base-case trace |
| `formal/phase03-multilane/modmul_reduce_uf.sv` (`uf_p`, `logic`) | not covered separately: its control `k1_negctl_noack.sby` (the proof without the consistency constraint must FAIL) fails as required in the Phase 3 evidence, which can only happen if `uf_p` is free | consistent with free |
