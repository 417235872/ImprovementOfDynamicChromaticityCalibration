import pandas as pd
import numpy as np
from scipy import signal
from scipy import interpolate
from scipy import ndimage
from scipy import optimize
import math
from functools import reduce
import seaborn as sns
from skimage import exposure
from tqdm import tqdm

# 高低频平滑
def smoothlyData(data:pd.DataFrame):
    '''

    :param data: dataFrame: index="DEPTH",column=angle name
    :return: dataFrame with same shape
    '''
    columns = data.columns.values
    x = data.index.values
    butter = signal.butter(10,0.1,"lowpass")
    y = {"DEPTH":x}
    for i in range(columns.shape[0]):
        y[columns[i]] = signal.filtfilt(*butter,data[columns[i]].values, method="gust")
    return pd.DataFrame(y).set_index("DEPTH")

# 高斯平滑
def gaussianFilter(data:pd.DataFrame,sigma=3):
    '''

    :param data: dataFrame: index="DEPTH",column=angle name
    :return: dataFrame with same shape
    '''
    columns = data.columns.values
    x = data.index.values
    y = {"DEPTH": x}
    for i in range(columns.shape[0]):
        y[columns[i]] = ndimage.gaussian_filter(data[columns[i]].values, sigma)
    return pd.DataFrame(y).set_index("DEPTH")
# 角度方向插值
def interpolation(data:pd.DataFrame,kind="cubic",tarNumb=720):
    '''

    :param data: dataFrame: index="DEPTH",column=angle name
    :param kind: interpolate method
    :param tarNumb: final column number
    :return: same length but tarNumb columns
    '''
    columns = data.columns.values
    idx = data.index.values
    val=np.empty((data.shape[0],data.shape[1]+1))
    val[:,:data.shape[1]] = data.values
    val[:,-1] = data.values[:,-1]
    x = np.arange(0,360.1,360/columns.shape[0])
    _x = np.arange(0,360,360/tarNumb)
    result = np.empty((data.shape[0],tarNumb))
    for i in range(idx.shape[0]):
        func = interpolate.interp1d(x,val[i],kind=kind)
        result[i] = func(_x)
    r = pd.DataFrame(result,columns=_x)
    r["DEPTH"] = idx
    return r.set_index("DEPTH")

# 直方图均衡
def histogramEqualization(data:pd.DataFrame):
    '''
    :param data:  dataFrame: index="DEPTH",column=angle name
    :return:  dataFrame with same shape
    '''
    max = data.max().max()
    min = data.min().min()
    r = (data - min) / (max - min) * 255
    return r

# 变换函数：直方图均衡
def transform_HE(data:pd.DataFrame):
    max = data.max().max()
    min = data.min().min()
    return lambda x:(x-min) / (max - min) * 255

# 动态应用函数
def dynamicOperation(data:pd.DataFrame,function: callable,winlen=300):
    '''
    对于data，取winlen长的数据传入function处理，然后移动4/5*winlen长度继续取数据，除了每个窗除了最后一个窗其余只会有4/5的数据合并到最终结果中
    :param data: dataFrame: index="DEPTH",column=angle name
    :param function: to handle data,receive only one argument -- data; return a dataFrame -- result of handling
    :param winlen: length of each block, after the first block, only 4/5 of each blocks will merge into the result
    :return:
    '''
    length = data.shape[0]
    if length <= winlen:
        return function(data)
    result = []
    index = 0
    overlapping = None
    step = int(0.8*winlen)
    for i in range(int(length/step)):
        d_handled = function(data.iloc[index:index+winlen])
        index += step
        result.append(d_handled.iloc[:step])
    if index < length:
        d_handled = function(data.iloc[index:])
        result.append(d_handled)
    def DFappend(d0:pd.DataFrame,d1:pd.DataFrame):
        return d0.append(d1)
    return reduce(DFappend,result)

# 平均值法的动态色度标定
def dynamicOperation_MeanValue(data:pd.DataFrame,function,winlen:int =300):
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
    rPD = pd.DataFrame(np.zeros(data.shape))
    rPD["DEPTH"] = data.index.values
    rPD = rPD.set_index("DEPTH")
    rPD.columns = data.columns.values
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
def dynamicOperation_GradualChange(data:pd.DataFrame,function, winlen:int = 300):
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
            if result[len(result)-1].shape[0] > step:
                rPD.iloc[step * i:] = result[len(result)-1].iloc[step:]
        else:
            l = (result[i].iloc[:overlapping].values.T * weight_overlapping +
                 result[i-1].iloc[-overlapping:].values.T * weight_overlapping[::-1]).T
            rPD.iloc[step * i:step * i + overlapping] = l
            rPD.iloc[step * i+overlapping:step*(i+1)] = result[i].iloc[overlapping:step]
    return rPD

# 自适应法的动态色度标定
def dynamicOperation_AutoAdjust(data:pd.DataFrame,function, winlen:int = 300):
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
        result:pd.DataFrame = data.copy()
        # for those blocks that are not full
        result.iloc[:winlen//2] = function(data.iloc[:winlen]).iloc[:winlen//2]
        result.iloc[length-winlen//2:] = function(data.iloc[length-winlen:]).iloc[winlen//2:]
        # for those blocks that are full
        for i in tqdm(range(winlen//2,length-winlen//2)):
            result.iloc[i] = function(data.iloc[i-winlen//2:i+winlen//2]).iloc[winlen//2]
        return result

# 自适应法的动态色度标定_快速
def dynamicOperation_QuicklyAutoAdjust(data:pd.DataFrame,transform_function, winlen:int = 300):
    '''
    与`自适应法的动态色度标定`函数类似，但是要求传入的函数返回的不是处理结果，而是直方图转换函数，这样只需要使用直方图转换函数处理目标深度点数据即可
    :param data: dataFrame: index="DEPTH",column=angle name
    :param function: to handle data,receive only one argument -- data; return a callable --Histogram conversion function
    :param winlen: length of each block
    :return:
    '''
    length = data.shape[0]
    if length <= winlen:
        return transform_function(data)
    else:
        result:pd.DataFrame = data.copy()
        # for those blocks that are not full
        result.iloc[:winlen//2] = transform_function(data.iloc[:winlen])(data.iloc[:winlen//2])
        result.iloc[length-winlen//2:] = transform_function(data.iloc[length-winlen:])(data.iloc[length-winlen//2:])
        # for those blocks that are full
        for i in tqdm(range(winlen//2,length-winlen//2)):
            result.iloc[i] = transform_function(data.iloc[i-winlen//2:i+winlen//2])(data.iloc[i])
        return result





# # 限制直方图均衡——直方图转换
# def clahe_histTransform(data:pd.DataFrame, maxLimit=0.01):
#     HE = histogramEqualization(data)
#     h,x = np.histogram(HE,bins=np.arange(255))
#     h_clahe = np.empty(h.shape)
#     capacity = h.sum()
#     outsideIndex = h > (maxLimit * capacity)
#     if outsideIndex.sum() == 0:
#         print(outsideIndex.sum())
#         return HE
#     else:
#         # 建立clahe直方图
#         outsideValues = (h[outsideIndex] - (maxLimit * capacity)).sum()
#         averageIncrease = outsideValues / (~outsideIndex).sum()
#         increaseIndex = h<((maxLimit * capacity)-averageIncrease)
#         h_clahe[~increaseIndex] = maxLimit * capacity
#         h_clahe[increaseIndex] = h[increaseIndex] + averageIncrease
#         outsideValues = h.sum() - h_clahe.sum()
#         while (outsideValues > 0.1):
#             averageIncrease = outsideValues / increaseIndex.sum()
#             increaseIndex = h_clahe < ((maxLimit * capacity) - averageIncrease)
#             h_clahe[increaseIndex] = h_clahe[increaseIndex] + averageIncrease
#             outsideValues = h.sum() - h_clahe.sum()
#         # 直方图映射函数
#         hist_CDF = h.cumsum()
#         clahe_CDF = h_clahe.cumsum()
#         import matplotlib.pyplot as plt
#         plt.subplot(2,1,1)
#         plt.plot(x[:-1],hist_CDF)
#         plt.grid()
#         plt.subplot(2, 2, 1)
#         plt.plot(x[:-1], clahe_CDF)
#         plt.grid()
#         plt.show()

