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
    input sd_ch1,
    input sd_ch2,
    input ws,
    input [1:0] channel_sel,
    output sd_out,
    output wsd,
    output wsp
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    wire [7:0] inputs = {1'b0, channel_sel, sd_ch2, sd_ch1, ws, rst, sck};
    wire [7:0] outputs;
    assign sd_out = outputs[2];
    assign wsd = outputs[1];
    assign wsp = outputs[0];

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
