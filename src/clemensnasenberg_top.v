module clemensnasenberg_top  #(
    parameter MSB=8
) (  
    input [7:0] io_in,
    output [7:0] io_out
);
    wire clk = io_in[0];
    wire reset = io_in[1];
    wire [31:0] out;
    assign io_out[7:0] = out[7:0];

    shift_reg #(
        .MSB( 32 )
    )
    shift_reg_inst
    (
        .d ( 1'b1 ),
        .clk ( clk ),
        .en ( 1'b1 ),
        .rstn ( !reset ),
        .out ( out )
    );

endmodule
