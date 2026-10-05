// Toolchain smoke-test DUT only. NOT project RTL.
`timescale 1ns / 1ps
`default_nettype none
module smoke_counter #(
    parameter int WIDTH = 8
) (
    input  wire logic             clk,
    input  wire logic             rst_n,   // active-low, synchronous
    input  wire logic             en,
    output logic      [WIDTH-1:0] count
);
    always_ff @(posedge clk) begin
        if (!rst_n)  count <= '0;
        else if (en) count <= count + 1'b1;
    end
endmodule
`default_nettype wire
