`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2026/05/24 11:00:32
// Design Name: 
// Module Name: tb_rgb2ycbcr_top
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


module tb_rgb2ycbcr_top;

    parameter CLK_PERIOD = 10;
    
    // 設定圖片的真實解析度 (與讀取的.txt 對應)
    parameter IMG_WIDTH  = 1080;
    parameter IMG_HEIGHT = 1350;

    reg         clk;
    reg         rst_n;
    reg  [15:0] active_width;
    reg  [15:0] active_height;

    reg         valid_in;
    reg  [7:0]  r_in;
    reg  [7:0]  g_in;
    reg  [7:0]  b_in;

    wire        valid_y_out;
    wire [7:0]  y_out;
    wire        valid_c_out;
    wire [7:0]  cb_out;
    wire [7:0]  cr_out;

    integer fd_in;
    integer fd_y_out;
    integer fd_c_out;
    integer scan_res;
    reg [23:0] rgb_data; // 暫存從 .txt 讀取的 24-bit RGB 資料

    rgb2ycbcr_top #(
        .MAX_WIDTH(1920),
        .MAX_HEIGHT(1080)
    ) u_top (
        .clk           (clk),
        .rst_n         (rst_n),
        .active_width  (active_width),
        .active_height (active_height),
        
        .valid_in      (valid_in),
        .r_in          (r_in),
        .g_in          (g_in),
        .b_in          (b_in),
        
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
    // 監聽結果並寫入輸出檔
    // ==========================================
    initial begin
        fd_y_out = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/output_top_y.txt", "w");
        fd_c_out = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/output_top_cbcr.txt", "w");

        if (fd_y_out == 0 || fd_c_out == 0) begin
            $display("Error: Failed to create output files.");
            $finish;
        end

        // 平行操作
        fork
            // 監聽 Y 結果
            forever begin
                @(posedge clk);
                if (valid_y_out) begin
                    $fwrite(fd_y_out, "%02X\n", y_out);
                end
            end
            
            // 監聽 CbCr 結果
            forever begin
                @(posedge clk);
                if (valid_c_out) begin
                    $fwrite(fd_c_out, "%02X%02X\n", cb_out, cr_out);
                end
            end
        join
    end

    // ==========================================
    // 讀取輸入檔 .txt 並模擬
    // ==========================================
    initial begin
        rst_n         = 0;
        valid_in      = 0;
        r_in          = 0;
        g_in          = 0;
        b_in          = 0;
        
        active_width  = IMG_WIDTH;
        active_height = IMG_HEIGHT;

        // 開啟原始的 RGB 文字檔
        fd_in = $fopen("C:/Users/david/Desktop/Color_Coordinate_Transform/road.txt", "r");
        if (fd_in == 0) begin
            $display("Error: road.txt not found. Please check the file path.");
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

        #(CLK_PERIOD * 10);

        // 關閉檔案並結束模擬
        $fclose(fd_in);
        $fclose(fd_y_out);
        $fclose(fd_c_out);
        $display("========================================");
        $display("System-Level Top Module Simulation Completed!");
        $display("Data Path: RGB -> YCbCr Core -> 4:2:0 Subsampler");
        $display("Please check output_top_y.txt and output_top_cbcr.txt");
        $display("========================================");
        $finish;
    end
endmodule
