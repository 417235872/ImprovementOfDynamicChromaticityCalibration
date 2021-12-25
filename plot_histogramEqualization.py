from MyTool.plotShow import *
from MyTool import wellData
from MyTool.dataPrehandle import *
d_raw = wellData().azigamma().iloc[160:930]
d_smoothly = gaussianFilter(d_raw)
d_histogramEqualization = histogramEqualization(d_smoothly)
d_dynamic = dynamicOperation(d_smoothly,histogramEqualization,100)

# plt.subplot(1,4,1)
# showImage(d_smoothly)
# addLabel("原始数据","角度方位，°","深度，m")
# plt.subplot(1,3,1)
# showImage(interpolation(d_smoothly))
# addLabel("高斯平滑+插值","角度方位，°","深度，m")
plt.subplot(1,2,1)
showImage(interpolation(d_histogramEqualization))
addLabel("(a)静态色度标定","角度方位，°","深度，m")
plt.subplot(1,2,2)
showImage(interpolation(d_dynamic))
addLabel("(b)动态色度标定","角度方位，°","深度，m")
plt.show()



