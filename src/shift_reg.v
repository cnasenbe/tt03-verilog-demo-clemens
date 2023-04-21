module shift_reg #(
    parameter MSB=8
) (  
    input d,
    input clk,
    input en,
    input rst,
    output reg [MSB-1:0] out
);    
   always @ (posedge clk)
      if (rst)
         out <= 0;
      else begin
         if (en)
            out <= {d, out[MSB-1:1]};
      end
endmodule
