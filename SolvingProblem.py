import numpy as np
import plotProblem


def problem2_plane_gate(planes, gatesList, dicFormula, dicFormulaReverse, answers):
    return recommend_First_random_Lates_Second(planes,gatesList,dicFormula,dicFormulaReverse,answers)
    # return recommend_First_wise_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers)


def recommend_First_random_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers):
    # 设航站楼T为0,卫星厅S为1
    # 记录gate释放时间
    gatesTime = np.zeros(gatesList.__len__())
    # 记录找到gate标记
    planeFlag = np.zeros(planes.__len__())
    # 记录找到bestGate标记
    planeBestFlag = np.zeros(planes.__len__())
    resultGate = []
    resultArriveTime = []
    resultLeaveTime = []

    for i in range(planes.__len__()):
        flag = 0
        gateNum = 0  # 记录选择的gate的number
        bestWeight = -1  # 记录优先权
        bestFlag = 0
        # 第一步 确定是否会失败
        # 第二步 确定是否有最优解(对应的登机口且空闲值最小)
        # 第三步 确定是否次优解(空闲值最小)
        for j in range(gatesTime.__len__()):
            if planes[i][1] * 24 * 60 + planes[i][2] >= gatesTime[j]:
                # 登机口独占 动态优先权算法
                flag = 1  # 找到至少一个
                if dicFormula.__contains__(planes[i][0]) and \
                        ((answers[dicFormula[planes[i][0]]] == 0 and gatesList[j][1] == 'T') \
                         or (answers[dicFormula[planes[i][0]]] == 1 and gatesList[j][1] == 'S')):
                    # 存在解对应的类型,则使用另外一个循环
                    bestFlag = 1
                    break
                if bestWeight < gatesTime[j]:  # 比较优先权
                    bestWeight = gatesTime[j]
                    gateNum = j
        if bestFlag == 1:
            # 进入此循环后重新记录bestWeight
            bestWeight = -1
            for j in range(gatesTime.__len__()):
                if planes[i][1] * 24 * 60 + planes[i][2] >= gatesTime[j]:
                    # 找同一类型
                    if dicFormula.__contains__(planes[i][0]) and \
                            ((answers[dicFormula[planes[i][0]]] == 0 and gatesList[j][1] == 'T') or (
                                    answers[dicFormula[planes[i][0]]] == 1 and gatesList[j][1] == 'S')):
                        # 找最繁忙的gate
                        if bestWeight < gatesTime[j]:  # 比较优先权
                            bestWeight = gatesTime[j]
                            gateNum = j
        planeFlag[i] = flag
        planeBestFlag[i] = bestFlag
        # 不管有没有找到最优解都要更新时间
        if flag == 1:
            gatesTime[gateNum] = planes[i][6] * 24 * 60 + planes[i][7] + 45
            resultArriveTime.append(planes[i][1] * 24 * 60 + planes[i][2])
            resultLeaveTime.append(planes[i][6] * 24 * 60 + planes[i][7])
            resultGate.append(gatesList[gateNum][0])
        else:
            resultArriveTime.append(-1)
            resultLeaveTime.append(-1)
            resultGate.append('fail')
    return planeFlag, planeBestFlag, resultGate, resultArriveTime, resultLeaveTime


def recommend_First_wise_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers):
    # 设航站楼T为0,卫星厅S为1
    # 记录gate释放时间
    gatesTime = np.zeros(gatesList.__len__())
    # 记录找到gate标记
    planeFlag = np.zeros(planes.__len__())
    # 记录找到bestGate标记
    planeBestFlag = np.zeros(planes.__len__())
    resultGate = []
    resultArriveTime = []
    resultLeaveTime = []
    # 剩余飞机中有recommendation的
    rest_plane_Req = []
    # 剩余未占用的门
    rest_gate_T = 0
    rest_gate_S = 0
    T_reqSum = 0
    S_reqSum = 0
    ST_reqSum = 0
    for i in range(planes.__len__()):
        if dicFormula.__contains__(planes[i][0]):
            ST_reqSum = ST_reqSum + 1
            if answers[dicFormula[planes[i][0]]] == 0:
                T_reqSum = T_reqSum + 1
            else:
                S_reqSum = S_reqSum + 1
    for i in range(planes.__len__()):
        if i == 0:
            if dicFormula.__contains__(planes[i][0]):
                ST_reqSum = ST_reqSum - 1
                if answers[dicFormula[planes[i][0]]] == 0:
                    T_reqSum = T_reqSum - 1
                else:
                    S_reqSum = S_reqSum - 1
            rest_plane_Req.append([ST_reqSum, T_reqSum, S_reqSum])
        else:
            if dicFormula.__contains__(planes[i][0]):
                ST_reqSum = ST_reqSum - 1
                if answers[dicFormula[planes[i][0]]] == 0:
                    T_reqSum = T_reqSum - 1
                else:
                    S_reqSum = S_reqSum - 1
                rest_plane_Req.append([ST_reqSum, T_reqSum, S_reqSum])
            else:
                rest_plane_Req.append(rest_plane_Req[-1])
    # print(restReq)
    for i in range(planes.__len__()):
        flag = 0
        gateNum = 0  # 记录选择的gate的number
        S_gateNum_No_recommend = 0  # 给不在推荐列表里的飞机选择的门
        T_gateNum_No_recommend = 0  # 给不在推荐列表里的飞机选择的门
        S_bestWeight = -1  # 记录优先权
        T_bestWeight = -1
        # bestWeight = -1     #最终返回的weight
        bestFlag = 0
        # 第一步 确定是否会失败
        # 第二步 确定是否有最优解(对应的登机口且空闲值最小)
        # 第三步 确定是否次优解(空闲值最小,根据S，T门紧张情况进行选择)
        for j in range(gatesTime.__len__()):
            if planes[i][1] * 24 * 60 + planes[i][2] >= gatesTime[j]:
                # 登机口独占 动态优先权算法
                flag = 1  # 找到至少一个
                if (gatesList[j][1] == 'T'):
                    rest_gate_T = rest_gate_T + 1
                else:
                    rest_gate_S = rest_gate_S + 1
                if dicFormula.__contains__(planes[i][0]) and \
                        ((answers[dicFormula[planes[i][0]]] == 0 and gatesList[j][1] == 'T') \
                         or (answers[dicFormula[planes[i][0]]] == 1 and gatesList[j][1] == 'S')):
                    # 存在解对应的类型,则使用另外一个循环
                    bestFlag = 1
                    break
                # 更新两个不同类型的次优解
                if gatesList[j][1] == 'T':
                    if T_bestWeight < gatesTime[j]:
                        T_bestWeight = gatesTime[j]
                        T_gateNum_No_recommend = j
                else:
                    if S_bestWeight < gatesTime[j]:
                        S_bestWeight = gatesTime[j]
                        S_gateNum_No_recommend = j

        if flag == 1 and bestFlag == 1:
            # 进入此循环后重新记录bestWeight
            bestWeight = -1
            for j in range(gatesTime.__len__()):
                if planes[i][1] * 24 * 60 + planes[i][2] >= gatesTime[j]:
                    # 找同一类型
                    if dicFormula.__contains__(planes[i][0]) and \
                            ((answers[dicFormula[planes[i][0]]] == 0 and gatesList[j][1] == 'T') or (
                                    answers[dicFormula[planes[i][0]]] == 1 and gatesList[j][1] == 'S')):
                        # 找最繁忙的gate
                        if bestWeight < gatesTime[j]:  # 比较优先权
                            bestWeight = gatesTime[j]
                            gateNum = j
        elif flag == 1 and bestFlag == 0:
            # 找次优解
            if ST_reqSum == 0:
                if S_bestWeight > T_bestWeight:
                    # bestWeight = S_bestWeight
                    gateNum = S_gateNum_No_recommend
                else:  # 可能导致优先选T
                    # bestWeight = T_bestWeight
                    gateNum = T_gateNum_No_recommend
            else:
                if (rest_gate_T - rest_plane_Req[1] > rest_gate_S - rest_plane_Req[2]):
                    # bestWeight = T_bestWeight
                    gateNum = T_gateNum_No_recommend
                else:
                    # bestWeight = S_bestWeight
                    gateNum = S_gateNum_No_recommend

            # if bestWeight < gatesTime[j]:  # 比较优先权
            #     bestWeight = gatesTime[j]
            #     gateNum = j
        planeFlag[i] = flag
        planeBestFlag[i] = bestFlag
        # 不管有没有找到最优解,只要找到解都要更新时间
        if flag == 1:
            gatesTime[gateNum] = planes[i][6] * 24 * 60 + planes[i][7] + 45
            resultArriveTime.append(planes[i][1] * 24 * 60 + planes[i][2])
            resultLeaveTime.append(planes[i][6] * 24 * 60 + planes[i][7])
            resultGate.append(gatesList[gateNum][0])
        else:
            resultArriveTime.append(-1)
            resultLeaveTime.append(-1)
            resultGate.append('fail')
    return planeFlag, planeBestFlag, resultGate, resultArriveTime, resultLeaveTime


def plane_gate(planes, gatesList):
    return Lates_first(planes, gatesList)
    # return FCFS(planes,gatesList)


# 先来先服务
def FCFS(planes, gatesList):
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


# 后完成的先接待
def Lates_first(planes, gatesList):
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


def solveProblem_1(matrix_sorted, relevant_gates):
    planeFlag, resultGate, resultArriveTime, resultLeaveTime = plane_gate(matrix_sorted, relevant_gates)
    print(planeFlag)
    print(planeFlag.sum())
    # print((np.asarray(resultArriveTime, dtype=np.float)))
    # print((np.asarray(resultLeaveTime, dtype=np.float)))
    # print(np.asarray(resultGate))
    name_list = np.asarray(relevant_gates)[..., 0]
    gate_count = {}
    # 计算使用口数量
    for gates in relevant_gates:
        gate_count[gates[0]] = 0
    for gateName in resultGate:
        if gateName != 'fail':
            gate_count[gateName] = gate_count[gateName] + 1
    plot_gate_array = []
    for name in name_list:
        plot_gate_array.append([name, int(gate_count[name])])

    # 画柱图
    # plot_gate_array=np.asarray(plot_gate_array)
    # plotProblem.plt_bar(np.asarray(plot_gate_array[...,1],dtype=np.float) ,plot_gate_array[...,0],numFlag=planeFlag,name = 'fig1')

    coordList = []
    for i in range(resultGate.__len__()):
        if resultGate[i] != 'fail':
            flag = -1
            for j in range(relevant_gates.__len__()):
                if relevant_gates[j][0] == resultGate[i]:
                    flag = j
                    break
            coordstart = [resultArriveTime[i] - 43119 * 24 * 60, flag]
            coordend = [resultLeaveTime[i] - 43119 * 24 * 60, flag]
            coordList.append([coordstart, coordend])
    # 画线图
    plotProblem.plt_line(coordList)
