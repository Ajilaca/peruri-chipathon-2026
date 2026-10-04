# quartus/phase09m2_core/C-20.sdc -- Phase 9M item 2: 20.000 ns (50 MHz), information only (ADR 0010), identical to quartus/phase09c_core/C-20.sdc except this comment.
# Not a gate (ADR 0010); information only.
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
