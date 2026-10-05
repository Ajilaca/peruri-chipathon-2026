# Read-only top-path report (Phase 5). Run on a COPY of a project (never on the repo .qpf: project_open rewrites it):
#   quartus_sta -t phase5_top_paths.tcl <project> <revision>      (default: C3-P6 C3-P6)
# Output: paths_slow100_{summary,full}.rpt in the current directory.
set prj [expr {[llength $quartus(args)] > 0 ? [lindex $quartus(args) 0] : "C3-P6"}]
set rev [expr {[llength $quartus(args)] > 1 ? [lindex $quartus(args) 1] : "C3-P6"}]
project_open $prj -revision $rev
create_timing_netlist -model slow -temperature 100 -voltage 1100
read_sdc
update_timing_netlist
report_timing -setup -npaths 300 -nworst 1 -pairs_only -detail summary -file paths_slow100_summary.rpt
report_timing -setup -npaths 3 -detail full_path -file paths_slow100_full.rpt
delete_timing_netlist
project_close
