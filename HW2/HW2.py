import numpy as np
import matplotlib.pyplot as plt

k = 17
N = 2*k+1

# step1 設定Hd(m/N)
Hd = []

for i in range(N):
    if i == 0:
        Hd.append(0)
    elif i == 1:
        Hd.append(-0.9j)
    elif 1 < i < k:
        Hd.append(-1j)
    elif i == k:
        Hd.append(-0.6j)
    elif i == k+1:
        Hd.append(0.6j)
    elif k+1 < i < N-1:
        Hd.append(1j)
    elif i == N-1:
        Hd.append(0.9j)


Hd = np.array(Hd)

"""
plt.figure(figsize=(10, 5))
plt.plot(Hd.imag, linewidth=2)
plt.title('Hilbert Transform Frequency Response (Imaginary Part)', fontsize=14)
plt.xlabel('Sample', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
"""

# step2 計算Hd的IDFT成為r1[n]
r1_n = np.fft.ifft(Hd)
"""
plt.figure(figsize=(10, 5))
plt.stem(range(len(r1_n)), r1_n.real, linefmt='C0-', markerfmt='C0o', basefmt='C0-', label='r1[n]')
plt.title('Inverse Fourier Transform (IFFT) Result', fontsize=14)
plt.xlabel('Sample', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.grid(True)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
"""

# step3 把r1[n]後面的點與前面做交換,並調整索引值
indices = np.arange(-k, k+1)
r_n = r1_n[np.mod(indices, N)]

plt.figure(figsize=(10, 5))
plt.stem(indices, r_n.real, linefmt='C0-', markerfmt='C0o', basefmt='C0-', label='r[n]')
plt.title('Rearranged Impulse Response', fontsize=14)
plt.xlabel('Sample', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.grid(True)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()

# step4 對重新排列後的 r_n 進行傅立葉變換,計算frequency response R(F)
F = np.arange(0.0, 1.0, 1/10000)
n = np.arange(-k, k+1)
R_F = np.zeros_like(F)

for i in range(len(F)):
    R_F[i] = np.sum(r_n * np.exp(-1j * 2 * np.pi * F[i] * n)).imag


def hilbert(x):
    if x == 0:
        return 0
    elif 0 < x <= 0.5:
        return -1j
    elif 0.5 < x < 1:
        return 1j


plt.figure(figsize=(10, 5))
plt.plot(F, R_F, linewidth=2, label='R(F)')
plt.plot(F, [hilbert(i).imag for i in F], linewidth=2, linestyle='--', label='H_d(F)')
plt.title("Frequency Response", fontsize=16)
plt.xlabel("Frequency", fontsize=14)
plt.ylabel("Amplitude", fontsize=14)
plt.grid(True)
plt.legend(fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
