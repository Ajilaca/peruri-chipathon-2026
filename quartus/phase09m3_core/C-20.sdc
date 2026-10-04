# quartus/phase09m3_core/C-20.sdc -- Phase 9M item 3: information compile at 20.000 ns (MK-20), identical to C.sdc except the clock period 20.000 ns; not a gate (ADR 0010).
# Not a gate (ADR 0010); information only.
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
