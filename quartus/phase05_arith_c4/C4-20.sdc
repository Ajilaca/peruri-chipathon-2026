# quartus/phase05_arith_c4/C4-20.sdc -- information compiles only (ADR 0011 D1): final C4 (C4b-B) and C3-P6 at 20.000 ns
# (50 MHz). Identical to C4.sdc except the clock period; not a Phase 5 gate (ADR 0010).
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
