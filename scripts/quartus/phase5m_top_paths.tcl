# Read-only top-path report (Phase 5M, option 1 of the 50 MHz question). Run on a COPY of a project (never on the repo .qpf: project_open rewrites it):
#   quartus_sta -t phase5m_top_paths.tcl <project> <revision> <temperature: 100 or -40>
# Output: <revision>_paths_slow<temperature>_{summary,full}.rpt in the current directory (300 worst setup paths, 3 in full detail).
set prj  [lindex $quartus(args) 0]
set rev  [lindex $quartus(args) 1]
set temp [lindex $quartus(args) 2]
project_open $prj -revision $rev
create_timing_netlist -model slow -temperature $temp -voltage 1100
read_sdc
update_timing_netlist
report_timing -setup -npaths 300 -nworst 1 -pairs_only -detail summary -file ${rev}_paths_slow${temp}_summary.rpt
report_timing -setup -npaths 3 -detail full_path -file ${rev}_paths_slow${temp}_full.rpt
delete_timing_netlist
project_close
