from tmp_interpolation import *


if __name__ == '__main__':
    rawData = azidendf[2100:2130]
    d_smoothed = smoothlyData(rawData)
    plt.figure(figsize=(7, 15))
    plt.subplot(1, 2, 1)
    showImage(rawData,vmax=np.max(d_smoothed.values))
    plt.title("原始数据",fontsize=20)
    plt.ylabel("深度", fontsize=18)
    plt.xlabel("方位",  fontsize=18)
    plt.subplot(1, 2, 2)
    showImage(d_smoothed)
    plt.title("平滑降噪",fontsize=20)
    plt.xlabel("方位",  fontsize=18)
    plt.show()