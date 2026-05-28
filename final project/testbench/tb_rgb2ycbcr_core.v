`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2026/05/23 11:32:14
// Design Name: 
// Module Name: tb_rgb2ycbcr_core
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


module tb_rgb2ycbcr_core;

    parameter CLK_PERIOD = 10;

    reg        clk;
    reg        rst_n;
    reg        valid_in;
    reg  [7:0] r_in;
    reg  [7:0] g_in;
    reg  [7:0] b_in;

    wire       valid_out;
    wire [7:0] y_out;
    wire [7:0] cb_out;
    wire [7:0] cr_out;

    integer fd_in;
    integer fd_out;
    integer scan_res;
    
    // 暫存讀取到的一行 24-bit RGB 十六進位資料
    reg [23:0] rgb_data;

    rgb2ycbcr_core u_core (
        .clk        (clk),
        .rst_n      (rst_n),
        .valid_in   (valid_in),
        .r_in       (r_in),
        .g_in       (g_in),
        .b_in       (b_in),
        .valid_out  (valid_out),
        .y_out      (y_out),
        .cb_out     (cb_out),
        .cr_out     (cr_out)
    );

    initial begin
        clk = 0;
        forever #(CLK_PERIOD / 2) clk = ~clk;
    end

    // ==========================================
    // 監聽結果並寫入輸出檔案
    // ==========================================
    initial begin
        fd_out = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/output_ycbcr_hex.txt", "w");
        if (fd_out == 0) begin
            $display("Error: Failed to create or open output_ycbcr_hex.txt");
            $finish;
        end
        
        forever begin
            @(posedge clk);
            if (valid_out) begin
                // 以十六進位格式寫入，例如 "FF8080"
                $fwrite(fd_out, "%02X%02X%02X\n", y_out, cb_out, cr_out);
            end
        end
    end

    // ==========================================
    // 讀取輸入檔並模擬
    // ==========================================
    initial begin
        rst_n    = 0;
        valid_in = 0;
        r_in     = 0;
        g_in     = 0;
        b_in     = 0;

        // 開啟輸入檔案
        fd_in = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/road.txt", "r");
        if (fd_in == 0) begin
            $display("Error: input_rgb_hex.txt not found. Please check the file path.");
            $finish;
        end

        #(CLK_PERIOD * 2);
        rst_n = 1;
        #(CLK_PERIOD * 2);

        while (!$feof(fd_in)) begin
            @(negedge clk);
            
            scan_res = $fscanf(fd_in, "%h\n", rgb_data);
            
            if (scan_res == 1) begin
                valid_in = 1;
                r_in     = rgb_data[23:16];
                g_in     = rgb_data[15:8];
                b_in     = rgb_data[7:0];
            end else begin
                valid_in = 0;
            end
        end

        @(negedge clk);
        valid_in = 0;

        #(CLK_PERIOD * 5);

        $fclose(fd_in);
        $fclose(fd_out);
        $display("========================================");
        $display("Hardware simulation completed!");
        $display("Please return to Python to check output_ycbcr_hex.txt");
        $display("========================================");
        $finish;
    end
endmodule
