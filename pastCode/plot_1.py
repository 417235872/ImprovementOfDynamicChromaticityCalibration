from tmp_interpolation import *


if __name__ == '__main__':
    rawData = azidendf[2100:2130]
    d_smoothed=smoothlyData(rawData)
    plt.subplot(1,2,1)
    showAzimuthal(rawData)
    plt.title("原始数据", fontsize=35)
    plt.xlabel("深度",  fontsize=35)
    plt.ylabel("密度",  fontsize=35)
    plt.subplot(1, 2, 2)
    showAzimuthal(d_smoothed)
    plt.title("平滑降噪", fontsize=35)
    plt.xlabel("深度",  fontsize=35)
    plt.ylabel("密度",  fontsize=35)
    plt.show()