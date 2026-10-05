# Read-only worst setup path per multiplier-path register segment (Phase 5). Run on a COPY of a project:
#   quartus_sta -t phase5_segments.tcl <project> <revision> <cutA> <cutB> <cutC>
# where cutA < cutB < cutC are the reducer REG_AFTER positions (e.g. 0 5 11 for C3-P6, 0 3 5 for C4a).
# Prints one "SEG <name> slack=..." line per segment (lanes and scaling multiplier), Slow 1100mV 100C.
set prj [lindex $quartus(args) 0]
set rev [lindex $quartus(args) 1]
set c0  [lindex $quartus(args) 2]
set c1  [lindex $quartus(args) 3]
set c2  [lindex $quartus(args) 4]
project_open $prj -revision $rev
create_timing_netlist -model slow -temperature 100 -voltage 1100
read_sdc
update_timing_netlist
foreach {inst tag} {u_bfly|u_mul LANE u_scale_mul SCALE} {
  foreach {name from to} [list \
      "${tag}_cut${c0}_to_cut${c1}" "*${inst}|*g_cut\[${c0}\].g_reg.q\[*\]" "*${inst}|*g_cut\[${c1}\].g_reg.q\[*\]" \
      "${tag}_cut${c1}_to_cut${c2}" "*${inst}|*g_cut\[${c1}\].g_reg.q\[*\]" "*${inst}|*g_cut\[${c2}\].g_reg.q\[*\]" \
      "${tag}_cut${c2}_to_any"      "*${inst}|*g_cut\[${c2}\].g_reg.q\[*\]" "*"] {
    set p [get_timing_paths -setup -npaths 1 -from [get_registers $from] -to [get_keepers $to]]
    set n 0
    foreach_in_collection x $p {
      incr n
      puts "SEG $name slack=[get_path_info $x -slack] from=[get_node_info -name [get_path_info $x -from]] to=[get_node_info -name [get_path_info $x -to]]"
    }
    if {$n == 0} { puts "SEG $name NO_PATH_FOUND" }
  }
}
delete_timing_netlist
project_close
