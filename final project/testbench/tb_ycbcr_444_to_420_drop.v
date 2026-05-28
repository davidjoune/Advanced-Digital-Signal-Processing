`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2026/05/24 10:17:24
// Design Name: 
// Module Name: tb_ycbcr_444_to_420_drop
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


module tb_ycbcr_444_to_420_drop;

    parameter CLK_PERIOD = 10;
    
    parameter IMG_WIDTH  = 1080;
    parameter IMG_HEIGHT = 1350;

    reg         clk;
    reg         rst_n;
    reg  [15:0] active_width;
    reg  [15:0] active_height;

    reg         valid_in;
    reg  [7:0]  y_in;
    reg  [7:0]  cb_in;
    reg  [7:0]  cr_in;

    wire        valid_y_out;
    wire [7:0]  y_out;
    wire        valid_c_out;
    wire [7:0]  cb_out;
    wire [7:0]  cr_out;

    integer fd_in;
    integer fd_y_out;
    integer fd_c_out;
    integer scan_res;
    reg [23:0] ycbcr_data;

    ycbcr_444_to_420_drop #(
        .MAX_WIDTH(1920),
        .MAX_HEIGHT(1080)
    ) u_drop (
        .clk           (clk),
        .rst_n         (rst_n),
        .active_width  (active_width),
        .active_height (active_height),
        .valid_in      (valid_in),
        .y_in          (y_in),
        .cb_in         (cb_in),
        .cr_in         (cr_in),
        .valid_y_out   (valid_y_out),
        .y_out         (y_out),
        .valid_c_out   (valid_c_out),
        .cb_out        (cb_out),
        .cr_out        (cr_out)
    );

    initial begin
        clk = 0;
        forever #(CLK_PERIOD / 2) clk = ~clk;
    end

    // ==========================================
    // 監聽結果並寫入輸出檔案
    // ==========================================
    initial begin
        fd_y_out = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/output_420_y.txt", "w");
        fd_c_out = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/output_420_cbcr.txt", "w");

        if (fd_y_out == 0 || fd_c_out == 0) begin
            $display("Error: Failed to create output files.");
            $finish;
        end

        // fork-join 啟動兩個平行的監聽迴圈
        fork
            forever begin
                @(posedge clk);
                if (valid_y_out) begin
                    $fwrite(fd_y_out, "%02X\n", y_out);
                end
            end
            
            forever begin
                @(posedge clk);
                if (valid_c_out) begin
                    $fwrite(fd_c_out, "%02X%02X\n", cb_out, cr_out);
                end
            end
        join
    end

    // ==========================================
    // 讀取輸入檔並模擬
    // ==========================================
    initial begin
        rst_n         = 0;
        valid_in      = 0;
        y_in          = 0;
        cb_in         = 0;
        cr_in         = 0;
        
        active_width  = IMG_WIDTH;
        active_height = IMG_HEIGHT;

        // 讀取上一個模組產生的 4:4:4 YCbCr .txt檔
        fd_in = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/ycbcr_road.txt", "r");
        if (fd_in == 0) begin
            $display("Error: output_ycbcr_hex.txt not found. Please check the file path.");
            $finish;
        end

        #(CLK_PERIOD * 2);
        rst_n = 1;
        #(CLK_PERIOD * 2);

        while (!$feof(fd_in)) begin
            @(negedge clk);
            scan_res = $fscanf(fd_in, "%h\n", ycbcr_data);
            if (scan_res == 1) begin
                valid_in = 1;
                y_in     = ycbcr_data[23:16];
                cb_in    = ycbcr_data[15:8];
                cr_in    = ycbcr_data[7:0];
            end else begin
                valid_in = 0;
            end
        end

        @(negedge clk);
        valid_in = 0;

        #(CLK_PERIOD * 5);

        $fclose(fd_in);
        $fclose(fd_y_out);
        $fclose(fd_c_out);
        $display("========================================");
        $display("4:2:0 Subsampling simulation completed!");
        $display("Please check output_420_y.txt and output_420_cbcr.txt");
        $display("========================================");
        $finish;
    end

endmodule
