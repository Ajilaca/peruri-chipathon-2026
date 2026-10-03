# quartus/phase08b_sampler/C.sdc -- Phase 8b constraint, identical to quartus/phase08_keccak/C.sdc (40.000 ns, ADR 0011 D1; ADR 0017 keeps it); only these comment lines differ.
# rst_ni is an asynchronous reset input of a kernel-only compile (virtual pin).
create_clock -name clk_i -period 40.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
