# quartus/phase07_keccak/K-20.sdc -- information compile at 20.000 ns (K0-20, test plan V10): identical to K.sdc except the clock period 20.000 ns (50 MHz).
# Not a gate (ADR 0010); information only.
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
