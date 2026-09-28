// Quartus toolchain smoke test only (verifies Quartus + Cyclone V device support).
// NOT project RTL. No board pin assignments are made on purpose: the fitter
// auto-places the 4 I/Os, which is fine for a toolchain check but must never
// be programmed onto the DE10-Nano.
`default_nettype none
module smoke_top (
    input  wire logic clk,
    input  wire logic rst_n,
    input  wire logic en,
    output logic      msb
);
    logic [31:0] count;
    always_ff @(posedge clk) begin
        if (!rst_n)  count <= '0;
        else if (en) count <= count + 1'b1;
    end
    assign msb = count[31];
endmodule
`default_nettype wire
