// Formal harness for the toolchain smoke test only.
module smoke_counter_props (input logic clk, input logic rst_n, input logic en);
    logic [7:0] count;
    smoke_counter #(.WIDTH(8)) dut (.clk, .rst_n, .en, .count);
    logic past_valid = 1'b0;
    always_ff @(posedge clk) past_valid <= 1'b1;
    always_ff @(posedge clk) if (past_valid) begin
        if (!$past(rst_n))                 assert (count == 8'd0);
        else if (!$past(en))               assert (count == $past(count));
        else                               assert (count == $past(count) + 8'd1);
    end
endmodule
