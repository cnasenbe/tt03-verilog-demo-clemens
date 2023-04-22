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
    wire sd = io_in[3];
    assign io_out[7:0] = {4'b0, wsd, wsp, xor_data_left, xor_data_right}; 

    wire xor_data_left;
    wire xor_data_right;

    reg wsd;
    reg wsd_reg;
    wire wsp;

    reg [WIDTH-1:0] data_left;
    reg [WIDTH-1:0] data_right;
    reg [WIDTH-1:0] data;
    reg [CTRL_WIDTH-1:0] control_reg;
    integer i;

    assign wsp = wsd ^ wsd_reg;
    assign xor_data_left = ^data_left;
    assign xor_data_right = ^data_right;

    always @ (posedge sck) begin
        if (wsp == 1'b1) begin
            control_reg[CTRL_WIDTH-2:0] <= 'b0;
            control_reg[CTRL_WIDTH-1] <= 1'b1;
            data[WIDTH-2:0] <= 'b0;
            data[WIDTH-1] <= sd;
        end else begin
            control_reg[CTRL_WIDTH-1] <= 1'b0;
            for (i = 1; i < CTRL_WIDTH; i = i+1) begin
                control_reg[CTRL_WIDTH-1-i] <= control_reg[CTRL_WIDTH-i];
            end
            for (i = 0; i <= CTRL_WIDTH; i = i+1) begin
                if (control_reg[CTRL_WIDTH-i] == 1'b1) begin        
                    data[WIDTH-1-i] <= sd;
                end
            end
        end
    
        wsd <= ws;
        wsd_reg <= wsd;
        
        if (!wsd & wsp) begin
            data_left <= data;
        end 
        if (wsd & wsp) begin
            data_right <= data;
        end
    end 
endmodule
