from tmp_interpolation import *


if __name__ == '__main__':
    plt.figure(figsize=(7, 15))
    rawData=azigamdf[2200:2670]
    plt.subplot(1, 4, 1)
    showImage(rawData)
    plt.title("原始数据",fontsize=15)
    plt.ylabel("深度", fontsize=13)
    plt.xlabel("方位",  fontsize=13)
    plt.subplot(1,4,2)
    showImage(testFunction(rawData))
    plt.title("降噪\n插值\n静态色度标定",fontsize=15)
    plt.xlabel("方位",  fontsize=13)
    plt.subplot(1,4,3)
    def fd(data:pd.DataFrame):
        return testFunction(data,dealStep=3)
    data_after = dynamicOperation(rawData,fd)
    showImage(data_after)
    plt.title("降噪\n插值\n动态色度标定",fontsize=15)
    plt.xlabel("方位",  fontsize=13)
    plt.subplot(1, 4, 4)
    # data_2 = dynamicOperation(rawData, testFunction)
    # showImage(data_2)
    # plt.subplot(1, 4, 4)
    def testFunction_2(data:pd.DataFrame):
        d_0 = smoothlyData(data)
        d_1 = interpolation(d_0, tarNumb=720)
        d_2 = colorDemarcate(d_1)
        d_3 = IntensifyContrast_use(d_2,doMean=True)
        return d_3
    data_3 = dynamicOperation(rawData, testFunction_2)
    showImage(data_3)
    plt.title("降噪\n插值\n动态色度标定\n图像增强",fontsize=15)
    plt.xlabel("方位",  fontsize=13)
    plt.show()