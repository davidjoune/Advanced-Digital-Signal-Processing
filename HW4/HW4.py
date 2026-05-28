import cv2
import numpy as np
import matplotlib.pyplot as plt


# %% Input setting
A = cv2.imread("cat1.jpg", cv2.IMREAD_GRAYSCALE)                 # 圖片 A
B = cv2.imread("cat2.jpg", cv2.IMREAD_GRAYSCALE)                 # 圖片 B
C = A * 0.5 + 127.5                                                      # 圖片 C 設定為 A 圖變亮
L = 255


def ssim(a, b, c1, c2):                                                  # SSIM
    mean_a = np.mean(a)
    mean_b = np.mean(b)
    variance_a = np.mean(np.square(a - mean_a))
    variance_b = np.mean(np.square(b - mean_b))
    covariance_ab = np.mean((a - mean_a) * (b - mean_b))

    numerator1 = (2 * mean_a * mean_b + (c1 * L) ** 2)
    numerator2 = (2 * covariance_ab + (c2 * L) ** 2)
    denominator1 = (mean_a ** 2 + mean_b ** 2 + (c1 * L) ** 2)
    denominator2 = (variance_a + variance_b + (c2 * L) ** 2)

    return (numerator1 * numerator2) / (denominator1 * denominator2)


ssim_value = ssim(A, C, 1 / (L ** 0.5), 1 / (L ** 0.5))                 # 計算ssim值
print("SSIM:", ssim_value)

# Plot the images and SSIM value
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.imshow(A, cmap='gray')                                              # 顯示 A 圖片灰階
ax1.set_title('Image A')
ax1.axis('off')
ax2.imshow(C, cmap='gray')                                              # 顯示 C 圖片灰階
ax2.set_title('Image C')
ax2.axis('off')

fig.suptitle(f'SSIM: {ssim_value:.4f}', fontsize=16)
fig.tight_layout()
plt.show()
