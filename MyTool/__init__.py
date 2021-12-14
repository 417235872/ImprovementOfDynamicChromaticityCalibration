import lasio
import pandas as pd
import numpy as np
class wellData():
    @staticmethod
    def azidendf(index=0):
        if index == 0:
            las = lasio.read('./data/P11-A-02_Composite_MEM_Image_NF.las')
        else:
            las = lasio.read('./data/P11-A-01_Composite_MEM_Image_NF.las')
        df = las.df()
        return df[['ABDC1M', 'ABDC2M', 'ABDC3M', 'ABDC4M', 'ABDC5M',
                       'ABDC6M', 'ABDC7M', 'ABDC8M', 'ABDC9M', 'ABDC10M',
                       'ABDC11M', 'ABDC12M', 'ABDC13M', 'ABDC14M', 'ABDC15M',
                       'ABDC16M']]

    @staticmethod
    def azigamma(index=0):
        if index == 0:
            las = lasio.read('./data/P11-A-02_Composite_MEM_Image_NF.las')
        else:
            las = lasio.read('./data/P11-A-01_Composite_MEM_Image_NF.las')
        df = las.df()
        return df[['GRAS0M', 'GRAS1M', 'GRAS2M', 'GRAS3M', 'GRAS4M',
                       'GRAS5M', 'GRAS6M', 'GRAS7M']]

    @staticmethod
    def measure(index=0):
        if index == 0:
            measureData = pd.read_excel("./data/measureData.xlsx")[
                ["Gamma0", "Gamma1", "Gamma2", "Gamma3", "Gamma4", "Gamma5", "Gamma6", "Gamma7"]]
        else:
            measureData = pd.read_excel("./data/newWell_data.xlsx")[
                ["Gamma0", "Gamma1", "Gamma2", "Gamma3", "Gamma4", "Gamma5", "Gamma6", "Gamma7"]]
        return measureData

    @staticmethod
    def cflog(index=0):
        fileList = ["GR_IMG.txt","3DP_Training_ProjectHW3.txt","Density_AllHW2.txt","HW1GR_IMG.txt","HW1GR_IMG_SM.txt","ROSC[0-15]HW1.txt","wei201-h3_LWD.txt"]
        data:pd.DataFrame = pd.read_csv("./data/aximuthImage/"+fileList[index],skiprows=8,sep="\s+",header=None).replace(-99999., np.nan)
        colList = ["DEPTH"]
        for i in range(data.shape[1]-1):
            colList.append("AXIM{}".format(i))
        data.columns = colList
        return data.set_index("DEPTH")



