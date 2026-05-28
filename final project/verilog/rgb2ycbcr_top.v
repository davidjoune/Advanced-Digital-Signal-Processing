`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2026/05/24 10:59:09
// Design Name: 
// Module Name: rgb2ycbcr_top
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


module rgb2ycbcr_top #(
    parameter MAX_WIDTH  = 1920,
    parameter MAX_HEIGHT = 1080 
)(

    input  wire        clk,
    input  wire        rst_n,
    
    input  wire [15:0] active_width,
    input  wire [15:0] active_height,
	
    input  wire        valid_in,
    input  wire [7:0]  r_in,
    input  wire [7:0]  g_in,
    input  wire [7:0]  b_in,
    
    output wire        valid_y_out,
    output wire [7:0]  y_out,
    
    output wire        valid_c_out,
    output wire [7:0]  cb_out,
    output wire [7:0]  cr_out
);

    wire        core_valid_out;
    wire [7:0]  core_y_out;
    wire [7:0]  core_cb_out;
    wire [7:0]  core_cr_out;

    rgb2ycbcr_core u_core (
        .clk        (clk),
        .rst_n      (rst_n),
        .valid_in   (valid_in),
        .r_in       (r_in),
        .g_in       (g_in),
        .b_in       (b_in),
        
        .valid_out  (core_valid_out),
        .y_out      (core_y_out),
        .cb_out     (core_cb_out),
        .cr_out     (core_cr_out)
    );

    ycbcr_444_to_420_drop #(
        .MAX_WIDTH  (MAX_WIDTH),
        .MAX_HEIGHT (MAX_HEIGHT)
    ) u_drop (
        .clk           (clk),
        .rst_n         (rst_n),
        .active_width  (active_width),
        .active_height (active_height),

        .valid_in      (core_valid_out),
        .y_in          (core_y_out),
        .cb_in         (core_cb_out),
        .cr_in         (core_cr_out),
        
        .valid_y_out   (valid_y_out),
        .y_out         (y_out),
        .valid_c_out   (valid_c_out),
        .cb_out        (cb_out),
        .cr_out        (cr_out)
    );
endmodule
