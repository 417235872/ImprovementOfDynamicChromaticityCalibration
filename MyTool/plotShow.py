import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def addLabel(title:str,xlabel:str,ylabel:str, size=20):
    plt.xticks(fontsize=size)
    plt.yticks(fontsize=size)
    plt.title(title,fontsize=size+10)
    plt.xlabel(xlabel,fontsize=size+5)
    plt.ylabel(ylabel,fontsize=size+5)


def showImage(data:pd.DataFrame,**kwargs):
    miny = data.index.min()
    maxy = data.index.max()
    plt.imshow(data, interpolation='none',
               aspect='auto', cmap=plt.cm.YlOrRd,
               **kwargs,
               vmax=0,vmin=255,
               extent=[0, 360, maxy, miny])
    plt.colorbar(orientation='horizontal', pad=0.1)

def showAzimuthal(data:pd.DataFrame,showNumber=3):
    columns = data.columns.values
    x = data.index.values
    for i in range(showNumber):
        plt.plot(x,data[columns[i]],label="chn:{}".format(i))
    plt.grid()
    plt.legend(fontsize =15)

def histOfGray(data:pd.DataFrame):
    h,x = np.histogram(data.values,bins=np.arange(255))
    plt.plot(x[:-1],h)
    plt.grid()
    plt.xlabel("gray level")
    plt.ylabel("frequency")
    plt.title("hist of gray")