from MyTool.plotShow import *
from MyTool import wellData
from MyTool.dataPrehandle import *
d_raw = histogramEqualization(wellData().azigamma().iloc[160:930])
d_smoothly = histogramEqualization(smoothlyData(d_raw))
d_gaussion = histogramEqualization(gaussianFilter(d_raw))

plt.subplot(1,3,1)
showImage(d_raw)
addLabel("原始数据","角度方位，°","深度，m")
plt.subplot(1,3,2)
showImage(d_gaussion)
addLabel("高斯滤波","角度方位，°","深度，m")
plt.subplot(1,3,3)
showImage(interpolation(d_gaussion))
addLabel("三次样条插值","角度方位，°","深度，m")
plt.show()

chnNumber = 5
plt.subplot(3,1,1)
showAzimuthal(d_raw,chnNumber)
addLabel("原始数据","深度，m","计数")
plt.subplot(3,1,2)
showAzimuthal(d_smoothly,chnNumber)
addLabel("低通滤波","深度，m","计数")
plt.subplot(3,1,3)
showAzimuthal(d_gaussion,chnNumber)
addLabel("高斯滤波","深度，m","计数")
plt.show()
