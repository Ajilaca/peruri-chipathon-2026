# 50 MHz reference, matching the DE10-Nano's 50 MHz FPGA clock inputs.
create_clock -name clk -period 20.000 [get_ports {clk}]
derive_clock_uncertainty
set_false_path -from [get_ports {rst_n en}]
set_false_path -to   [get_ports {msb}]
