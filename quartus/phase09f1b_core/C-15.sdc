# quartus/phase09f1b_core/C-15.sdc -- Phase 9F step S1b: 15.000 ns, information only (ADR 0010, ADR 0036), same form as quartus/phase09c_core/C-20.sdc.
create_clock -name clk_i -period 15.000 [get_ports {clk_i}]
derive_clock_uncertainty
