import numpy as np
import matplotlib.pyplot as plt

N = 17
fs = 6000
delta = 0.0001
k = int((N - 1) / 2)
F0 = np.array([0, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])  # k+2=10

E1 = 1000  # 很大的數，確保第一次進入迴圈
iteration = 0

while True:

    # STEP2 求出S矩陣 (AS=H)
    A = np.zeros([k + 2, k + 2])
    hd = np.zeros(k + 2)
    for m in range(0, k + 2):
        for n in range(0, k + 1):
            A[m, n] = np.cos(2 * np.pi * n * F0[m])
        cutoff = 1350 / fs
        A[m, k + 1] = (-1)**m * 1/(0.6 if F0[m] > cutoff else 1)
        hd[m] = int(F0[m] <= cutoff)

    s = np.linalg.inv(A).dot(hd)

    # STEP3 計算R[f]、求出error
    F = np.linspace(0, 0.5, 5001)
    R = np.zeros([F.shape[0]])
    hd = np.zeros([F.shape[0]])
    w = np.zeros([F.shape[0]])
    for f in range(0, F.shape[0]):

        # 計算R[f]
        temp = 0
        for n in range(0, k + 1):
            temp += s[n] * np.cos(2 * np.pi * n * F[f])
        R[f] = temp

        # 設定hd[f]
        cutoff = 1350 / fs
        hd[f] = int(F[f] <= cutoff)

        # 設定w[f]
        cutoff2 = 1200 / fs
        cutoff3 = 1500 / fs
        w[f] = (0.6 if F[f] >= cutoff3 else (1 if F[f] <= cutoff2 else 0))

    err = (R - hd) * w

    # STEP4 找出極值點，並分配K+2個來更新F0
    extreme_point = []
    extreme_value = []
    boundary_point = []
    boundary_value = []

    n = F.shape[0]

    for i in range(n):
        curr_err = err[i]
        if i == 0:
            if curr_err > 0 and curr_err > err[i + 1]:
                boundary_point.append(F[i])
                boundary_value.append(abs(curr_err))
            elif curr_err < 0 and curr_err <= err[i + 1]:
                boundary_point.append(F[i])
                boundary_value.append(abs(curr_err))
        elif i == n - 1:
            if curr_err > err[i - 1] and curr_err > 0:
                boundary_point.append(F[i])
                boundary_value.append(abs(curr_err))
            elif curr_err < err[i - 1] and curr_err < 0:
                boundary_point.append(F[i])
                boundary_value.append(abs(curr_err))
        else:
            prev_err = err[i - 1]
            next_err = err[i + 1]
            if curr_err > prev_err and curr_err > next_err:
                extreme_point.append(F[i])
                extreme_value.append(curr_err)
            elif curr_err < prev_err and curr_err < next_err:
                extreme_point.append(F[i])
                extreme_value.append(curr_err)

    while len(extreme_value) < (k + 2):
        if boundary_value:
            temp_value = max(boundary_value)
            index = boundary_value.index(temp_value)
            boundary_value.remove(temp_value)
            extreme_value.append(temp_value)
            temp_point = boundary_point.pop(index)
            extreme_point.append(temp_point)
        else:
            break

    (extreme_point, extreme_value) = (list(t) for t in zip(*sorted(zip(extreme_point, extreme_value))))

    F0 = np.array(extreme_point)

    # 作圖找出最大誤差值(每次疊代)，順便印出來
    max_err = np.max(np.abs(err))
    max_err_idx = np.argmax(np.abs(err))
    plt.figure()
    plt.plot(F, err)
    plt.scatter(F[max_err_idx], err[max_err_idx], c='r', marker='x', s=80, label=f'Max Error = {max_err:.5f}')
    plt.legend()
    plt.xlabel('Frequency')
    plt.ylabel('Error')
    plt.title(f'Iteration {iteration}')
    plt.show()

    if iteration >= 0:
        print(f'Iteration {iteration} max_err is : {max_err:.5f}')

    # STEP5 判斷error有沒有收斂
    E0 = max(abs(err))

    if abs(E1-E0) < delta:
        break
    else:
        E1 = E0
        iteration += 1


# STEP6 收斂完跳出迴圈，重新找出所有極值點，不限只有K+2個
err = (R - hd) * w
extreme_point = []
extreme_value = []
boundary_point = []
boundary_value = []

n = F.shape[0]

for i in range(n):
    curr_err = err[i]
    if i == 0:
        if curr_err > 0 and curr_err > err[i + 1]:
            boundary_point.append(F[i])
            boundary_value.append(abs(curr_err))
        elif curr_err < 0 and curr_err <= err[i + 1]:
            boundary_point.append(F[i])
            boundary_value.append(abs(curr_err))
    elif i == n - 1:
        if curr_err > err[i - 1] and curr_err > 0:
            boundary_point.append(F[i])
            boundary_value.append(abs(curr_err))
        elif curr_err < err[i - 1] and curr_err < 0:
            boundary_point.append(F[i])
            boundary_value.append(abs(curr_err))
    else:
        prev_err = err[i - 1]
        next_err = err[i + 1]
        if curr_err > prev_err and curr_err > next_err:
            extreme_point.append(F[i])
            extreme_value.append(curr_err)
        elif curr_err < prev_err and curr_err < next_err:
            extreme_point.append(F[i])
            extreme_value.append(curr_err)

while len(extreme_value) < (k + 2):
    if boundary_value:
        temp_value = max(boundary_value)
        index = boundary_value.index(temp_value)
        boundary_value.remove(temp_value)
        extreme_value.append(temp_value)
        temp_point = boundary_point.pop(index)
        extreme_point.append(temp_point)
    else:
        break

(extreme_point, extreme_value) = (list(t) for t in zip(*sorted(zip(extreme_point, extreme_value))))

F0 = np.array(extreme_point)


# 作圖 error 找出最大誤差(最後結果)
max_err = np.max(np.abs(err))
max_err_idx = np.argmax(np.abs(err))
plt.figure()
plt.plot(F, err)
plt.scatter(F[max_err_idx], err[max_err_idx], c='r', marker='x', s=80, label=f'Max Error = {max_err:.5f}')
plt.legend()
plt.xlabel('Frequency')
plt.ylabel('Error')
plt.title(f'Iteration {iteration+1}')
plt.show()

print(f'Iteration {iteration+1} max_err is : {max_err:.5f}')


# 作圖 frequency response
extreme_R = [R[F == f][0] for f in extreme_point]

plt.figure(figsize=(8, 6))
plt.plot(F, R, label='H(F)')
plt.plot(F, hd, label='Hd(F)')
plt.scatter(extreme_point, extreme_R, color='r', marker='o', label='Extremes')

plt.axvline(x=1200/fs, color='g', linestyle='--', label='Transition Start')
plt.axvline(x=1500/fs, color='r', linestyle='--', label='Transition End')

plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.xlim(0, 0.5)
plt.ylim(-0.2, 1.2)
plt.legend()
plt.title('Frequency Response')
plt.grid(True)
plt.show()


# 作圖 impulse response
h_n = np.zeros([N])
y = np.zeros([N])

for i in range(0, N):
    if i < k:
        h_n[i] = s[k-i] / 2
    elif i == k:
        h_n[i] = s[0]
    elif i > k:
        h_n[i] = s[i-k] / 2

n = np.arange(N)
plt.figure(figsize=(10, 6))
plt.stem(n, h_n)

plt.plot(n, y, color='b', linestyle='-', label='Zero Reference')
plt.xlabel('n', fontsize=14)
plt.ylabel('h[n]', fontsize=14)
plt.title('Impulse Response', fontsize=16)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
