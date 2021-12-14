from tmp_interpolation import *


if __name__ == '__main__':
    rawData = azidendf[2100:2130]
    d_smoothed = smoothlyData(rawData)
    kinds = ["linear", "quadratic", "cubic"]
    kinds_cn = ["线性插值",'平方插值','三次样条']
    plt.subplot(1, 4, 1)
    showImage(d_smoothed)
    plt.title("插值前",fontsize=20)
    plt.ylabel("深度", fontsize=18)
    plt.xlabel("方位",  fontsize=18)
    # plt.subplot(1, 4, 3)
    for i in range(3):
        plt.subplot(1,4,2+i)
        data_interpolation=interpolation(d_smoothed,kind=kinds[i],tarNumb=720)
        showImage(data_interpolation)
        plt.title("{}".format(kinds_cn[i]),fontsize=20)
        plt.xlabel("方位", fontsize=18)
    plt.show()