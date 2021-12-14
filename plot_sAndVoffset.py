from MyTool.plotShow import *
import matplotlib.pyplot as plt
from MyTool import wellData
from MyTool.dataPrehandle import *

def showArgument(data:pd.DataFrame,index = 0):
    x = data.index.values
    if index == 0:
        plt.plot(x,data["S"],label="$S$")
    else:
        plt.plot(x,data["V_offset"],label="$V_{offset}$",color = "g")
    plt.grid()
    plt.legend(fontsize =15)

def getArgumentOfHE(data:pd.DataFrame):
    s = np.empty(data.shape[0])
    l = data.max().max() - data.min().min()
    s[:] = 255/l
    V_offset = np.empty(data.shape[0])
    V_offset[:] = - data.min().min() * s
    result = pd.DataFrame({"DEPTH" : data.index.values,"S" : s,"V_offset" : V_offset}).set_index("DEPTH")
    return result

# 平均值法的动态色度标定
def _dynamicOperation_MeanValue(data:pd.DataFrame,function,winlen:int =300):
    '''
    对于data，取winlen长的数据传入function处理，然后移动1/5*winlen长度继续取数据传入function处理，对于重叠部分取平均值
    :param data: dataFrame: index="DEPTH",column=angle name
    :param function: to handle data,receive only one argument -- data; return a dataFrame -- result of handling
    :param winlen: length of each block
    :return:
    '''
    length = data.shape[0]
    if length <= winlen:
        return function(data)
    result = []
    index = 0
    overlapping = None
    step = int(0.2 * winlen)
    s = np.zeros(data.shape[0])
    V_offset = np.zeros(data.shape[0])
    rPD = pd.DataFrame({"DEPTH": data.index.values, "S": s, "V_offset": V_offset}).set_index("DEPTH")
    for i in range(math.ceil((length-winlen)/step)+1):
        d = function(data.iloc[step*i:step*i+winlen])
        result.append(d)
    if len(result) >= 5:
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
    else:
        for i in range(len(result)+4):
            if i <= len(result)-1:
                for j in range(i+1):
                    rPD.iloc[step * i:step * i + step] += result[j].iloc[step * (i - j):step * (i - j) + step]
                rPD.iloc[step*i:step*i+step] /= i+1
            elif i >= 5:
                for j in range(len(result)+4-i):
                    if step * (1-len(result)+i+j) + step <= result[len(result)-j-1].shape[0]:
                        rPD.iloc[step * i:step * i + step] += result[len(result)-j-1].iloc[step * (1-len(result)+i+j):step * (1-len(result)+i+j) + step]
                    else:
                        rPD.iloc[step * i:step * i + step] += result[len(result) - j-1].iloc[step * (1 - len(result) + i + j):]
                rPD.iloc[step*i:step*i+step] /= len(result)+4-i
            else:
                for j in range(len(result)):
                    rPD.iloc[step * i:step * i + step] += result[j].iloc[step * (i-j):step * (i-j) + step]
                rPD.iloc[step * i:step * i + step] /= len(result)
    return rPD

# 渐变平滑法的动态色度标定
def _dynamicOperation_GradualChange(data:pd.DataFrame,function, winlen:int = 300):
    '''
    对于data，取winlen长的数据传入function处理，然后移动4/5*winlen长度继续取数据，对于重叠部分使用渐变过渡法
    :param data: dataFrame: index="DEPTH",column=angle name
    :param function: to handle data,receive only one argument -- data; return a dataFrame -- result of handling
    :param winlen: length of each block
    :return:
    '''
    length = data.shape[0]
    result = []
    index = 0
    overlapping = int(winlen * 0.4)
    step =  winlen - overlapping
    s = np.zeros(data.shape[0])
    V_offset = np.zeros(data.shape[0])
    rPD = pd.DataFrame({"DEPTH": data.index.values, "S": s, "V_offset": V_offset}).set_index("DEPTH")
    weight_overlapping = np.linspace(0,1,overlapping)
    for i in range(math.ceil((length - winlen) / step) + 1):
        d = function(data.iloc[step * i:step * i + winlen])
        result.append(d)
    for i in range(len(result)+1):
        if i == 0:
            rPD.iloc[:step] = result[0].iloc[:step]
        elif i == len(result):
            if result[len(result)-1].shape[0] > step:
                rPD.iloc[step * i:] = result[len(result)-1].iloc[step:]
        else:
            l = (result[i].iloc[:overlapping].values.T * weight_overlapping +
                 result[i-1].iloc[-overlapping:].values.T * weight_overlapping[::-1]).T
            rPD.iloc[step * i:step * i + overlapping] = l
            rPD.iloc[step * i+overlapping:step*(i+1)] = result[i].iloc[overlapping:step]
    return rPD

# 自适应法的动态色度标定
def _dynamicOperation_AutoAdjust(data:pd.DataFrame,function, winlen:int = 300):
    '''
    对于每一个深度点（一行数据），以目标深度点为中心总长winlen的数据块传入function处理，然后只取对应深度点的数据填入最终结果
    整个井段开始部分和结尾winlen/2长度的部分填入直接用function处理该数据块的结果
    :param data: dataFrame: index="DEPTH",column=angle name
    :param function: to handle data,receive only one argument -- data ; return a dataFrame -- result of handling
    :param winlen: length of each block
    :return:
    '''
    length = data.shape[0]
    if length <= winlen:
        return function(data)
    else:
        s = np.zeros(data.shape[0])
        V_offset = np.zeros(data.shape[0])
        result = pd.DataFrame({"DEPTH" : data.index.values,"S" : s,"V_offset" : V_offset}).set_index("DEPTH")
        # for those blocks that are not full
        result.iloc[:winlen // 2] = function(data.iloc[:winlen]).iloc[:winlen // 2]
        result.iloc[length - winlen // 2:] = function(data.iloc[length - winlen:]).iloc[winlen // 2:]
        # for those blocks that are full
        for i in tqdm(range(winlen // 2, length - winlen // 2)):
            result.iloc[i] = function(data.iloc[i - winlen // 2:i + winlen // 2]).iloc[winlen // 2]
        return result

d_raw = wellData().azigamma().iloc[160:930]
d_smoothly = gaussianFilter(d_raw)
a_raw = dynamicOperation(d_smoothly, getArgumentOfHE,100)
a_meanValue = _dynamicOperation_MeanValue(d_smoothly,getArgumentOfHE,100)
a_GrandualChange = _dynamicOperation_GradualChange(d_smoothly,getArgumentOfHE,100)
a_AutoAdjust = _dynamicOperation_AutoAdjust(d_smoothly,getArgumentOfHE,100)



# for i in range(2):
#     plt.subplot(4,2,1+i)
#     showArgument(a_raw,i)
#     plt.subplot(4,2,3+i)
#     showArgument(a_meanValue,i)
#     plt.subplot(4,2,5+i)
#     showArgument(a_GrandualChange,i)
#     plt.subplot(4,2,7+i)
#     showArgument(a_AutoAdjust,i)
# plt.show()
def plotMeanValues_arg():
    plt.subplot(2,2,1)
    showArgument(a_raw,0)
    addLabel("动态色度标定刻度系数$S$","深度,$m$","刻度系数")
    plt.subplot(2,2,2)
    showArgument(a_raw,1)
    addLabel("动态色度标定偏移量$V_{offset}$","深度,$m$","偏移量")
    plt.subplot(2,2,3)
    showArgument(a_meanValue,0)
    addLabel("平均值法等效刻度系数$S$","深度,$m$","刻度系数")
    plt.subplot(2,2,4)
    showArgument(a_meanValue,1)
    addLabel("平均值法等效偏移量$V_{offset}$","深度,$m$","偏移量")
    plt.show()

def plotGradualChange_arg():
    plt.subplot(2,2,1)
    showArgument(a_raw,0)
    addLabel("动态色度标定刻度系数$S$","深度,$m$","刻度系数")
    plt.subplot(2,2,2)
    showArgument(a_raw,1)
    addLabel("动态色度标定偏移量$V_{offset}$","深度,$m$","偏移量")
    plt.subplot(2,2,3)
    showArgument(a_GrandualChange,0)
    addLabel("渐变过渡法等效刻度系数$S$","深度,$m$","刻度系数")
    plt.subplot(2,2,4)
    showArgument(a_GrandualChange,1)
    addLabel("渐变过渡法等效偏移量$V_{offset}$","深度,$m$","偏移量")
    plt.show()

def plotAutoAdjust_arg():
    plt.subplot(2,2,1)
    showArgument(a_raw,0)
    addLabel("动态色度标定刻度系数$S$","深度,$m$","刻度系数")
    plt.subplot(2,2,2)
    showArgument(a_raw,1)
    addLabel("动态色度标定偏移量$V_{offset}$","深度,$m$","偏移量")
    plt.subplot(2,2,3)
    showArgument(a_AutoAdjust,0)
    addLabel("自适应动态色度标定法等效刻度系数$S$","深度,$m$","刻度系数")
    plt.subplot(2,2,4)
    showArgument(a_AutoAdjust,1)
    addLabel("自适应动态色度标定法等效偏移量$V_{offset}$","深度,$m$","偏移量")
    plt.show()

def plotArg(index:int = 0):
    data = [a_raw,a_meanValue,a_GrandualChange,a_AutoAdjust]
    name = ["动态色度标定","平均值法等效","渐变过渡法等效","自适应动态色度标定法等效"]
    plt.subplot(1, 2, 1)
    showArgument(data[index], 0)
    addLabel(name[index]+"标定刻度系数$S$", "深度,$m$", "刻度系数")
    plt.subplot(1, 2, 2)
    showArgument(data[index], 1)
    addLabel(name[index]+"偏移量$V_{offset}$", "深度,$m$", "偏移量")
    plt.show()

if __name__ == '__main__':
    for i in range(4):
        plotArg(i)