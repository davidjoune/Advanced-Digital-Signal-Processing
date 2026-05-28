`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2026/05/23 11:21:12
// Design Name: 
// Module Name: rgb2ycbcr_core
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module rgb2ycbcr_core(
    input  wire        clk,
    input  wire        rst_n,
    
    input  wire        valid_in,
    input  wire [7:0]  r_in,
    input  wire [7:0]  g_in,
    input  wire [7:0]  b_in,
    
    output reg         valid_out,
    output reg  [7:0]  y_out,
    output reg  [7:0]  cb_out,
    output reg  [7:0]  cr_out
);

    // ==========================================
    // 定義 (放大 256 倍)
    // ==========================================
    // Y  =  0.299*R + 0.587*G + 0.114*B ->  77*R + 150*G +  29*B
    // Cb = -0.169*R - 0.331*G + 0.500*B -> -43*R -  85*G + 128*B + 32768
    // Cr =  0.500*R - 0.419*G - 0.081*B -> 128*R - 107*G -  21*B + 32768
    
    // ==========================================
    // Pipeline Stage 1: Multiplier
    // ==========================================
    reg        valid_d1;
    reg [15:0] mult_y_r,  mult_y_g,  mult_y_b;
    reg [15:0] mult_cb_r, mult_cb_g, mult_cb_b;
    reg [15:0] mult_cr_r, mult_cr_g, mult_cr_b;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            valid_d1   <= 1'b0;
            mult_y_r   <= 16'd0; mult_y_g   <= 16'd0; mult_y_b   <= 16'd0;
            mult_cb_r  <= 16'd0; mult_cb_g  <= 16'd0; mult_cb_b  <= 16'd0;
            mult_cr_r  <= 16'd0; mult_cr_g  <= 16'd0; mult_cr_b  <= 16'd0;
        end else begin
            valid_d1   <= valid_in;
            
            if (valid_in) begin
                // Y 乘積
                mult_y_r   <= 8'd77  * r_in;
                mult_y_g   <= 8'd150 * g_in;
                mult_y_b   <= 8'd29  * b_in;
                
                // Cb 乘積
                mult_cb_r  <= 8'd43  * r_in;
                mult_cb_g  <= 8'd85  * g_in;
                mult_cb_b  <= 8'd128 * b_in;
                
                // Cr 乘積
                mult_cr_r  <= 8'd128 * r_in;
                mult_cr_g  <= 8'd107 * g_in;
                mult_cr_b  <= 8'd21  * b_in;
            end
        end
    end

    // ==========================================
    // Pipeline Stage 2: Adder Tree
    // ==========================================
    reg        valid_d2;
    // 使用 18-bit 確保加法不溢位
    reg [17:0] sum_y;
    reg [17:0] sum_cb;
    reg [17:0] sum_cr;
    
    // offset 32768 + 四捨五入補償 128 = 32896
    wire [17:0] ROUNDING_OFFSET = 18'd128;
    wire [17:0] CHROMA_OFFSET   = 18'd32896; 

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            valid_d2 <= 1'b0;
            sum_y    <= 18'd0;
            sum_cb   <= 18'd0;
            sum_cr   <= 18'd0;
        end else begin
            valid_d2 <= valid_d1;
            
            if (valid_d1) begin
                // Y = 77R + 150G + 29B + 128
                sum_y  <= mult_y_r + mult_y_g + mult_y_b + ROUNDING_OFFSET;
                
                // Cb = 128B + 32896 - (43R + 85G)
                sum_cb <= (mult_cb_b + CHROMA_OFFSET) - (mult_cb_r + mult_cb_g); // 避免sum為負數，先加總正數，再減去負數
                
                // Cr = 128R + 32896 - (107G + 21B)
                sum_cr <= (mult_cr_r + CHROMA_OFFSET) - (mult_cr_g + mult_cr_b);
            end
        end
    end

    // ==========================================
    // Pipeline Stage 3: Shift & Clip 如果大於等於 65536 (bit[17:16] != 0)，
	// 強制設為 255，否則取 bit[15:8] (相當於除以 256)
    // ==========================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            valid_out <= 1'b0;
            y_out     <= 8'd0;
            cb_out    <= 8'd0;
            cr_out    <= 8'd0;
        end else begin
            valid_out <= valid_d2;
            
            if (valid_d2) begin
                if (|sum_y[17:16])  y_out <= 8'hFF;
                else                y_out <= sum_y[15:8];

                if (|sum_cb[17:16]) cb_out <= 8'hFF;
                else                cb_out <= sum_cb[15:8];

                if (|sum_cr[17:16]) cr_out <= 8'hFF;
                else                cr_out <= sum_cr[15:8];
            end
        end
    end
endmodule
