from tmp_interpolation import *


if __name__ == '__main__':
    kinds = ["sigmod","sigmod_mean","log","gamma","double","gamma_mean"]
    for i in range(25):
        rawData = azidendf[2200+30*i:2230+30*i]
        plt.subplot(2, 8, 1)
        data_all = testFunction(rawData, dealStep=3)
        showImage(data_all)
        plt.title("增强前")
        plt.subplot(2,8,9)
        histOfGray(data_all)
        for j in range(6):
            plt.subplot(2, 8, 2+j)
            data_IC = IntensifyContrast_use(data_all, doMean=False,kind=kinds[j])
            showImage(data_IC)
            plt.title("增强后-{}".format(kinds[j]))
            plt.subplot(2, 8, 10+j)
            # data_IC = IntensifyContrast_use(data_all)
            histOfGray(data_IC)
        plt.show()

# 2200-sigmod_mean