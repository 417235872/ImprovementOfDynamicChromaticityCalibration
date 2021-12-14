from MyTool.plotShow import *
from MyTool import wellData
from MyTool.dataPrehandle import *
import time
d_raw = wellData().azigamma().iloc[160:930]
print("d_smoothly")
t0 = time.time()
d_smoothly = gaussianFilter(d_raw)
print(time.time()-t0)
print("d_AHE")
t1 = time.time()
d_AHE = dynamicOperation_AutoAdjust(d_smoothly,histogramEqualization)
print(time.time()-t1)
print("d_AHE-quick")
t1 = time.time()
d_AHE_q = dynamicOperation_QuicklyAutoAdjust(d_smoothly,transform_HE)
print(time.time()-t1)

plt.subplot(1,2,1)
showImage(interpolation(d_AHE))
plt.subplot(1,2,2)
showImage(interpolation(d_AHE_q))
plt.show()