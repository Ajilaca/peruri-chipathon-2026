# quartus/phase05m_memsched/M-20.sdc -- information compile only (test plan_s8.md V10): identical to M.sdc except the clock period 20.000 ns (50 MHz).
# Not a gate of Phase 5M (ADR 0010, ADR 0011 D1).
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
