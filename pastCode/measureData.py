import numpy as np
import pandas as pd
from tmp_interpolation import *
from simulationData import simulationDataPrehandle
import functools

_measureData = pd.read_excel("./data/measureData.xlsx",header=0).set_index("Depth")
_measureData = _measureData.iloc[:,:8]
_measureData = _measureData.loc[9616:10783]
print(_measureData)
measureData = simulationDataPrehandle(_measureData,0)
func_ = functools.partial(simulationDataPrehandle,multi=0)
measureData_dynamic = dynamicOperation(_measureData,func_,winlen=300*3)


if __name__ == '__main__':
    plt.subplot(1,3,1)
    showImage(_measureData)
    plt.subplot(1, 3, 2)
    showImage(measureData)
    plt.subplot(1, 3, 3)
    showImage(measureData_dynamic)
    plt.show()