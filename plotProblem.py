import numpy as np
import matplotlib.pyplot as plt

#画柱状图并包含百分比
#输入为  dtype数组！！！！！！！！！！！！！！
def plt_bar(datalist,namelist,numFlag,name):
    x = list(range(datalist.__len__()))
    total_width, n = 0.8, 2
    width = total_width / n
    # plt.bar(x, np.asarray(datalist, dtype=np.float), width=width,
    #         tick_label=namelist, fc='r')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, np.asarray(datalist, dtype=np.float) / sum(numFlag), width=width,
            tick_label=namelist, fc='b')
    plt.title(name)
    plt.show()
def plt_line(coordList):
    for coord in coordList:
        x=np.linspace(coord[0][0],coord[1][0],50)
        y=np.linspace(coord[0][1],coord[1][1],50)
        plt.plot(x,y)
    plt.grid()
    plt.show()
    pass
# if __name__ == "__main__":
#     plt_line(list(np.array([[[0, 0],[1, 1]]],dtype=np.float) ))