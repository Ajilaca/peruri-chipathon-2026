# quartus/phase01_ntt_c0/report_critical_paths.tcl
# Read-only timing drill-down on the EXISTING post-fit netlist of revision C0.
# Does not recompile, does not change the RTL, the .qsf or C0.sdc.
#
# Run from quartus/phase01_ntt_c0/:
#   quartus_sta -t report_critical_paths.tcl
# Outputs go to output_files/C0_*.rpt (not committed; extracts go to evidence/).

project_open phase01_ntt_c0 -revision C0

create_timing_netlist
foreach oc [get_available_operating_conditions] {
    puts "OPERATING_CONDITION_AVAILABLE: $oc"
}

# Worst corner reported in C0.sta.summary: Slow 1100mV 100C.
set_operating_conditions 7_slow_1100mv_100c
read_sdc
update_timing_netlist

report_clocks -file output_files/C0_clocks.rpt
report_sdc    -file output_files/C0_sdc.rpt

# Worst setup paths with full data-path and clock-path breakdown.
report_timing -setup -npaths 10 -detail full_path -show_routing \
    -file output_files/C0_worst_setup_paths_full.rpt

# Many paths, summary only: used to see which modules the failing endpoints belong to.
report_timing -setup -npaths 5000 -nworst 1 -detail summary \
    -file output_files/C0_setup_top5000_summary.rpt

# Worst hold paths (for completeness; hold is met).
report_timing -hold -npaths 10 -detail full_path \
    -file output_files/C0_worst_hold_paths_full.rpt

# Clock network of the launch/latch registers (checks the ripple-clock warning 15725).
report_timing -setup -npaths 1 -detail full_path -show_routing \
    -file output_files/C0_worst_setup_path_1_routing.rpt

report_clock_fmax_summary -file output_files/C0_fmax_summary.rpt

delete_timing_netlist
project_close

# ---- Second pass: per-structure drill-down (same netlist, same corner, read-only) ----
project_open phase01_ntt_c0 -revision C0
create_timing_netlist
set_operating_conditions 7_slow_1100mv_100c
read_sdc
update_timing_netlist

# Worst path through each modular multiplier instance (NTT/CT, INTT/GS, INTT scaling).
report_timing -setup -npaths 1 -detail full_path \
    -through [get_cells -compatibility_mode {*u_fwd_mul*}] -file output_files/C0_path_through_u_fwd_mul.rpt
report_timing -setup -npaths 1 -detail full_path \
    -through [get_cells -compatibility_mode {*u_inv_mul*}] -file output_files/C0_path_through_u_inv_mul.rpt
report_timing -setup -npaths 1 -detail full_path \
    -through [get_cells -compatibility_mode {*u_scale_mul*}] -file output_files/C0_path_through_u_scale_mul.rpt

# Control-only endpoints (the FSM/counter registers).
report_timing -setup -npaths 3 -detail full_path \
    -to [get_registers {layer_q[*]}] -file output_files/C0_path_to_layer_q.rpt
report_timing -setup -npaths 1 -detail full_path \
    -to [get_registers {zeta_idx_q[*]}] -file output_files/C0_path_to_zeta_idx_q.rpt

delete_timing_netlist
project_close
