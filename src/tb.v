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
    input sd1,
    input sd2,
    input ws,
    output [6:0] data_out,
    output sd_out
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    wire [7:0] inputs = {3'b0, sd2, sd1, ws, rst, sck};
    wire [7:0] outputs;
    assign data_out = outputs[6:0];
    assign sd_out = outputs[7];

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
