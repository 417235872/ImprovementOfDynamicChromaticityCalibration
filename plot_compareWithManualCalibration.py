from MyTool.plotShow import *
from MyTool import wellData
from MyTool.dataPrehandle import *
d_raw = wellData().azigamma().iloc[160:930]
print("d_smoothly")
d_smoothly = gaussianFilter(d_raw)
print("d_manual")
d_manual = histogramEqualization(d_smoothly.iloc[120:300])
print("d_dynamic")
d_dynamic = dynamicOperation(d_smoothly,histogramEqualization,100)
print("d_meanValue")
d_meanValue = dynamicOperation_MeanValue(d_smoothly,histogramEqualization,100)
print("d_gradualChange")
d_gradualChange = dynamicOperation_GradualChange(d_smoothly,histogramEqualization,100)
print("d_AHE-quick")
d_AHE = dynamicOperation_QuicklyAutoAdjust(d_smoothly,transform_HE,100)


plt.subplot(1,5,1)
showImage(interpolation(d_dynamic.iloc[200:300]))
addLabel("(a)动态色度标定","角度方位，°","深度，m")
plt.subplot(1,5,2)
showImage(interpolation(d_smoothly.iloc[200:300]))
addLabel("(b)静态色度标定","角度方位，°","深度，m")

plt.subplot(1,5,3)
showImage(interpolation(d_manual.iloc[80:]))
addLabel("(c)手动标定色度","角度方位，°","深度，m")
# plt.subplot(1,4,3)
# showImage(interpolation(d_meanValue.iloc[180:300]))
# addLabel("平均值法","角度方位，°","深度，m")
plt.subplot(1,5,4)
showImage(interpolation(d_gradualChange.iloc[200:300]))
addLabel("(d)渐变过渡法","角度方位，°","深度，m")
plt.subplot(1,5,5)
showImage(interpolation(d_AHE.iloc[200:300]))
addLabel("(e)限制步长法","角度方位，°","深度，m")
plt.show()