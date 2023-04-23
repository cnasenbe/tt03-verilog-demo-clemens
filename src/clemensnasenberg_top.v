module clemensnasenberg_top  #(
    parameter WIDTH=24,
    parameter CTRL_WIDTH=23
) (  
    input [7:0] io_in,
    output [7:0] io_out
);
    wire sck = io_in[0];
    wire reset = io_in[1];
    wire ws = io_in[2];
    wire sd_c1 = io_in[3];
    wire sd_c2 = io_in[4];
    wire [1:0] channel_sel = io_in[6:5];
    wire sd_out;
    assign io_out[7:0] = {3'b0, sd_out, wsd, wsp, xor_data_left, xor_data_right}; 

    wire xor_data_left;
    wire xor_data_right;

    reg wsd;
    reg wsd_reg;
    wire wsp;

    reg [WIDTH-1:0] data_left_c1;
    reg [WIDTH-1:0] data_right_c1;
    reg [WIDTH-1:0] data_c1;
    reg [WIDTH-1:0] data_left_c2;
    reg [WIDTH-1:0] data_right_c2;
    reg [WIDTH-1:0] data_c2;
    reg [CTRL_WIDTH-1:0] control_reg;
    integer i;

    assign wsp = wsd ^ wsd_reg;
    assign xor_data_left = ^data_left_c1;
    assign xor_data_right = ^data_right_c1;

    always @ (posedge sck) begin
        if (reset == 1'b1) begin
            wsd <= 1'b0;
            wsd <= 1'b0;
            data_left_c1 <= 'b0;
            data_right_c1 <= 'b0;
            data_c1 <= 'b0;
            data_left_c2 <= 'b0;
            data_right_c2 <= 'b0;
            data_c2 <= 'b0;
            control_reg <= 'b0;
        end else begin
            if (wsp == 1'b1) begin
                control_reg[CTRL_WIDTH-2:0] <= 'b0;
                control_reg[CTRL_WIDTH-1] <= 1'b1;
                data_c1[WIDTH-2:0] <= 'b0;
                data_c1[WIDTH-1] <= sd_c1;
                data_c2[WIDTH-2:0] <= 'b0;
                data_c2[WIDTH-1] <= sd_c2;
            end else begin
                control_reg[CTRL_WIDTH-1] <= 1'b0;
                for (i = 1; i < CTRL_WIDTH; i = i+1) begin
                    control_reg[CTRL_WIDTH-1-i] <= control_reg[CTRL_WIDTH-i];
                end
                for (i = 0; i <= CTRL_WIDTH; i = i+1) begin
                    if (control_reg[CTRL_WIDTH-i] == 1'b1) begin        
                        data_c1[WIDTH-1-i] <= sd_c1;
                        data_c2[WIDTH-1-i] <= sd_c2;
                    end
                end
            end
    
            wsd <= ws;
            wsd_reg <= wsd;

            if (wsd & wsp) begin
                data_left_c1 <= data_c1;
                data_left_c2 <= data_c2;
            end 
            if (!wsd & wsp) begin
                data_right_c1 <= data_c1;
                data_right_c2 <= data_c2;
            end
        end
    end

    reg [WIDTH-1:0] data_shift;
    wire [WIDTH:0] add_left_channel;
    wire [WIDTH:0] add_right_channel;

    //                                                            (2'b11                        )   2'b10
    //                                                            (2'b01                        )   2'b00
    assign add_right_channel = channel_sel[1] ? (channel_sel[0] ? (data_right_c1 + data_right_c2) : data_right_c2) :
                                                (channel_sel[0] ? (data_right_c1                ) : 33'b0)         ;
    assign add_left_channel  = channel_sel[1] ? (channel_sel[0] ? (data_left_c1 + data_left_c2  ) : data_left_c2) :
                                                (channel_sel[0] ? (data_left_c1                 ) : 33'b0)         ;
    assign sd_out = data_shift[WIDTH-1];

    always @ (negedge sck) begin
        if (reset == 1'b1) begin
            data_shift <= 'b0;
        end else begin
            if (wsp == 1'b1) begin
                if (wsd == 1'b1) begin
                    data_shift <= add_right_channel >> 1;
                end else begin
                    data_shift <= add_left_channel >> 1;
                end
            end else begin
                data_shift <= {data_shift[WIDTH-2:0], 1'b0};
            end
        end
    end
endmodule
