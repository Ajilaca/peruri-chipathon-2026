# rtl/
Synthesizable SystemVerilog, one module per file. Every file starts with ```default_nettype none``` and ends by restoring ```default_nettype wire```. No block is written before its golden model exists (docs/ROADMAP.md). Numbers about a block come only from Quartus (`/quartus-report`).
