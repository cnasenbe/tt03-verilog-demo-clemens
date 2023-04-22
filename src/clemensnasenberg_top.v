module clemensnasenberg_top  #(
    parameter WIDTH=24
) (  
    input [7:0] io_in,
    output [7:0] io_out
);
    wire sck = io_in[0];
    wire reset = io_in[1];
    wire ws = io_in[2];
    wire sd1 = io_in[3];
    wire sd2 = io_in[4];
    wire sd_out;
    assign io_out[7] = sd_out;
    //Debug out for now
    //assign io_out[7:0] = {7'b0,data[24]};
    assign io_out[6:0] = {data[24],count[2],start,carry,data[2],data[1],data[0]};
    wire ws_rising_pulse;

    reg ws_edge;
    reg carry;
    reg [WIDTH:0] data; //width+1 because add overflow
    reg [$clog2(WIDTH):0] count;
    reg start;

    always @ (negedge sck) begin
        if (reset) begin
            data <= 'b0;
            count <= 0;
            start <= 1'b0;
            carry <= 1'b0;
            ws_edge <= 1'b0;
        end else begin
            ws_edge <= ws;
            if (ws_rising_pulse == 1'b1) begin
                count <= 0;
                carry <= 1'b0;
                start <= 1'b1;
            end
            if (count == WIDTH-1) begin 
                start <= 1'b0;
            end
            if (start == 1'b1) begin
                {carry, data[count]} <= sd1 + sd2 + carry;
                count <= count + 1;
            end
        end
    end
    assign ws_rising_pulse = ws_edge ^ ws;
    assign sd_out = count>0 ? data[count-1] : 1'b0;

endmodule
