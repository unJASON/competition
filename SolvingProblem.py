import numpy as np
import plotProblem
import random
import matplotlib.pyplot as plt
import copy
def problem2_plane_gate(planes, gatesList, dicFormula, dicFormulaReverse, answers):
    # return recommend_First_random_Lates_Second(planes,gatesList,dicFormula,dicFormulaReverse,answers)
    return recommend_First_wise_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers)
    # return recommend_First_wise2_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers)
def problem3_plane_gate(planes, gatesList, dicFormula, dicFormulaReverse, answers):
    return recommend_First_wise2_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers)
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

def recommend_First_wise2_Lates_Second(planes, gatesList, dicFormula, dicFormulaReverse, answers):
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
    return Late_first(planes, gatesList)
    # return FCFS(planes,gatesList)
    # return GA_reduce_gate(planes,gatesList)


    # return IGA_reduce_gate(planes,gatesList)

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
def Late_first(planes, gatesList):
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
    # plotProblem.plt_line(coordList)
    return planeFlag, resultGate, resultArriveTime, resultLeaveTime

def GA_reduce_gate(planes,gatesList,max_iter=10000):
    #生成300随机数列
    generationList =[]
    # 保存每次迭代得到的最优解
    optimalSolutions = []
    optimalValues = []
    previlege = np.random.permutation(planes.__len__())
    # for i in range(500):
    #     a = np.zeros(planes.__len__())
    #     for ser_i in range( planes.__len__() ):
    #         a[ser_i] = random.randint(0,gatesList.__len__()-1)
    #     generationList.append(a)


    for i in range(1000):
        a = np.zeros(planes.__len__())
        for ser_i in range( planes.__len__() ):
            gatesLength = gatesList.__len__()
            a[ser_i] = previlege[(ser_i+i)%planes.__len__()] % gatesLength
        generationList.append(a)
    #使用适应度函数,生成概率模型

    generationList = np.asarray(generationList,dtype=np.int)
    cnt = 0
    for i in range(max_iter):
        cnt = cnt + 1
        # print(generationList[0])
        evaluates,cum_proba=fit_value(generationList,planes,gatesList)
        #轮盘选下一代generation
        newpopulations = selectNewPopulation(generationList, cum_proba)
        # print(newpopulations[0:10])
        # 进行交叉操作
        crossoverpopulation = crossover(newpopulations)
        # print(crossoverpopulation[0:10])
        # 进行变异
        mutationpopulation = mutation(crossoverpopulation,gatesList.__len__())
        #分析函数，保存每次的结果模型
        evaluates, cum_proba = fit_value(mutationpopulation, planes, gatesList)

        generationList = np.copy(mutationpopulation)

        optimalValues.append(np.max(list(evaluates)))
        index = np.where(evaluates == max(list(evaluates)))
        optimalSolutions.append(generationList[index[0][0],:])
        if cnt %100 == 0:
            print("np.max(optimalValues):",np.max(optimalValues))



    #返回迭代后的最优结果
    # 搜索最优解
    optimalValue = np.max(optimalValues)
    optimalIndex = np.where(optimalValues == optimalValue)
    optimalSolution = optimalSolutions[optimalIndex[0][0]]
    return optimalSolution, optimalValue
# 得到个体的适应度值及每个个体被选择的累积概率
def fit_value(generationList,planes,gatesList):
    # 得到种群规模和决策变量的个数
    population, nums = generationList.shape
    # 初始化种群的适应度值为0
    fitnessvalues = np.zeros((population, 1))
    # 计算适应度值
    for i in range(population):
        fitnessvalues[i, 0] = GA_gates_Num(generationList[i, :],planes,gatesList)
    probability = fitnessvalues*1.0 / np.sum(fitnessvalues)
    cum_probability = np.cumsum(probability)
    return fitnessvalues,cum_probability
def GA_gates_Num(plane_order,planes,gatesList):
    count = 0
    gate_plane_group = {}
    #根据gate的number分组
    #分组求效率
    #1.计算门使用效率
    #2.减小门的使用数量
    #plane_order:对应planes中plane选择的门
    #分组
    for i in range(planes.__len__()):
        # print("plane_order[i]:"+str(plane_order[i]))
        if(gate_plane_group.__contains__(gatesList[ plane_order[i] ][0])):
            gate_plane_group[ gatesList[plane_order[i]][0] ].append(planes[i])
        else:
            gate_plane_group[gatesList[plane_order[i]][0]] = []
            gate_plane_group[gatesList[plane_order[i]][0]].append(planes[i])

    for group in gate_plane_group.values():
        group = sorted(group,key=lambda ele: ele[6] + ele[7] / 24 / 60)
        for i in range(group.__len__()):
            if i == 0:
                count = count+1
            else:
                if group[i][1]*24*60+group[i][2] >= group[i-1][6]*24*60 + group[i-1][7] + 45:
                    count = count +1
                else:
                    pass
    # print("count:"+str(count)+"gate_plane_group:"+str(gate_plane_group.__len__()))
    return count*100+(gatesList.__len__()-gate_plane_group.__len__())*1

def selectNewPopulation(chromosomes,cum_probability):
    m, n = chromosomes.shape
    newpopulation = np.zeros((m, n), dtype=np.uint8)
    # 随机产生M个概率值
    randoms = np.random.rand(m)
    for i, randoma in enumerate(randoms):
        logical = cum_probability >= randoma
        index = np.where(logical == 1)
        # index是tuple,tuple中元素是ndarray
        newpopulation[i, :] = chromosomes[index[0][0], :]
    return newpopulation

def crossover(population,Pc=1.0):
    """
        :param population: 新种群
        :param Pc: 交叉概率默认是0.8
        :return: 交叉后得到的新种群
        """
    # 根据交叉概率计算需要进行交叉的个体个数
    m, n = population.shape
    numbers = np.uint8(m * Pc)
    # 确保进行交叉的染色体个数是偶数个
    if numbers % 2 != 0:
        numbers += 1
    # 交叉后得到的新种群
    updatepopulation = np.zeros((m, n), dtype=np.uint8)
    # 产生随机索引
    index = random.sample(range(m), numbers)
    # 不进行交叉的染色体进行复制
    for i in range(m):
        if not index.__contains__(i):
            updatepopulation[i, :] = population[i, :]
    # crossover
    while len(index) > 0:
        a = index.pop()
        b = index.pop()
        # 随机产生一个交叉点
        crossoverPoint = random.sample(range(1, n), 1)
        crossoverPoint = crossoverPoint[0]
        # one-single-point crossover
        updatepopulation[a, 0:crossoverPoint] = population[a, 0:crossoverPoint]
        updatepopulation[a, crossoverPoint:] = population[b, crossoverPoint:]
        updatepopulation[b, 0:crossoverPoint] = population[b, 0:crossoverPoint]
        updatepopulation[b, crossoverPoint:] = population[a, crossoverPoint:]
    return updatepopulation
def mutation(population,randNum, Pm=0.05):
    """
        :param population: 经交叉后得到的种群
        :param Pm: 变异概率默认是0.01
        :return: 经变异操作后的新种群
        """
    updatepopulation = np.copy(population)
    m, n = population.shape
    # 计算需要变异的基因个数
    gene_num = np.uint8(m * n * Pm)
    # 将所有的基因按照序号进行10进制编码，则共有m*n个基因
    # 随机抽取gene_num个基因进行基本位变异
    mutationGeneIndex = random.sample(range(0, m * n), gene_num)
    # 确定每个将要变异的基因在整个染色体中的基因座(即基因的具体位置)
    for gene in mutationGeneIndex:
        # 确定变异基因位于第几个染色体
        chromosomeIndex = gene // n
        # 确定变异基因位于当前染色体的第几个基因位
        geneIndex = gene % n
        #改为随机重新分配
        updatepopulation[chromosomeIndex, geneIndex] = random.randint(0,randNum-1)
        # mutation 倒置
        # another_ind = -1
        # while True:
        #     another_ind=np.random.randint(n)
        #     if another_ind != geneIndex:
        #         break;
        # mutationInts = population[chromosomeIndex,min(geneIndex,another_ind):max(geneIndex,another_ind)]
        # mutationInts = mutationInts[::-1]
        # updatepopulation[chromosomeIndex,min(geneIndex,another_ind):max(geneIndex,another_ind)] = mutationInts
    return updatepopulation
def IGA_reduce_gate(planes,gatesList,max_iter=10000):
    # 生成300随机数列
    generationList = []
    # 保存每次迭代得到的最优解
    optimalSolutions = []
    optimalValues = []
    previlege = np.random.permutation(planes.__len__())
    for i in range(100):
        a = np.zeros(planes.__len__())
        for ser_i in range(planes.__len__()):
            a[ser_i] = random.randint(0, gatesList.__len__() - 1)
        generationList.append(a)
    generationList = np.asarray(generationList,dtype=np.int)
    cnt = 0
    for i in range(max_iter):
        cnt = cnt + 1
        # print(generationList[0])
        evaluates,cum_proba=fit_value(generationList,planes,gatesList)
        #轮盘选下一代generation
        newpopulations = selectNewPopulation(generationList, cum_proba)
        # print(newpopulations[0:10])
        # 进行交叉操作
        crossoverpopulation = crossover(newpopulations)
        # print(crossoverpopulation[0:10])
        # 进行变异
        mutationpopulation = mutation(crossoverpopulation,gatesList.__len__())
        # print(mutationpopulation[0:10])
        #分析函数，保存每次的结果模型
        evaluates, cum_proba = fit_value(mutationpopulation, planes, gatesList)

        optimalValues.append(np.max(list(evaluates)))
        index = np.where(evaluates == max(list(evaluates)))
        optimalSolutions.append(mutationpopulation[index[0][0],:])
        if cnt %100 == 0:
            print("np.max(optimalValues):",np.max(optimalValues))
        generationList = np.copy(mutationpopulation)


    #返回迭代后的最优结果
    # 搜索最优解
    optimalValue = np.max(optimalValues)
    optimalIndex = np.where(optimalValues == optimalValue)
    optimalSolution = optimalSolutions[optimalIndex[0][0]]
    return optimalSolution, optimalValue

def problem3_plane_gate(plane_gate_mapper, dicFormula, dicFormulaReverse,arriving_pucks_tickets_leaving_pucks):
    optimalSolution, optimalValue = Ga_reduce_gate_user_confidence(plane_gate_mapper, dicFormula, dicFormulaReverse,arriving_pucks_tickets_leaving_pucks)
    loss, nerv, gate_left, failList=GA_gates_Num_user_confidence(optimalSolution,plane_gate_mapper,arriving_pucks_tickets_leaving_pucks)
    return nerv,gate_left,failList,optimalSolution
#为第三题写的遗传算法
def Ga_reduce_gate_user_confidence(plane_gate_mapper, dicFormula, dicFormulaReverse,arriving_pucks_tickets_leaving_pucks,max_iter=10000):
    # 生成300随机数列
    generationList = []
    # 保存每次迭代得到的最优解
    optimalSolutions = []
    optimalValues = []
    for i in range(50):
        a = []
        for mapper in plane_gate_mapper:
            b = np.zeros(mapper[0].__len__())
            for ser_i in range( mapper[0].__len__() ):
                b[ser_i] = random.randint(0,mapper[1].__len__()-1)
            a.append(b)
        generationList.append(a)
    # 使用适应度函数,生成概率模型

    # generationList = np.asarray(generationList, dtype=np.int)
    cnt = 0
    for i in range(max_iter):
        cnt = cnt + 1
        # print(generationList[0])
        evaluates, cum_proba = fit_value_user_confidence(generationList, plane_gate_mapper, arriving_pucks_tickets_leaving_pucks)
        # 轮盘选下一代generation
        newpopulations = selectNewPopulation_user_confidence(generationList, cum_proba)
        # print(newpopulations[0:10])
        # 进行交叉操作
        crossoverpopulation = crossover_user_confidence(newpopulations)
        # print(crossoverpopulation[0:10])
        # 进行变异
        mutationpopulation = mutation_user_confidence(crossoverpopulation,plane_gate_mapper)
        # 分析函数，保存每次的结果模型
        evaluates, cum_proba = fit_value_user_confidence(mutationpopulation, plane_gate_mapper, arriving_pucks_tickets_leaving_pucks)

        generationList = np.copy(mutationpopulation)

        optimalValues.append(np.max(list(evaluates)))
        index = np.where(evaluates == max(list(evaluates)))
        optimalSolutions.append(generationList[index[0][0], :])
        if cnt % 100 == 0:
            print("np.max(optimalValues):", np.max(optimalValues))

    # 返回迭代后的最优结果
    # 搜索最优解
    optimalValue = np.max(optimalValues)
    optimalIndex = np.where(optimalValues == optimalValue)
    optimalSolution = optimalSolutions[optimalIndex[0][0]]
    return optimalSolution, optimalValue



def split_as_list(a,size):
    pass


def fit_value_user_confidence(generationList, plane_gate_mapper, arriving_pucks_tickets_leaving_pucks):
    fitnessvalues = np.zeros((generationList.__len__(), 1))
    # 计算适应度值
    for i in range(generationList.__len__()):
        loss = GA_gates_Num_user_confidence(generationList[i],plane_gate_mapper,arriving_pucks_tickets_leaving_pucks)
        fitnessvalues[i, 0] = loss[0]
    probability = fitnessvalues*1.0 / np.sum(fitnessvalues)
    cum_probability = np.cumsum(probability)
    return fitnessvalues,cum_probability

def selectNewPopulation_user_confidence(chromosomes, cum_probability):
    m = chromosomes.__len__()
    newpopulation = []
    # 随机产生M个概率值
    randoms = np.random.rand(m)
    for i, randoma in enumerate(randoms):
        logical = cum_probability >= randoma
        index = np.where(logical == 1)
        # index是tuple,tuple中元素是ndarray
        newpopulation.append( chromosomes[index[0][0]] )
    return newpopulation
def crossover_user_confidence(population,Pc=1.0):
    """
           :param population: 新种群
           :param Pc: 交叉概率默认是0.8
           :return: 交叉后得到的新种群
           """
    # 根据交叉概率计算需要进行交叉的个体个数
    # m, n = population.shape
    m = population.__len__()
    numbers = np.uint8(m * Pc)
    # 确保进行交叉的染色体个数是偶数个
    if numbers % 2 != 0:
        numbers += 1
    # 交叉后得到的新种群
    # updatepopulation = np.zeros((m, n), dtype=np.uint8)
    updatepopulation = []
    # 产生随机索引
    index = random.sample(range(m), numbers)
    # 不进行交叉的染色体进行复制
    for i in range(m):
        if not index.__contains__(i):
            updatepopulation.append(population[i])
    # crossover
    while len(index) > 0:
        a = index.pop()
        b = index.pop()
        # 随机产生一个交叉点
        #针对每个基因片段都产生交叉
        switch_a = []
        switch_b = []
        for j in range(population[0].__len__()):
            # 针对每个基因片段都产生交叉
            crossoverPoint = random.sample( range(1, population[0][j].__len__() ), 1)
            crossoverPoint = crossoverPoint[0]
            # one-single-point crossover
            switch_a = copy.deepcopy(population[a])
            switch_b = copy.deepcopy(population[b])
            switch_a[j][0:crossoverPoint] = population[a][j][0:crossoverPoint]
            switch_a[j][crossoverPoint:] = population[b][j][crossoverPoint:]
            switch_b[j][0:crossoverPoint] = population[b][j][0:crossoverPoint]
            switch_b[j][crossoverPoint:] = population[a][j][crossoverPoint:]
        updatepopulation.append(switch_a)
        updatepopulation.append(switch_b)
    return updatepopulation
def mutation_user_confidence(population,plane_gate_mapper, Pm=0.05):
    """
            :param population: 经交叉后得到的种群
            :param Pm: 变异概率默认是0.01
            :return: 经变异操作后的新种群
            """
    m = population.__len__()
    updatepopulation = copy.deepcopy(population)
    for i in range( population[0].__len__() ):
        # 计算需要变异的基因个数
        n = population[0][i].__len__()
        gene_num = np.uint8(m * n * Pm)
        # 将所有的基因按照序号进行10进制编码，则共有m*n个基因
        # 随机抽取gene_num个基因进行基本位变异

        mutationGeneIndex = random.sample(range(0, m * n), gene_num)
        # 确定每个将要变异的基因在整个染色体中的基因座(即基因的具体位置)
        for gene in mutationGeneIndex:
            # 确定变异基因位于第几个染色体
            chromosomeIndex = gene // n
            # 确定变异基因位于当前染色体的第几个基因位
            geneIndex = gene % n
            # 改为随机重新分配
            updatepopulation[chromosomeIndex][i] [geneIndex] = random.randint(0, plane_gate_mapper[i][1].__len__() - 1)

    return updatepopulation
global_value={}
def analyse_nerv(come_gate,com_dir_str,ti,go_gate,go_dir_str):
    global global_value
    fastS = come_gate + "_" + go_gate + "_" + ti[4] + "_" + ti[27] + "_" + str(com_dir_str) + "_" + str(
        go_dir_str) + "_" + ti[12] + "_" + str(ti[13])
    # 找到求过的解
    if global_value.__contains__(fastS):
        return global_value[fastS]
    value = 0
    com_dir = -1
    go_dir = -1
    walking_weight = [10, 15, 20, 25, 20, 25, 25,
                      15, 10, 15, 20, 15, 20, 20,
                      20, 15, 10, 25, 20, 25, 25,
                      20, 20, 25, 10, 15, 20, 20,
                      25, 15, 20, 15, 10, 15, 15,
                      25, 20, 25, 20, 15, 10, 20,
                      25, 20, 25, 20, 15, 20, 10]
    walking_weight = np.asarray(walking_weight, dtype=np.float).reshape((7, 7))
    if come_gate == 'S':
        if com_dir_str == "North":
            com_dir = 3
        elif com_dir_str == "Center":
            com_dir = 4
        elif com_dir_str == "South":
            com_dir = 5
        else:
            com_dir = 6
    else:
        if com_dir_str == "North":
            com_dir = 0
        elif com_dir_str == "Center":
            com_dir = 1
        else:
            com_dir = 2

    if go_gate == 'S':
        if go_dir_str == "North":
            go_dir = 3
        elif go_dir_str == "Center":
            go_dir = 4
        elif go_dir_str == "South":
            go_dir = 5
        else:
            go_dir = 6
    else:
        if go_dir_str == "North":
            go_dir = 0
        elif go_dir_str == "Center":
            go_dir = 1
        else:
            go_dir = 2

    if come_gate == 'S' and go_gate == 'T' and ti[4] == 'I' and ti[27] == 'I':
        value = (30 + walking_weight[com_dir][go_dir] + 8) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))
    if come_gate == 'S' and go_gate == 'T' and ti[4] == 'I' and ti[27] == 'D':
        value = (40 + walking_weight[com_dir][go_dir] + 8) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))
    if come_gate == 'S' and go_gate == 'T' and ti[4] == 'D' and ti[27] == 'I':
        value = (40 + walking_weight[com_dir][go_dir] + 8) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))
    if come_gate == 'S' and go_gate == 'T' and ti[4] == 'D' and ti[27] == 'D':
        value = (20 + walking_weight[com_dir][go_dir] + 8) / (
                float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'S' and go_gate == 'S' and ti[4] == 'I' and ti[27] == 'I':
        value = (20 + walking_weight[com_dir][go_dir]) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'S' and go_gate == 'S' and ti[4] == 'I' and ti[27] == 'D':
        value = (45 + walking_weight[com_dir][go_dir] + 16) / (
                float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))
    if come_gate == 'S' and go_gate == 'S' and ti[4] == 'D' and ti[27] == 'I':
        value = (35 + walking_weight[com_dir][go_dir]) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'S' and go_gate == 'S' and ti[4] == 'D' and ti[27] == 'D':
        value = (15 + walking_weight[com_dir][go_dir]) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'T' and ti[4] == 'I' and ti[27] == 'I':
        value = (20 + walking_weight[com_dir][go_dir]) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'T' and ti[4] == 'I' and ti[27] == 'D':
        value = (35 + walking_weight[com_dir][go_dir]) / (
                float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'T' and ti[4] == 'D' and ti[27] == 'I':
        value = (35 + walking_weight[com_dir][go_dir]) / (
                float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'T' and ti[4] == 'D' and ti[27] == 'D':
        value = (15 + walking_weight[com_dir][go_dir]) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'S' and ti[4] == 'I' and ti[27] == 'I':
        value = (30 + walking_weight[com_dir][go_dir] + 8) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'S' and ti[4] == 'I' and ti[27] == 'D':
        value = (40 + walking_weight[com_dir][go_dir] + 8) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'S' and ti[4] == 'D' and ti[27] == 'I':
        value = (40 + walking_weight[com_dir][go_dir] + 8) / (
                float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    if come_gate == 'T' and go_gate == 'S' and ti[4] == 'D' and ti[27] == 'D':
        value = (20 + walking_weight[com_dir][go_dir] + 8) / (
                    float(ti[24]) * 24 * 60 + float(ti[25]) - float(ti[1]) * 24 * 60 - float(ti[2]))

    #存储之前计算过解
    global_value[fastS] = float(ti[13]) * value

    return float(ti[13]) * value
def GA_gates_Num_user_confidence(generationGroup,plane_gate_mapper,arriving_pucks_tickets_leaving_pucks):
    count = 0
    #门和飞机对应分组
    gate_plane_group = {}
    failList = []
    for i in range( generationGroup.__len__() ):
        # 分组
        for j in range(generationGroup[i].__len__()):
            # print("plane_order[i]:"+str(plane_order[i]))
            if (gate_plane_group.__contains__(plane_gate_mapper[i][1][ int(generationGroup[i][j]) ][0])):
                gate_plane_group[plane_gate_mapper[i][1][ int(generationGroup[i][j]) ][0]].append(plane_gate_mapper[i][0][j])
            else:
                gate_plane_group[plane_gate_mapper[i][1][ int(generationGroup[i][j]) ][0]] = []
                gate_plane_group[plane_gate_mapper[i][1][ int(generationGroup[i][j]) ][0]].append(plane_gate_mapper[i][0][j])
    # 1.提高门使用次数，尽量减小临时机场使用次数
    for group in gate_plane_group.values():
        group = sorted(group, key=lambda ele: ele[6] + ele[7] / 24 / 60)
        for i in range(group.__len__()):
            if i == 0:
                count = count + 1
            else:
                if group[i][1] * 24 * 60 + group[i][2] >= group[i - 1][6] * 24 * 60 + group[i - 1][7] + 45:
                    count = count + 1
                else:
                    failList.append(group[0][0])
                    pass
    # 2.减小客户焦虑时间
        #逆向建立飞机-登机口表

    plane_gate_index = {}
    for gate_name in gate_plane_group.keys():
        for plane in gate_plane_group[gate_name]:
            plane_gate_index[plane[0]] = gate_name
        # 建立登机口索引表
    gate_index = {} #name-gate
    for plane_gate in plane_gate_mapper:
        for gate in plane_gate[1]:
            if gate_index.__contains__(gate[0]):
                pass
            else:
                gate_index[gate[0]] = gate
        #开始进行紧张度计算
    nerv = 0
    for ti in arriving_pucks_tickets_leaving_pucks:
        if failList.__contains__(ti[0]) or failList.__contains__(ti[18]):
            nerv = nerv + 3600*float(ti[13])
        else:
            nerv = nerv + analyse_nerv(gate_index[plane_gate_index[ti[0]]][1],
                                       gate_index[plane_gate_index[ti[0]]][2],
                                       ti,
                                       gate_index[plane_gate_index[ti[18]]][1],
                                       gate_index[plane_gate_index[ti[18]]][2])
    # 3.减小门使用数量
    totalgates = 67
    # for group in gate_plane_group:
    #   totalgates = totalgates+ group[1].__len__()
    return count * 1000000-int(nerv)+(totalgates - gate_plane_group.__len__() )*1,nerv,totalgates-gate_plane_group.__len__(),failList

