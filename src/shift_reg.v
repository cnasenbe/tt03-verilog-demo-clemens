module shift_reg #(
    parameter REG_WIDTH=8
) (  
    input d,
    input clk,
    input en,
    input rst,
    output reg [REG_WIDTH-1:0] out
);    
   always @ (posedge clk)
      if (rst)
         out <= 0;
      else begin
         if (en)
            out <= {out[REG_WIDTH-2:1], d};
      end
endmodule
