from MyTool.plotShow import *
from MyTool import wellData
from MyTool.dataPrehandle import *
d_raw = wellData().azigamma().iloc[160:930]
d_smoothly = gaussianFilter(d_raw)
d_dynamic = dynamicOperation(d_smoothly,histogramEqualization)
d_meanValue = dynamicOperation_MeanValue(d_smoothly,histogramEqualization)
d_gradualChange = dynamicOperation_GradualChange(d_smoothly,histogramEqualization)

# plt.subplot(1,4,1)
# showImage(interpolation(d_smoothly))
# addLabel("直方图均衡","角度方位，°","深度，m")
plt.subplot(1,3,1)
showImage(interpolation(d_dynamic))
addLabel("动态直方图均衡","角度方位，°","深度，m")
plt.subplot(1,3,2)
showImage(interpolation(d_meanValue))
addLabel("平均值法","角度方位，°","深度，m")
plt.subplot(1,3,3)
showImage(interpolation(d_gradualChange))
addLabel("渐变过渡法","角度方位，°","深度，m")
plt.show()