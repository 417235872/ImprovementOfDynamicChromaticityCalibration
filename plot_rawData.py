from MyTool.plotShow import *
from MyTool import wellData

data = wellData().cflog(0)
winlength = 900
for i in range(data.shape[0]//winlength):
    d = data.iloc[winlength*i:winlength*(i+1)]
    showImage(d)
    plt.title("{}-{}".format(winlength*i,winlength*(i+1)))
    plt.show()
    # showAzimuthal(d)
    # plt.show()



