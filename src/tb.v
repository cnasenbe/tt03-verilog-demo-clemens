`default_nettype none
`timescale 1ns/1ps

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb (
    // testbench is controlled by test.py
    input sck,
    input rst,
    input sd_c1,
    input sd_c2,
    input ws,
    input [1:0] channel_sel,
    output sd_out,
    output wsd,
    output wsp,
    output xor_data_left,
    output xor_data_right
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    wire [7:0] inputs = {1'b0, channel_sel, sd_c2, sd_c1, ws, rst, sck};
    wire [7:0] outputs;
    assign sd_out = outputs[4];
    assign wsd = outputs[3];
    assign wsp = outputs[2];
    assign xor_data_left = outputs[1];
    assign xor_data_right = outputs[0];

    // instantiate the DUT
    clemensnasenberg_top clemensnasenberg_top_inst(
        `ifdef GL_TEST
            .vccd1( 1'b1),
            .vssd1( 1'b0),
        `endif
        .io_in  (inputs),
        .io_out (outputs)
        );

endmodule
