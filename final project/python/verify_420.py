import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image

# 確保長寬與原始 road 圖片一致
WIDTH = 1080
HEIGHT = 1350  

# ==========================================
# verilog 輸出結果路徑
# ==========================================
y_file = r"C:\Users\david\Desktop\Color_Coordinate_Transform\road_top_y.txt"
c_file = r"C:\Users\david\Desktop\Color_Coordinate_Transform\road_top_cbcr.txt"

# 原始 .jpg 圖片路徑
original_img_file = r"C:\Users\david\Desktop\Color_Coordinate_Transform\road.jpg" 

print("正在讀取硬體 4:2:0 輸出檔案...")

# 讀取 Y
try:
    with open(y_file, 'r') as f:
        y_data = [int(line.strip(), 16) for line in f]
except FileNotFoundError:
    print(f"❌ 找不到 {y_file}！")
    exit()

# 讀取 CbCr
try:
    with open(c_file, 'r') as f:
        lines = f.readlines()
        cb_data = [int(line.strip()[0:2], 16) for line in lines]
        cr_data = [int(line.strip()[2:4], 16) for line in lines]
except FileNotFoundError:
    print(f"❌ 找不到 {c_file}！")
    exit()

# 防呆
expected_y_len = WIDTH * HEIGHT
expected_c_len = (WIDTH // 2) * (HEIGHT // 2)

if len(y_data) != expected_y_len or len(cb_data) != expected_c_len:
    print("❌ 錯誤：檔案內的資料行數與設定的解析度不符！")
    print(f"預期 Y: {expected_y_len} 行, 實際: {len(y_data)} 行")
    print(f"預期 C: {expected_c_len} 行, 實際: {len(cb_data)} 行")
    exit()

# ==========================================
# 重組 2D YCbCr
# ==========================================
print("正在進行色度上採樣與陣列重組...")

# 將一維資料折疊成二維矩陣
y_img = np.array(y_data, dtype=np.float32).reshape((HEIGHT, WIDTH))
cb_img = np.array(cb_data, dtype=np.float32).reshape((HEIGHT // 2, WIDTH // 2))
cr_img = np.array(cr_data, dtype=np.float32).reshape((HEIGHT // 2, WIDTH // 2))

# CbCr共用
cb_upsampled = np.repeat(np.repeat(cb_img, 2, axis=0), 2, axis=1)
cr_upsampled = np.repeat(np.repeat(cr_img, 2, axis=0), 2, axis=1)

# ==========================================
# YCbCr 還原 RGB
# ==========================================
print("正在執行 YCbCr 到 RGB 的逆向轉換...")

Cb = cb_upsampled - 128.0
Cr = cr_upsampled - 128.0

R = y_img + 1.402 * Cr
G = y_img - 0.344136 * Cb - 0.714136 * Cr
B = y_img + 1.772 * Cb

# ==========================================
# 截斷
# ==========================================
rgb_array = np.stack((R, G, B), axis=2)
rgb_array = np.clip(rgb_array, 0, 255).astype(np.uint8)

# ==========================================
# 計算 PSNR
# ==========================================
print("正在計算 PSNR 數據...")

try:
    # 讀取原始圖片並轉成 numpy 陣列
    original_img = Image.open(original_img_file).convert('RGB')
    
    # 防呆
    if original_img.size != (WIDTH, HEIGHT):
         print(f"⚠️ 警告：原圖尺寸 {original_img.size} 與設定的 ({WIDTH}, {HEIGHT}) 不符！")
         
    original_array = np.array(original_img, dtype=np.float32)
    hw_array = rgb_array.astype(np.float32) # 轉成 float32 避免相減時溢位
    
    # 計算 MSE
    mse = np.mean((original_array - hw_array) ** 2)
    
    if mse == 0:
        print("PSNR: 無限大 (與原圖完全 100% 一致)")
    else:
        max_pixel = 255.0
        psnr = 10 * math.log10((max_pixel ** 2) / mse)
        print(f"----------------------------------------")
        print(f"MSE (均方誤差): {mse:.4f}")
        print(f"PSNR (峰值信噪比): {psnr:.2f} dB")
        print(f"----------------------------------------")
        
except FileNotFoundError:
     print(f"❌ 找不到原始圖片 {original_img_file}，無法計算 PSNR。")

print("轉換完成！正在顯示圖片...")
plt.figure(figsize=(10, 8))
plt.imshow(rgb_array)
plt.title(f"Reconstructed RGB (4:2:0 Drop Strategy)\nPSNR: {psnr:.2f} dB" if 'psnr' in locals() else "Reconstructed RGB")
plt.axis('off')
plt.tight_layout()
plt.show()