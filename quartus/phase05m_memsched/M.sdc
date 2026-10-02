# quartus/phase05m_memsched/M.sdc -- one constraint file for every Phase 5M revision, compiled at the Phase 4 / 5 constraint
# (40.000 ns, ADR 0011 D1; ADR 0017 keeps it). Content identical to quartus/phase05_arith_c4/C4.sdc; only these comment lines differ.
# rst_ni is an asynchronous reset input of a kernel-only compile (virtual pin).
create_clock -name clk_i -period 40.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
