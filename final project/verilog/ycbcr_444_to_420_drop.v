`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2026/05/24 10:15:44
// Design Name: 
// Module Name: ycbcr_444_to_420_drop
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


module ycbcr_444_to_420_drop #(
    parameter MAX_WIDTH  = 1920,
    parameter MAX_HEIGHT = 1080
)(
    input  wire        clk,
    input  wire        rst_n,
    
    input  wire [15:0] active_width,
    input  wire [15:0] active_height,
    
    // Input 4:4:4
    input  wire        valid_in,
    input  wire [7:0]  y_in,
    input  wire [7:0]  cb_in,
    input  wire [7:0]  cr_in,
    
    // Output 4:2:0
    output reg         valid_y_out,
    output reg  [7:0]  y_out,
    output reg         valid_c_out,
    output reg  [7:0]  cb_out,
    output reg  [7:0]  cr_out
);

    // ==========================================
    // 座標計數器 (X, Y)
    // ==========================================
    reg [15:0] x_cnt;
    reg [15:0] y_cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            x_cnt <= 16'd0;
            y_cnt <= 16'd0;
        end else if (valid_in) begin
            // 水平計數器：數到當前圖片寬度邊界
            if (x_cnt == active_width - 16'd1) begin
                x_cnt <= 16'd0;
                
                // 垂直計數器：換行時 +1
                if (y_cnt == active_height - 16'd1) begin
                    y_cnt <= 16'd0; // 一整張圖片掃描完畢，回到原點
                end else begin
                    y_cnt <= y_cnt + 16'd1;
                end
            end else begin
                x_cnt <= x_cnt + 16'd1;
            end
        end
    end

    // ==========================================
    // 資料輸出與抽樣邏輯
    // ==========================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            valid_y_out <= 1'b0;
            y_out       <= 8'd0;
            valid_c_out <= 1'b0;
            cb_out      <= 8'd0;
            cr_out      <= 8'd0;
        end else begin
            // -----------------------------------
            // Y：Bypass
            // ----------------------------------
            valid_y_out <= valid_in;
            y_out       <= y_in;

            // -----------------------------------
            // Cb/Cr：4:2:0 Drop 若 X 和 Y 都是偶數就代表要保留
            // -----------------------------------
            if (valid_in && (x_cnt[0] == 1'b0) && (y_cnt[0] == 1'b0)) begin
                valid_c_out <= 1'b1;
                cb_out      <= cb_in;
                cr_out      <= cr_in;
            end else begin
                valid_c_out <= 1'b0;
                cb_out      <= 8'd0; 
                cr_out      <= 8'd0;
            end
        end
    end
endmodule
