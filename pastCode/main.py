# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lasio

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def showImageEX():
    las = lasio.read('../data/P11-A-02_Composite_MEM_Image_NF.las')
    df = las.df()
    azidendf = df[['ABDC1M', 'ABDC2M', 'ABDC3M', 'ABDC4M', 'ABDC5M',
                   'ABDC6M', 'ABDC7M', 'ABDC8M', 'ABDC9M', 'ABDC10M',
                   'ABDC11M', 'ABDC12M', 'ABDC13M', 'ABDC14M', 'ABDC15M',
                   'ABDC16M']]

    azigamdf = df[['GRAS0M', 'GRAS1M', 'GRAS2M', 'GRAS3M', 'GRAS4M',
                   'GRAS5M', 'GRAS6M', 'GRAS7M']]
    plt.figure(figsize=(7, 15))
    miny = azidendf.index.min()
    maxy = azidendf.index.max()
    plt.imshow(azidendf, interpolation='none',
               aspect='auto', cmap=plt.cm.YlOrRd,
               vmin=1.5, vmax=2.6,
               extent=[0, 360, maxy, miny])

    plt.ylim(2130, 2100)

    plt.colorbar(orientation='horizontal', pad=0.03)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    def func(x):
        return x**0.5*np.exp(-x)
    xMax = 10
    bin = 1000
    x = np.linspace(0,xMax,bin)
    y = func(x)
    plt.plot(x,y)
    plt.grid()
    plt.title(y.sum()*xMax/bin)
    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
