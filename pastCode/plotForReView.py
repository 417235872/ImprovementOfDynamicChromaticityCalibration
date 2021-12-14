import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

if __name__ == '__main__':
    y = [1,0.997,0.994,0.986,0.981,0.965]
    x = [1,2,4,8,16,32]
    plt.plot(x,y, "o-")
    plt.grid()
    plt.xlim((0,35))
    #plt.ylim((0.94,1.02))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title("多线程的加速效率",fontsize=20)
    plt.xlabel("工作线程数",fontsize=18)
    plt.ylabel("加速比",fontsize=18)
    plt.show()