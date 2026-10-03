# quartus/phase08c_smp/P.sdc -- Phases 8c / 8d constraint, identical to quartus/phase06_sched/P.sdc (40.000 ns; ADR 0011 D1, kept by ADR 0017); only this comment line differs.
# rst_ni is an asynchronous reset input of a kernel-only compile (virtual pin).
create_clock -name clk_i -period 40.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
