import numpy as np
import plotProblem

def problem2_plane_gate(planes,gatesList,dicFormula,dicFormulaReverse,answers):
    return recommend_First_Lates_Second(planes,gatesList,dicFormula,dicFormulaReverse,answers)
def recommend_First_Lates_Second(planes,gatesList,dicFormula,dicFormulaReverse,answers):
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
                if bestWeight < gatesTime[j]:  # 比较优先权
                    bestWeight = gatesTime[j]
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


def solveProblem_1 (matrix_sorted,relevant_gates):
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