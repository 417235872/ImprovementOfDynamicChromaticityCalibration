from MyTool.plotShow import *
from MyTool import wellData
from MyTool.dataPrehandle import *
d_raw = wellData.cflog(0).iloc[30:330]
d_smoothly = gaussianFilter(d_raw)
d_interpolation = interpolation(d_smoothly)
plt.subplot(1,3,1)
showImage(d_raw)
plt.subplot(1,3,2)
showImage(d_smoothly)
plt.subplot(1,3,3)
showImage(d_interpolation)
plt.show()
plt.subplot(2,1,1)
showAzimuthal(d_raw)
plt.subplot(2,1,2)
showAzimuthal(d_smoothly)
plt.show()