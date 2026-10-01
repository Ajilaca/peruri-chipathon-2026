# quartus/phase05_arith_c4/C4.sdc -- one constraint file for every Phase 5 revision (C4a .. C4d) compiled at the
# Phase 4 constraint (ADR 0011 D1: 40.000 ns, as C3-P6). Content identical to quartus/phase04_pipeline_c3/C3.sdc;
# only these comment lines differ. rst_ni is an asynchronous reset input of a kernel-only compile (virtual pin).
create_clock -name clk_i -period 40.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
