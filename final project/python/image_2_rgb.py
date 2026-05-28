from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 讀取圖片
# ==========================================
img_path = 'road.jpg' # 替換圖片檔名
img = Image.open(img_path).convert('RGB')

img_array = np.array(img)

print(f"圖片解析度 (Height, Width, Channels): {img_array.shape}")
print(f"資料型態: {img_array.dtype} (通常是 uint8，範圍 0~255)")

first_pixel = img_array[0, 0]
print(f"左上角第一顆像素的 RGB 值: R={first_pixel[0]}, G={first_pixel[1]}, B={first_pixel[2]}")


# ==========================================
# 準備 verilog 測資
# ==========================================
# 把 3D 陣列攤平成 1D，並轉成 Hex 寫入 txt 檔 (ex: FF8800)
output_filename = 'input_rgb_hex.txt'

with open(output_filename, 'w') as f:
    flat_pixels = img_array.reshape(-1, 3) 
    
    for pixel in flat_pixels:
        r, g, b = pixel
        hex_str = f"{r:02X}{g:02X}{b:02X}\n"
        f.write(hex_str)

print(f"\n成功！已將 {len(flat_pixels)} 個像素的 RGB 資料寫入 {output_filename}")
print("這份 txt 檔案未來可以直接用 Verilog 的 $readmemh 或 $fscanf 讀取！")

