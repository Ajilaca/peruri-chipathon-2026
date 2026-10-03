# quartus/phase08_keccak/C-20.sdc -- information compile at 20.000 ns (C5-20, 8a test plan V10): identical to C.sdc except the clock period 20.000 ns (50 MHz).
# Not a gate (ADR 0010); information only.
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
