import extractExcel
import numpy as np
import plotProblem
def printListAsMatrix(list):
    print(list.__len__())
    for i in list:
        print(i)
    print("\n")
    return
path = 'InputData.xlsx'
gates, gates_matrix = extractExcel.extractGate(path)
tickets, tickets_matrix = extractExcel.extractTicket(path)
pucks, pucks_matrix = extractExcel.extractPuck(path)
# printListAsMatrix(pucks_matrix)
W_type = ['332', '333', '33E', '33H', '33L','773']
N_type = ['319', '320', '321', '323', '325', '738', '73A', '73E', '73H', '73L']
# pucks_matrx 各属性对应列表
# 0:飞机专场记录
# 1:到达日期(date - 43119)
# 2:到达时间(min 为单位)
# 3:到达航班
# 4:到达类型
# 5:飞机类型
# 6:出发日期(date - 43119)
# 7:出发时间(min 为单位)
# 8:出发航班
# 9:出发类型
# 10:上个机场
# 11:下个机场

# puchks分组
DI_W_pucks_matrix = []
DI_N_pucks_matrix = []
ID_W_pucks_matrix = []
ID_N_pucks_matrix = []
DD_W_pucks_matrix = []
DD_N_pucks_matrix = []
II_W_pucks_matrix = []
II_N_pucks_matrix = []





###############################################预处理plane
#将matrix 中的飞机型号转出string
for i in pucks_matrix:
    if not isinstance(i[5], str):
        i[5] = str(int(i[5]))

for i in range(pucks_matrix.__len__()):
    if (pucks_matrix[i][4] == 'D'and pucks_matrix[i][9] == 'I'
            and( pucks_matrix[i][1] == 43120 or pucks_matrix[i][6] == 43120 )):
        if pucks_matrix[i][5] in W_type:
            DI_W_pucks_matrix.append(pucks_matrix[i])
        else:
            DI_N_pucks_matrix.append(pucks_matrix[i])
    elif (pucks_matrix[i][4] == 'I' and pucks_matrix[i][9] == 'D'
          and (pucks_matrix[i][1] == 43120 or pucks_matrix[i][6] == 43120)):
        if pucks_matrix[i][5] in W_type:
            ID_W_pucks_matrix.append(pucks_matrix[i])
        else:
            ID_N_pucks_matrix.append(pucks_matrix[i])
    elif (pucks_matrix[i][4] == 'D' and pucks_matrix[i][9] == 'D'
          and (pucks_matrix[i][1] == 43120 or pucks_matrix[i][6] == 43120)):
        if pucks_matrix[i][5] in W_type:
            DD_W_pucks_matrix.append(pucks_matrix[i])
        else:
            DD_N_pucks_matrix.append(pucks_matrix[i])
    elif (pucks_matrix[i][4] == 'I' and pucks_matrix[i][9] == 'I'
          and (pucks_matrix[i][1] == 43120 or pucks_matrix[i][6] == 43120)):
        if pucks_matrix[i][5] in W_type:
            II_W_pucks_matrix.append(pucks_matrix[i])
        else:
            II_N_pucks_matrix.append(pucks_matrix[i])
# print(DI_W_pucks_matrix.__len__(),DI_N_pucks_matrix.__len__(),ID_W_pucks_matrix.__len__()
#       ,ID_N_pucks_matrix.__len__(),DD_W_pucks_matrix.__len__(),DD_N_pucks_matrix.__len__()
#       ,II_W_pucks_matrix.__len__(),II_N_pucks_matrix.__len__())

#按照时间顺序排列
DI_W_pucks_matrix_sorted = sorted(DI_W_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)
DI_N_pucks_matrix_sorted = sorted(DI_N_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)

ID_W_pucks_matrix_sorted = sorted(ID_W_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)
ID_N_pucks_matrix_sorted = sorted(ID_N_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)

DD_W_pucks_matrix_sorted = sorted(DD_W_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)
DD_N_pucks_matrix_sorted = sorted(DD_N_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)

II_W_pucks_matrix_sorted = sorted(II_W_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)
II_N_pucks_matrix_sorted = sorted(II_N_pucks_matrix,key = lambda ele : ele[1]+ele[2]/24/60)
# printListAsMatrix(DI_W_pucks_matrix_sorted)
# printListAsMatrix(DI_N_pucks_matrix_sorted)
# printListAsMatrix(ID_W_pucks_matrix_sorted)
# printListAsMatrix(ID_N_pucks_matrix_sorted)
# printListAsMatrix(DD_W_pucks_matrix_sorted)
# printListAsMatrix(DD_N_pucks_matrix_sorted)
# printListAsMatrix(II_W_pucks_matrix_sorted)
# printListAsMatrix(II_N_pucks_matrix_sorted)

###############预处理GATE################################
gate_time = np.zeros(gates_matrix.__len__())

I_I_N_gates=[]  #4
I_I_W_gates=[]  #17
I_DI_W_gates=[] #1

D_D_N_gates=[]  #35
D_D_W_gates=[]  #2
D_DI_N_gates=[] #2

DI_DI_W_gates=[]    #3
DI_DI_N_gates=[]    #2
DI_D_N_gates=[]     #2
DI_I_W_gates=[]     #1

# printListAsMatrix(gates_matrix)
for gate in gates_matrix:
    if gate[3] == 'I' and gate[4] == 'I' and gate[5] == 'N':
        I_I_N_gates.append(gate)
    if gate[3] == 'I' and gate[4] == 'I' and gate[5] == 'W':
        I_I_W_gates.append(gate)
    if gate[3] == 'I' and gate[4] == 'D, I' and gate[5] == 'W':
        I_DI_W_gates.append(gate)
    if gate[3] == 'D' and gate[4] == 'D' and gate[5] == 'N':
        D_D_N_gates.append(gate)
    if gate[3] == 'D' and gate[4] == 'D' and gate[5] == 'W':
        D_D_W_gates.append(gate)
    if gate[3] == 'D' and gate[4] == 'D, I' and gate[5] == 'N':
        D_DI_N_gates.append(gate)
    if gate[3] == 'D, I' and gate[4] == 'D, I' and gate[5] == 'W':
        DI_DI_W_gates.append(gate)
    if gate[3] == 'D, I' and gate[4] == 'D, I' and gate[5] == 'N':
        DI_DI_N_gates.append(gate)
    if gate[3] == 'D, I' and gate[4] == 'D' and gate[5] == 'N':
        DI_D_N_gates.append(gate)
    if gate[3] == 'D, I' and gate[4] == 'I' and gate[5] == 'W':
        DI_I_W_gates.append(gate)
# print(I_I_N_gates.__len__()+I_I_W_gates.__len__()+I_DI_W_gates.__len__()
#       +D_D_N_gates.__len__()+D_D_W_gates.__len__()+D_DI_N_gates.__len__()
#       +DI_DI_W_gates.__len__()+DI_DI_N_gates.__len__()+DI_D_N_gates.__len__()
#       +DI_I_W_gates.__len__())
# printListAsMatrix(I_I_N_gates)
# printListAsMatrix(I_I_W_gates)
# printListAsMatrix(I_DI_W_gates)
#
# printListAsMatrix(D_D_N_gates)
# printListAsMatrix(D_D_W_gates)
# printListAsMatrix(D_DI_N_gates)
#
# printListAsMatrix(DI_DI_W_gates)
# printListAsMatrix(DI_DI_N_gates)
# printListAsMatrix(DI_D_N_gates)
# printListAsMatrix(DI_I_W_gates)
##################预处理gate结束####################################
####根据排队论+流水线处理第一问并画图
#飞机型号对应登机门，并针对不同问题画图

def plane_gate(planes,gatesList):
    return Lates_first(planes,gatesList)
    # return FCFS(planes,gatesList)

#先来先服务
def FCFS(planes,gatesList):
    gatesTime = np.zeros(gatesList.__len__())
    planeFlag = np.zeros(planes.__len__())
    resultGate = []
    resultArriveTime = []
    resultLeaveTime = []
    for i in range(planes.__len__()):
        flag = 0
        gateNum = 0  # 记录选择的gate的number
        for j in range(gatesTime.__len__()):
            if planes[i][1] * 24 * 60 + planes[i][2] >= gatesTime[j]:
                # 登机口独占 动态优先权算法
                flag = 1  # 找到至少一个
                gatesTime[j] = planes[i][6] * 24 * 60 + planes[i][7] + 45
                gateNum = j
                break
        planeFlag[i] = flag
        if flag == 1:
            resultArriveTime.append(planes[i][1] * 24 * 60 + planes[i][2])
            resultLeaveTime.append(planes[i][6] * 24 * 60 + planes[i][7])
            resultGate.append(gatesList[gateNum][0])
        else:
            resultArriveTime.append(-1)
            resultLeaveTime.append(-1)
            resultGate.append('fail')
    return planeFlag, resultGate, resultArriveTime, resultLeaveTime

#后完成的先接待
def Lates_first(planes,gatesList):
    gatesTime = np.zeros(gatesList.__len__())
    planeFlag = np.zeros(planes.__len__())
    resultGate = []
    resultArriveTime = []
    resultLeaveTime = []
    for i in range(planes.__len__()):
        flag = 0
        gateNum = 0  # 记录选择的gate的number
        bestWeight = -1  # 记录优先权
        for j in range(gatesTime.__len__()):
            if planes[i][1] * 24 * 60 + planes[i][2] >= gatesTime[j]:
                # 登机口独占 动态优先权算法
                flag = 1  # 找到至少一个
                if bestWeight < gatesTime[j]:  # 比较有限权
                    bestWeight = gatesTime[j]
                    # gatesTime[j] = planes[i][6] * 24 * 60 + planes[i][7] + 45
                    gateNum = j

        planeFlag[i] = flag
        if flag == 1:
            gatesTime[gateNum] = planes[i][6] * 24 * 60 + planes[i][7] + 45
            resultArriveTime.append(planes[i][1] * 24 * 60 + planes[i][2])
            resultLeaveTime.append(planes[i][6] * 24 * 60 + planes[i][7])
            resultGate.append(gatesList[gateNum][0])
        else:
            resultArriveTime.append(-1)
            resultLeaveTime.append(-1)
            resultGate.append('fail')
    return planeFlag, resultGate, resultArriveTime, resultLeaveTime
# printListAsMatrix(DD_N_pucks_matrix_sorted)
# printListAsMatrix(DI_DI_W_gates)
# printListAsMatrix(DI_I_W_gates)


def solvingProblem (matrix_sorted,relevant_gates):
    planeFlag,resultGate,resultArriveTime,resultLeaveTime=plane_gate(matrix_sorted,relevant_gates)
    print(planeFlag)
    print(  ( np.asarray(resultArriveTime,dtype= np.float)  ) )
    print(  ( np.asarray(resultLeaveTime,dtype= np.float)  ) )
    print( np.asarray(resultGate) )
    name_list = np.asarray(relevant_gates)[...,0]
    gate_count = {}
    #计算使用口数量
    for gates in relevant_gates:
        gate_count[gates[0]] = 0
    for gateName in resultGate:
        if gateName != 'fail':
            gate_count[gateName] = gate_count[gateName]+1
    plot_gate_array = []
    for name in name_list:
        plot_gate_array.append([name,int(gate_count[name])])

    # 画柱图
    # plot_gate_array=np.asarray(plot_gate_array)
    # plotProblem.plt_bar(np.asarray(plot_gate_array[...,1],dtype=np.float) ,plot_gate_array[...,0],numFlag=planeFlag,name = 'fig1')

    coordList =[]
    for i in range(resultGate.__len__()):
        if resultGate[i] != 'fail':
            flag = -1
            for j in range (relevant_gates.__len__()):
                if relevant_gates[j][0] == resultGate[i]:
                    flag = j
                    break
            coordstart = [resultArriveTime[i]-43119*24*60,flag]
            coordend = [resultLeaveTime[i]-43119*24*60,flag]
            coordList.append([coordstart,coordend])
    # 画线图
    plotProblem.plt_line(coordList)

solvingProblem(II_W_pucks_matrix_sorted,I_I_W_gates)

def usegate(planeName,gateID):

    pass
def leavegate(planeName,gateID):

    pass