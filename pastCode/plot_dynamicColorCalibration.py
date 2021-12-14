from tmp_interpolation import *
import math
def dynamicOperation(data:pd.DataFrame,function: callable,winlen=300):
    length = data.shape[0]
    result = []
    index = 0
    step = int(winlen*0.8)
    rPD = pd.DataFrame(np.zeros(data.shape))
    rPD["DEPTH"] = data.index.values
    rPD = rPD.set_index("DEPTH")
    rPD.columns = data.columns.values
    for i in range(math.ceil((length - winlen) / step) + 1):
        d = function(data.iloc[step * i:step * i + winlen])
        result.append(d)
    for i in range(len(result) + 1):
        if i == len(result):
            rPD.iloc[step * i:] = result[len(result) - 1].iloc[step:]
        else:
            rPD.iloc[step * i:step * (i + 1)] = result[i].iloc[:step]
    return rPD


def dynamicDemarcateFilter(data:pd.DataFrame,function,winlen:int =300):
    length = data.shape[0]
    result = []
    index = 0
    overlapping = None
    step = int(0.2 * winlen)
    rPD = pd.DataFrame(np.zeros(data.shape))
    rPD["DEPTH"] = data.index.values
    rPD = rPD.set_index("DEPTH")
    rPD.columns = data.columns.values
    for i in range(math.ceil((length-winlen)/step)+1):
        d = function(data.iloc[step*i:step*i+winlen])
        result.append(d)
    for i in range(len(result)+4):
        if i <= 3:
            for j in range(i+1):
                rPD.iloc[step * i:step * i + step] += result[j].iloc[step * (i - j):step * (i - j) + step]
            rPD.iloc[step*i:step*i+step] /= i+1
        elif i >= len(result):
            for j in range(len(result)+4-i):
                if step * (1-len(result)+i+j) + step <= result[len(result)-j-1].shape[0]:
                    rPD.iloc[step * i:step * i + step] += result[len(result)-j-1].iloc[step * (1-len(result)+i+j):step * (1-len(result)+i+j) + step]
                else:
                    rPD.iloc[step * i:step * i + step] += result[len(result) - j-1].iloc[step * (1 - len(result) + i + j):]
            rPD.iloc[step*i:step*i+step] /= len(result)+4-i
        else:
            for j in range(5):
                rPD.iloc[step * i:step * i + step] += result[i-j].iloc[step * (j):step * (j) + step]
            rPD.iloc[step*i:step*i+step] /= 5
    return rPD

def dynamicDemarcateSmoothly(data:pd.DataFrame,function, winlen:int = 300):
    length = data.shape[0]
    result = []
    index = 0
    overlapping = int(winlen * 0.4)
    step =  winlen - overlapping
    rPD = pd.DataFrame(np.zeros(data.shape))
    rPD["DEPTH"] = data.index.values
    rPD = rPD.set_index("DEPTH")
    rPD.columns = data.columns.values
    weight_overlapping = np.linspace(0,1,overlapping)
    for i in range(math.ceil((length - winlen) / step) + 1):
        d = function(data.iloc[step * i:step * i + winlen])
        result.append(d)
    for i in range(len(result)+1):
        if i == 0:
            rPD.iloc[:step] = result[0].iloc[:step]
        elif i == len(result):
            rPD.iloc[step * i:] = result[len(result)-1].iloc[step:]
        else:
            l = (result[i].iloc[:overlapping].values.T * weight_overlapping +
                 result[i-1].iloc[-overlapping:].values.T * weight_overlapping[::-1]).T
            rPD.iloc[step * i:step * i + overlapping] = l
            rPD.iloc[step * i+overlapping:step*(i+1)] = result[i].iloc[overlapping:step]
    return rPD

if __name__ == '__main__':
    plt.figure(figsize=(7, 15))
    rawData = azidendf[2300:2400]
    d_0 = testFunction(rawData,2)
    plt.subplot(1,4,1)
    showImage(d_0)
    plt.title("静态色度标定",fontsize = 15)
    plt.subplot(1, 4, 2)
    d_1 = dynamicOperation(d_0,colorDemarcate)
    showImage(d_1)
    plt.title("动态色度标定",fontsize = 15)
    plt.subplot(1, 4, 3)
    d_2 = dynamicDemarcateFilter(d_0, colorDemarcate)
    showImage(d_2)
    plt.title("动态色度标定_重叠平均",fontsize = 15)
    plt.subplot(1,4,4)
    d_3 = dynamicDemarcateSmoothly(d_0,colorDemarcate)
    showImage(d_3)
    plt.title("动态色度标定_渐变过渡",fontsize = 15)
    plt.show()
    # plt.subplot(1, 4, 1)
    # showAzimuthal(d_0)
    # plt.subplot(1, 4, 2)
    # showAzimuthal(d_1)
    # plt.subplot(1, 4, 3)
    # showAzimuthal(d_2)
    # plt.subplot(1, 4, 4)
    # showAzimuthal(d_3)
    # plt.show()