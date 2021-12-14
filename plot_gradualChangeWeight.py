from MyTool.plotShow import *

w_f = np.linspace(1,0,100)
x = np.arange(100)
w_s = w_f[::-1]
plt.plot(x,w_f,linewidth=2,label="$\\vec w_{first}$")
plt.plot(x,w_s,linewidth=2,label="$\\vec w_{second}$")
plt.plot(x,w_s+w_f,linewidth=2,label="$\\vec w_{first}+\\vec w_{second}$")
addLabel("线性渐变权值","权值下标","权值大小")
plt.legend(fontsize=25)
plt.grid()

plt.show()