# quartus/phase04_pipeline_c3/C3.sdc -- one constraint file for all four Phase 4 revisions
# (C3-P0, C3-P2, C3-P4, C3-P6). ADR 0006: Phase 4 milestone constraint 40.000 ns (25 MHz), an
# experimental target, not a hardware or system requirement. This is the Phase 3 SDC with only the
# period changed. rst_ni is an asynchronous reset input of a kernel-only compile (virtual pin).
create_clock -name clk_i -period 40.000 [get_ports {clk_i}]
derive_clock_uncertainty

set_false_path -from [get_ports {rst_ni}]
