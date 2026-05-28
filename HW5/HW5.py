import numpy as np
import cmath

def dft(f):
    N = len(f)
    F = np.zeros(N, dtype=complex)
    for m in range(N):
        for n in range(N):
            F[m] += f[n] * cmath.exp(-2j * cmath.pi * m * n / N)
    return F

# 輸入實數序列 f1 和 f2
f1 = [1, 2, 3, 4]
f2 = [4, 8, 7, 3]

# 合併 f1 和 f2，得到 f3
f3 = [f1[i] + 1j*f2[i] for i in range(len(f1))]

# 對 f3 進行 DFT
F3 = dft(f3)

# 計算得出 F1[m] 和 F2[m]
N = len(F3)
F1 = [0.5 * (F3[0] + np.conj(F3[0]))]                # m=0 的情況
F2 = [-0.5j * (F3[0] - np.conj(F3[0]))]              # m=0 的情況

for m in range(1, N):
    F1.append(0.5 * (F3[m] + np.conj(F3[N-m])))      # m 後續的情況
    F2.append(-0.5j * (F3[m] - np.conj(F3[N-m])))    # m 後續的情況

# 對結果四捨五入，控制在小數點2位
F1 = np.round(F1, 2)
F2 = np.round(F2, 2)

# 印結果~
print("Input real sequence f1[n]:")
print(f1)

print("Input real sequence f2[n]:")
print(f2)

print("DFT Result F1:")
print(F1)

print("DFT Result F2:")
print(F2)
