# quartus/phase09f1_core/C.sdc -- Phase 9F step S1 constraint, identical to quartus/phase09c_core/C.sdc (40.000 ns); only this comment differs.
# rst_ni is an asynchronous reset input of a kernel-only compile (virtual pin).
create_clock -name clk_i -period 40.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
