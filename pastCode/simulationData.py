import numpy as np
import pandas as pd
from tmp_interpolation import *
# from pyqtgraph.examples import run
# run()
def interpolation_depth(data:pd.DataFrame,kind="linear",multi = 10):
    columns = data.columns
    d_0 = {}
    _x = data.index.values
    func = interpolate.interp1d(np.arange(_x.shape[0]), _x, kind=kind)
    _l = np.arange(_x.shape[0])
    l = np.arange(_x.shape[0]-1+1/multi,step=1/multi)
    if l[-1] > _l[-1]:
        x = func(l[:-1])
    else:
        x = func(l)

    d_0["depth"] = x
    for i in columns:
        func = interpolate.interp1d(_x, data.loc[:,i].values, kind=kind)
        d_0[i] = func(x)
    r = pd.DataFrame(d_0).set_index("depth")
    return r

def simulationDataPrehandle(data:pd.DataFrame,multi = 30,tarNumb=720):
    if multi > 1:
        d_0 = interpolation_depth(data,multi = multi)
    else:
        d_0 = data
    d_1 = interpolation(d_0,tarNumb=tarNumb)
    d_2 = colorDemarcate(d_1)
    return d_2


_simulationData_30 = pd.read_csv("../data/simulation/二维数据.txt", sep="\s+", dtype="float64", header=None)
_simulationData_30.columns = [x for x in range(0,361,15)] #"angle{:0>3d}".format(x)
depth_30 = pd.read_csv("../data/simulation/depth.txt", sep="\s+", dtype="float64", header=None)
_simulationData_30["depth"] = depth_30.values
_simulationData_30 = _simulationData_30.set_index("depth")
simulationData_30 = simulationDataPrehandle(_simulationData_30)


_simulationData_60 = pd.read_csv("../data/simulation/二维数据(1).txt", sep="\s+", dtype="float64", header=None)
_simulationData_60.columns = [x for x in np.arange(0,361,22.5)]
depth_60 = pd.read_csv("../data/simulation/depth_60.txt", sep="\s+", dtype="float64", header=None)
_simulationData_60["depth"] = depth_60.values
_simulationData_60 = _simulationData_60.set_index("depth")
simulationData_60 = simulationDataPrehandle(_simulationData_60)

if __name__ == '__main__':
    plt.subplot(1,2,1)
    showImage(colorDemarcate(_simulationData_30))
    plt.title("raw Data:30°")
    plt.subplot(1,2,2)
    showImage(simulationData_30)
    plt.title("handled Data:30°")
    plt.show()

    plt.subplot(1,2,1)
    showImage(colorDemarcate(_simulationData_60))
    plt.title("raw Data:60°")
    plt.subplot(1,2,2)
    showImage(simulationData_60)
    plt.title("handled Data:60°")
    plt.show()

    plt.subplot(1, 2, 1)
    showAzimuthal(_simulationData_30,16)
    plt.title("raw Data:30°")
    plt.subplot(1, 2, 2)
    showAzimuthal(simulationData_60,16)
    plt.title("handled Data:60°")
    plt.show()

