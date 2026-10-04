# quartus/phase09f0_core/C-11.sdc -- Phase 9F step S0: 11.000 ns, information only (ADR 0010, ADR 0036), same form as the other S0 files (no reset false path: see result_9f0.md finding 4).
create_clock -name clk_i -period 11.000 [get_ports {clk_i}]
derive_clock_uncertainty
