module clemensnasenberg_top  #(
    parameter MSB=8
) (  
    input [7:0] io_in,
    output [7:0] io_out
);
    wire clk = io_in[0];
    wire reset = io_in[1];
    wire data_in = io_in[2];
    wire [31:0] data_out;
    assign io_out[7:0] = data_out[7:0];

    shift_reg #(
        .MSB( 32 )
    )
    shift_reg_inst
    (
        .d ( data_in ),
        .clk ( clk ),
        .dir ( 1'b0 ),
        .en ( 1'b1 ),
        .rstn ( !reset ),
        .out ( data_out )
    );

endmodule
