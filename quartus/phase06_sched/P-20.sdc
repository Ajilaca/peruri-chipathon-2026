# quartus/phase06_sched/P-20.sdc -- information compiles at 20.000 ns (S10-20, test plan_s10.md V7): identical to P.sdc except the clock period 20.000 ns (50 MHz).
# Not a gate (ADR 0010); information only.
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
