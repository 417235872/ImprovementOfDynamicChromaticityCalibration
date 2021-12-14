import pandas as pd
import numpy as np
import lasio
import os
from MyTool.plotShow import *
from MyTool.dataPrehandle import *


def getStimulateData(idx:int = 0):
    if idx == 0:
        dataPath = "./data/simulation/二维数据.txt"
        depthPath = "./data/simulation/depth.txt"
        cln = [x for x in range(0,361,15)]
    elif idx == 1:
        dataPath = "./data/simulation/二维数据(1).txt"
        depthPath = "./data/simulation/depth_60.txt"
        cln = [x for x in np.arange(0,361,22.5)]
    else:
        dataPath = "./data/simulation/二维数据.txt"
        depthPath = "./data/simulation/depth.txt"
        cln = [x for x in range(0, 361, 15)]
    simulationData = pd.read_csv(dataPath, sep="\s+", dtype="float64", header=None)
    simulationData.columns = cln
    depth = pd.read_csv(depthPath, sep="\s+", dtype="float64", header=None)
    simulationData["DEPTH"] = depth.values
    return simulationData.set_index("DEPTH")

def getMeasureData(idx:int=0):
    pathList = []
    for root, dirs, files in os.walk("../data/aximuthImage", topdown=False):
        for name in files:
            print()
            pathList.append(os.path.join(root, name))
    if idx >= len(pathList):
        idx = 0
    path = pathList[idx]
    data = pd.read_csv(path,sep="\s+",skiprows=8,header=None)
    l = ["DEPTH"]
    l.extend(data.columns[:-1].tolist())
    print(len(l))
    data.columns = np.array(l)
    data = data.set_index("DEPTH")
    data = data.replace(data.min(),np.nan)
    return data

def useOperator(data:pd.DataFrame,operator:np.array):
    length = operator.shape[0]
    x = data.index.values
    print(data.shape[1],data.shape[0])
    result = np.empty((length,data.shape[0]-length+1,data.shape[1]))
    values = data.values
    for i in range(length-1):
        result[i] = values[i:i-length+1]*operator[i]
    result[-1] = values[length-1:] * operator[-1]
    result = result.sum(0)
    y_1 = pd.DataFrame(result)
    idx = data.shape[0]-length+1
    y_1["DEPTH"] = x[:idx]
    return y_1.set_index("DEPTH")

if __name__ == '__main__':
    from scipy import ndimage
    def showThreePlot(data:pd.DataFrame):
        rows,columns = (2,2)
        d = data
        plt.subplot(rows,columns,1)
        showAzimuthal(d,5)
        plt.subplot(rows,columns,2)
        showImage(d)
        plt.subplot(rows,columns,3)
        diff = difference(d)
        showAzimuthal(diff, 5)
        plt.subplot(rows,columns,4)
        showImage(diff)



    for i in range(6):
        d = getMeasureData(i).iloc[50:400]
        d = gaussianFilter(d)
        showThreePlot(d)
        plt.show()
        op = np.append(np.arange(5),-1*np.arange(5))
        d_0 = useOperator(d, op)
        showThreePlot(d_0)
        plt.show()

    # for i in range(2):
    #     d = getStimulateData(i)
    #     showThreePlot(d)
    #     plt.show()
    #     d_0 = useOperator(d,np.array([1,2,3,-3,-2,-1]))
    #     showThreePlot(d_0)
    #     plt.show()