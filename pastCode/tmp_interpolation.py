import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lasio
from scipy import signal
from scipy import interpolate
from scipy import optimize
from functools import reduce
import seaborn as sns
from skimage import exposure
plt.rcParams['font.sans-serif'] = ['SimHei']
# Matplotlib中设置字体-黑体，解决Matplotlib中文乱码问题
# plt.rcParams['axes.unicode_minus'] = False
# # 解决Matplotlib坐标轴负号'-'显示为方块的问题
# sns.set(font='SimHei')
# Seaborn中设置字体-黑体，解决Seaborn中文乱码问题


las = lasio.read('../data/P11-A-02_Composite_MEM_Image_NF.las')
df = las.df()

azidendf = df[['ABDC1M', 'ABDC2M', 'ABDC3M', 'ABDC4M', 'ABDC5M',
               'ABDC6M', 'ABDC7M', 'ABDC8M', 'ABDC9M', 'ABDC10M',
               'ABDC11M', 'ABDC12M', 'ABDC13M', 'ABDC14M', 'ABDC15M',
               'ABDC16M']]

azigamdf = df[['GRAS0M', 'GRAS1M', 'GRAS2M', 'GRAS3M', 'GRAS4M',
               'GRAS5M', 'GRAS6M', 'GRAS7M']]

def showImage(data:pd.DataFrame,**kwargs):
    miny = data.index.min()
    maxy = data.index.max()
    plt.imshow(data, interpolation='none',
               aspect='auto', cmap=plt.cm.YlOrRd,
               **kwargs,
               #vmax=2.7,vmin=np.nanmin(data.values),
               extent=[0, 360, maxy, miny])

    #plt.ylim(2130, 2100)
    cb = plt.colorbar(orientation='horizontal', pad=0.05)
    cb.ax.tick_params(labelsize=14)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

def showAzimuthal(data:pd.DataFrame,showNumber=3):
    columns = data.columns.values
    x = data.index.values
    for i in range(showNumber):
        plt.plot(x,data[columns[i]],label="{:.2f}°方位".format(22.5*i))
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.grid()
    plt.legend(fontsize=25)


def smoothlyData(data:pd.DataFrame):
    columns = data.columns.values
    x = data.index.values
    butter = signal.butter(10,0.1,"lowpass")
    y = {"DEPTH":x}
    for i in range(columns.shape[0]):
        y[columns[i]] = signal.filtfilt(*butter,data[columns[i]].values, method="gust")
    return pd.DataFrame(y).set_index("DEPTH")

def interpolation(data:pd.DataFrame,kind="cubic",tarNumb=720):
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

def colorDemarcate(data:pd.DataFrame,Cmax=255,Cmin=0):
    columns = data.columns.values
    idx = data.index.values
    val = data.values
    Vmax=val.max()
    Vmin=val.min()
    Scale=(Cmax-Cmin)/(Vmax-Vmin)
    #Voffset=Cmin-Vmin
    Vpixel=(data-Vmin)*Scale+Cmin
    return Vpixel

def ImageIntensification(data:pd.DataFrame):
    '''
    TODO:1.get the histogram of values,to analyze the distribution
        2.according to the distribution, check whether it should be intensified
        3.according to the distribution, choose which function should be used
    :param data:
    :return:
    '''
    pass


def dynamicOperation(data:pd.DataFrame,function: callable,winlen=300):
    length = data.shape[0]
    result = []
    index = 0
    overlapping = None
    step = int(0.8*winlen)
    for i in range(int(length/step)):
        d_handled = function(data.iloc[index:index+winlen])
        index += step
        if overlapping is None:
            result.append(d_handled)
        else:
            result.append(d_handled[winlen-step:])
            overlapping = d_handled[step-winlen:]
    if index < length:
        d_handled = function(data.iloc[index:])
        if overlapping is None:
            result.append(d_handled)
        else:
            result.append(d_handled[winlen - step:])
            overlapping = d_handled[step - winlen:]
    def DFappend(d0:pd.DataFrame,d1:pd.DataFrame):
        return d0.append(d1)
    return reduce(DFappend,result)

def testFunction(data:pd.DataFrame,dealStep=4):
    if dealStep >= 1:
        d_0 = smoothlyData(data)
    else:
        d_0 = data
    if dealStep >= 2:
        d_1 = interpolation(d_0, tarNumb=720)
    else:
        d_1 = d_0
    if dealStep >= 3:
        d_2 = colorDemarcate(d_1)
    else:
        d_2 = d_1
    if dealStep >= 4:
        d_3 = IntensifyContrast_use(d_2)
    else:
        d_3 = d_2
    return d_3

def histOfGray(data:pd.DataFrame):
    h,x = np.histogram(data.values,bins=np.arange(255))
    plt.plot(x[:-1],h)
    plt.grid()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel("灰度值",fontsize=15)
    plt.ylabel("频率",fontsize=15)


def IntensifyContrast(data:pd.DataFrame,coeff:np.array):
    r = np.zeros(data.shape)
    # for i in range(coeff.shape[0]):
    #     r += coeff[i] * data ** i
    a,b = coeff
    r = 1/(np.exp(a*(data+b))+1)
    r[r > 1] = 1
    r[r < 0] = 0
    return r*255

def tans(coeff:np.array,*params):
    data,mean=params
    r = IntensifyContrast(data,coeff)
    D_hist,bins = np.histogram(r,bins=np.arange(256))
    s = np.abs(mean - D_hist).sum()
    return s

def optim_tans(data:pd.DataFrame):
    hist,_ = np.histogram(data,bins=np.arange(256))
    rranges = (slice(-10,10,0.1), slice(-10,10,0.1))
    rebrute = optimize.brute(tans,rranges,args=(data/255,hist.mean()),full_output=True,finish=optimize.fmin)
    print("global min args",rebrute[0])
    print("global min values",rebrute[1])

def IntensifyContrast_use(data:pd.DataFrame,coeff=np.array([-10,-0.5]),doMean=True,kind="sigmod"):
    if kind == "sigmod":
        d =IntensifyContrast(data/255,coeff)
    elif kind == "sigmod_mean":
        d = IntensifyContrast(data / 255, coeff)
        doMean = True
    elif kind == "gamma_mean":
        d = exposure.adjust_gamma(data.values, 1.2)
        doMean = True
    elif kind == "gamma":
        d = exposure.adjust_gamma(data.values,1.1)
    elif kind == "log":
        d = exposure.adjust_log(data.values,1.2)
    elif kind == "double":
        d_0 = IntensifyContrast(data/255,coeff)
        d_0[d_0 > 255] = 255
        d_0[d_0 < 0] = 0
        d_1 = exposure.adjust_log(data.values,1.2)
        d_1[d_1 > 255] = 255
        d_1[d_1 < 0] = 0
        d = (d_0 + d_1)
    d[d>255] = 255
    d[d<0]  = 0
    import copy
    d_ = copy.copy(data)
    if doMean:
        d_.iloc[:] = (d+data.values)/2
    else:
        d_.iloc[:] = d
    return d_

if __name__ == '__main__':
    # plt.figure(figsize=(7, 15))
    # plt.subplot(1,2,1)
    # showImage(azigamdf)
    # plt.title("gamma")
    # plt.subplot(1, 2, 2)
    # showImage(azidendf)
    # plt.title("density")
    # plt.show()
    #
    #
    #
    # plt.figure(figsize=(7, 15))
    # rawData=azigamdf[2200:2670]
    # plt.subplot(1, 4, 1)
    # showImage(rawData)
    # plt.title("raw data")
    # plt.subplot(1,4,2)
    # showImage(testFunction(rawData))
    # plt.title("smoothly,\ninterpolate\nstatic color demarcate")
    # plt.subplot(1,4,3)
    # def fd(data:pd.DataFrame):
    #     return testFunction(data,dealStep=3)
    # data_after = dynamicOperation(rawData,fd)
    # showImage(data_after)
    # plt.title("smoothly,\ninterpolate\ndynamic color demarcate")
    # plt.subplot(1, 4, 4)
    # # data_2 = dynamicOperation(rawData, testFunction)
    # # showImage(data_2)
    # # plt.subplot(1, 4, 4)
    # def testFunction_2(data:pd.DataFrame):
    #     d_0 = smoothlyData(data)
    #     d_1 = interpolation(d_0, tarNumb=720)
    #     d_2 = colorDemarcate(d_1)
    #     d_3 = IntensifyContrast_use(d_2,doMean=True)
    #     return d_3
    # data_3 = dynamicOperation(rawData, testFunction_2)
    # showImage(data_3)
    # plt.title("smoothly,\ninterpolate\ndynamic color demarcate\nimage intensification")
    # plt.show()
    # #
    # kinds=["linear","quadratic","cubic"]
    # rawData = azidendf[2100:2130]
    # print(rawData.shape)
    # d_smoothed=smoothlyData(rawData)
    # d_interpolation=interpolation(d_smoothed,tarNumb=720)
    # print(d_smoothed)
    # plt.subplot(1,4,1)
    # showAzimuthal(rawData)
    # plt.title("raw data")
    # plt.subplot(1, 4, 2)
    # showAzimuthal(d_smoothed)
    # plt.title("smoothly")
    # plt.subplot(1, 3, 3)
    # showAzimuthal(rawData-d_smoothed)
    # plt.title("noise data")
    # plt.show()
    # plt.figure(figsize=(7, 15))
    # plt.subplot(1, 2, 1)
    # showImage(rawData,vmax=np.max(d_smoothed.values))
    # plt.title("raw data")
    # plt.subplot(1, 4, 1)
    # showImage(d_smoothed)
    # plt.title("before interpolated")
    # # plt.subplot(1, 4, 3)
    # for i in range(3):
    #     plt.subplot(1,4,2+i)
    #     data_interpolation=interpolation(d_smoothed,kind=kinds[i],tarNumb=720)
    #     showImage(data_interpolation)
    #     plt.title("{}".format(kinds[i]))

    # plt.subplot(2,3,6)
    # data_all = testFunction(rawData)
    # showImage(data_all)
    # plt.title("add color demarcate \nand image intensification")
    # plt.show()
    # # optim_tans(data_all)
    # # ImageIntensification(data_all)
    #


    rawData=azidendf[2500:2530]
    plt.subplot(2,2,1)
    data_all = testFunction(rawData,dealStep=3)
    # data_b = IntensifyContrast_f(data_all)
    data_b = data_all
    showImage(data_b)
    plt.title("增强前")
    plt.subplot(2,2,2)

    data_IC = IntensifyContrast_use(data_all,doMean=False)
    showImage(data_IC)
    plt.title("增强后")
    # plt.show()

    plt.subplot(2, 2, 3)

    histOfGray(data_b)
    plt.subplot(2,2, 4)
    # data_IC = IntensifyContrast_use(data_all)
    histOfGray(data_IC)
    plt.show()