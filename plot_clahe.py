import cv2
from MyTool.plotShow import *
from MyTool import azidendf,azigamdf
from MyTool.dataPrehandle import *
d_raw = azidendf[2200:2300]

print("d_smoothly")
d_smoothly = gaussianFilter(d_raw)
print("d_AHE-quick")
d_AHE = dynamicOperation_QuicklyAutoAdjust(d_smoothly,transform_HE)
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(10,1))
d_clahe = clahe.apply(d_smoothly.values)

plt.subplot(1,5,1)
showImage(interpolation(d_smoothly))
plt.subplot(1,5,2)
showImage(interpolation(d_AHE))
plt.subplot(1,5,3)
plt.imshow(d_clahe, interpolation='none',
               aspect='auto', cmap=plt.cm.YlOrRd,
               #vmax=2.7,vmin=np.nanmin(data.values),
               )
plt.colorbar(orientation='horizontal', pad=0.2)
plt.show()