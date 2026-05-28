import numpy as np
import matplotlib.pyplot as plt

# 圖片讀取路徑
image = plt.imread('C:/Users/david/Downloads/input.jpg').astype(np.float32)
print('image.shape：', image.shape)

# 定義轉換矩陣
transform_matrix = np.array([[0.299, 0.587, 0.114],
                             [-0.169, -0.331, 0.500],
                             [0.500, -0.419, -0.081]])

# 對圖片進行轉換
ycbcr_image = np.dot(image, transform_matrix.T)

print('ycbcr_image.shape：', ycbcr_image.shape)

y = ycbcr_image[:, :, 0]
cb = ycbcr_image[:, :, 1]
cr = ycbcr_image[:, :, 2]

print('y.shape：', y.shape)
print('cb.shape：', cb.shape)
print('cr.shape：', cr.shape)

cb_compressed = cb[::2, ::2]
cr_compressed = cr[::2, ::2]

print('cb_compressed.shape：', cb_compressed.shape)
print('cr_compressed.shape：', cr_compressed.shape)

# 重新建構 Cb
cb_reconstructed = np.zeros_like(cb)
cb_reconstructed[::2, ::2] = cb_compressed

# 對奇數col進行插值
if cb_reconstructed.shape[1] % 2 == 0:
    cb_reconstructed[::2, 1:-1:2] = (cb_reconstructed[::2, :-2:2] + cb_reconstructed[::2, 2::2]) * 0.5
    cb_reconstructed[::2, -1] = cb_reconstructed[::2, -2]
else:
    cb_reconstructed[::2, 1::2] = (cb_reconstructed[::2, :-1:2] + cb_reconstructed[::2, 2::2]) * 0.5

# 對奇數row進行插值
if cb_reconstructed.shape[0] % 2 == 0:
    cb_reconstructed[1:-1:2, :] = (cb_reconstructed[:-2:2, :] + cb_reconstructed[2::2, :]) * 0.5
    cb_reconstructed[-1, :] = cb_reconstructed[-2, :]
else:
    cb_reconstructed[1::2, :] = (cb_reconstructed[:-1:2, :] + cb_reconstructed[2::2, :]) * 0.5

print('check：cb_reconstructed[-5:, -5:] ：')
print(cb_reconstructed[-5:, -5:])

# 重新建構 Cr
cr_reconstructed = np.zeros_like(cr)
cr_reconstructed[::2, ::2] = cr_compressed

# 對奇數col進行插值
if cr_reconstructed.shape[1] % 2 == 0:
    cr_reconstructed[::2, 1:-1:2] = (cr_reconstructed[::2, :-2:2] + cr_reconstructed[::2, 2::2]) * 0.5
    cr_reconstructed[::2, -1] = cr_reconstructed[::2, -2]
else:
    cr_reconstructed[::2, 1::2] = (cr_reconstructed[::2, :-1:2] + cr_reconstructed[::2, 2::2]) * 0.5

# 對奇數row進行插值
if cr_reconstructed.shape[0] % 2 == 0:
    cr_reconstructed[1:-1:2, :] = (cr_reconstructed[:-2:2, :] + cr_reconstructed[2::2, :]) * 0.5
    cr_reconstructed[-1, :] = cr_reconstructed[-2, :]
else:
    cr_reconstructed[1::2, :] = (cr_reconstructed[:-1:2, :] + cr_reconstructed[2::2, :]) * 0.5

print('check：cr_reconstructed[-5:, -5:] ：')
print(cr_reconstructed[-5:, -5:])

# 將重建的 Cb 和 Cr 與 Y 結合
ycbcr_reconstructed = np.stack((y, cb_reconstructed, cr_reconstructed), axis=-1)

print('ycbcr_reconstructed.shape：', ycbcr_reconstructed.shape)

# YCbCr 轉換回 RGB 的轉換矩陣
inverse_transform_matrix = np.linalg.inv(transform_matrix)

# 變回 RGB
rgb_reconstructed = np.dot(ycbcr_reconstructed, inverse_transform_matrix.T)

print('rgb_reconstructed.shape：', rgb_reconstructed.shape)

print('以上為我在測試程式正不正確><')

# 顯示原始的圖像和重建後的圖像
plt.subplot(1, 2, 1)
plt.imshow(image/255)
plt.title('Original Image')
plt.subplot(1, 2, 2)
plt.imshow(rgb_reconstructed/255)
plt.title('Reconstructed Image')
plt.show()
