from tmp_interpolation import *


if __name__ == '__main__':
    rawData = azidendf[2500:2530]
    plt.subplot(2, 2, 1)
    data_all = testFunction(rawData, dealStep=3)
    showImage(data_all)
    plt.title("增强前",fontsize=20)
    plt.ylabel("深度", fontsize=18)
    plt.xlabel("方位",  fontsize=18)
    plt.subplot(2, 2, 3)
    histOfGray(data_all)
    plt.subplot(2, 2, 2)
    data_IC = IntensifyContrast_use(data_all, doMean=False,kind="sigmod_mean")
    showImage(data_IC)
    plt.title("增强后",fontsize=20)
    plt.xlabel("方位",  fontsize=18)
    plt.subplot(2, 2, 4)
    # data_IC = IntensifyContrast_use(data_all)
    histOfGray(data_IC)
    plt.show()