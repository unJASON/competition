import extractExcel
import numpy as np
import time
import SolvingProblem


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
W_type = ['332', '333', '33E', '33H', '33L', '773']
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
# 将matrix 中的飞机型号转出string
for i in pucks_matrix:
    if not isinstance(i[5], str):
        i[5] = str(int(i[5]))

for i in range(pucks_matrix.__len__()):
    if (pucks_matrix[i][4] == 'D' and pucks_matrix[i][9] == 'I'
            and (pucks_matrix[i][1] == 43120 or pucks_matrix[i][6] == 43120)):
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

# 按照时间顺序排列
DI_W_pucks_matrix_sorted = sorted(DI_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
DI_N_pucks_matrix_sorted = sorted(DI_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)

ID_W_pucks_matrix_sorted = sorted(ID_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
ID_N_pucks_matrix_sorted = sorted(ID_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)

DD_W_pucks_matrix_sorted = sorted(DD_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
DD_N_pucks_matrix_sorted = sorted(DD_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)

II_W_pucks_matrix_sorted = sorted(II_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
II_N_pucks_matrix_sorted = sorted(II_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
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

I_I_N_gates = []  # 4
I_I_W_gates = []  # 17
I_DI_W_gates = []  # 1

D_D_N_gates = []  # 35
D_D_W_gates = []  # 2
D_DI_N_gates = []  # 2

DI_DI_W_gates = []  # 3
DI_DI_N_gates = []  # 2
DI_D_N_gates = []  # 2
DI_I_W_gates = []  # 1

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
##################预处理gate结束####################################
##################预处理ticket######################################
import itertools

tickets_matrix_array = np.asarray(tickets_matrix)
pucks_matrix_array = np.asarray(pucks_matrix)
pucks_join_tickets = []
# 做笛卡尔积

tickets_final_matrix = []
# print(tickets_matrix.__len__())
# 找到需要考虑的飞机班次
pucks_consider = []
for puck in pucks_matrix_array:
    if float(puck[1]) == 43120.0 or float(puck[6]) == 43120.0:
        pucks_consider.append(puck)
pucks_consider = np.asarray(pucks_consider)
for ticket in tickets_matrix:
    # 过滤到达时间和出发时间 都不在20号的  找不到对应飞机信息的
    flag1 = False
    flag2 = False
    for puck_consider in pucks_consider:
        if (ticket[3] == float(puck_consider[1]) and ticket[2] == puck_consider[3]):
            flag1 = True
            break
    for puck_consider in pucks_consider:
        if ticket[5] == float(puck_consider[6]) and ticket[4] == puck_consider[8]:
            flag2 = True
            break
    if flag1 and flag2:
        tickets_final_matrix.append(ticket)
# print(tickets_final_matrix.__len__())
tickets_final_matrix = np.asarray(tickets_final_matrix)
pucks_consider = np.asarray(pucks_consider)
for x in itertools.product(pucks_consider, tickets_final_matrix):
    y = list(x[0]) + list(x[1])
    pucks_join_tickets.append(y)
# 找到某个降落飞机中有哪些乘客
# 找到某个起飞飞机中有哪些乘客
arriving_pucks_tickets = []
leaving_pucks_tickets = []
arriving_pucks_tickets_leaving_pucks = []
# 不同天有相同班次的飞机
for puck_join_ticket in pucks_join_tickets:
    if (puck_join_ticket[3] == puck_join_ticket[14] and puck_join_ticket[1] == puck_join_ticket[15]):
        arriving_pucks_tickets.append(puck_join_ticket)
    if (puck_join_ticket[8] == puck_join_ticket[16] and puck_join_ticket[6] == puck_join_ticket[17]):
        leaving_pucks_tickets.append(puck_join_ticket)
for arriving_puck_ticket in arriving_pucks_tickets:
    for leaving_puck_ticket in leaving_pucks_tickets:
        if (arriving_puck_ticket[12] == leaving_puck_ticket[12]):
            arriving_pucks_tickets_leaving_pucks.append(arriving_puck_ticket + leaving_puck_ticket)
            break


def generateFormula_problem3():
    # 设航站楼T为0,卫星厅S为1,引入其他决策变量y0-y6
    dicFormula = {}
    dicFormulaReverse = {}
    i = 0
    string = "0"
    walking_weight = [10,15,20,25,20,25,25,
                      15,10,15,20,15,20,20,
                      20,15,10,25,20,25,25,
                      20,20,25,10,15,20,20,
                      25,15,20,15,10,15,15,
                      25,20,25,20,15,10,20,
                      25,20,25,20,15,20,10]
    walking_weight = np.asarray(walking_weight,dtype=np.int).reshape((7,7))
    for arriving_puck_ticket_leaving_ticket in arriving_pucks_tickets_leaving_pucks:
        if not dicFormula.__contains__(arriving_puck_ticket_leaving_ticket[0]):
            dicFormula[arriving_puck_ticket_leaving_ticket[0]] = i
            dicFormulaReverse[i] = arriving_puck_ticket_leaving_ticket[0]
            i = i + 1
        if not dicFormula.__contains__(arriving_puck_ticket_leaving_ticket[18]):
            dicFormula[arriving_puck_ticket_leaving_ticket[18]] = i
            dicFormulaReverse[i] = arriving_puck_ticket_leaving_ticket[0]
            i = i + 1
    for a in arriving_pucks_tickets_leaving_pucks:
        if a[4] == 'I' and a[27] == 'I':
            # 1 1
            string = string + "+(" + "x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "20"
            # 0 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "38"
            # 1 0
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "38"
            # 0 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "20+"+print_matrix(dicFormula[a[0]],dicFormula[a[18]],walking_weight)+")"

        if a[4] == 'I' and a[27] == 'D':
            # 1 1
            string = string + "+(" + "x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "61"
            # 0 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "48"
            # 1 0
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "48"
            # 0 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "35+"+print_matrix(dicFormula[a[0]],dicFormula[a[18]],walking_weight)+")"
        if a[4] == 'D' and a[27] == 'I':
            # 1 1
            string = string + "+" + "(x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "35"
            # 1 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "48"
            # 0 1
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "48"
            # 0 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "35+"+print_matrix(dicFormula[a[0]],dicFormula[a[18]],walking_weight)+")"

        if a[4] == 'D' and a[27] == 'D':
            # 1 1
            string = string + "+" + "(x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "15"
            # 0 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "28"
            # 1 0
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "28"
            # 1 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "15+"+print_matrix(dicFormula[a[0]],dicFormula[a[18]],walking_weight)+")"
        string = string + "*" + str(a[13])+"/"+str(float(a[24])*24*60+float(a[25])-float(a[1])*24*60-float(a[2]))

    import sys
    from  Logger import Logger
    sys.stdout = Logger("1.txt")  # 保存
    print("Model:")
    print("min=" + string + ";")
    for value in dicFormula.values():
        print("(1-x"+str(value)+")*("+"x"+str(value)+"_0+"+"x"+str(value)+"_1+"+"x"+str(value)+"_2)+x"+str(value)+"*("+"x"+str(value)+"_3+"+"x"+str(value)+"_4+"+"x"+str(value)+"_5+"+"x"+str(value)+"_6) = 1;" )
    for value in dicFormula.values():
        print("@bin(x" + str(value) + ");")
        print("@bin(x" + str(value) + "_0" + ");")
        print("@bin(x" + str(value) + "_1" + ");")
        print("@bin(x" + str(value) + "_2" + ");")
        print("@bin(x" + str(value) + "_3" + ");")
        print("@bin(x" + str(value) + "_4" + ");")
        print("@bin(x" + str(value) + "_5" + ");")
        print("@bin(x" + str(value) + "_6" + ");")
    print("end")

    return dicFormula, dicFormulaReverse
def print_matrix(arriving_number,leaving_number,walking_weight):
    #11SS
    arriving_number = str(arriving_number)
    leaving_number = str(leaving_number)
    #4*4
    string = "x"+arriving_number+"*"+"x"+leaving_number+"*("+"x"+arriving_number+"_3*x"+leaving_number+"_3*"+str(walking_weight[3][3])+\
                                                            "+x"+arriving_number+"_3*x"+leaving_number+"_4*"+str(walking_weight[3][4])+\
                                                            "+x"+arriving_number+"_3*x"+leaving_number+"_5*"+str(walking_weight[3][5])+\
                                                            "+x"+arriving_number+"_3*x"+leaving_number+"_6*"+str(walking_weight[3][6])+\
                                                            "+x"+arriving_number+"_4*x"+leaving_number+"_3*"+str(walking_weight[4][3])+\
                                                            "+x"+arriving_number+"_4*x"+leaving_number+"_4*"+str(walking_weight[4][4])+\
                                                            "+x"+arriving_number+"_4*x"+leaving_number+"_5*"+str(walking_weight[4][5])+\
                                                            "+x"+arriving_number+"_4*x"+leaving_number+"_6*"+str(walking_weight[4][6])+\
                                                            "+x"+arriving_number+"_5*x"+leaving_number+"_3*"+str(walking_weight[5][3])+\
                                                            "+x"+arriving_number+"_5*x"+leaving_number+"_4*"+str(walking_weight[5][4])+\
                                                            "+x"+arriving_number+"_5*x"+leaving_number+"_5*"+str(walking_weight[5][5])+\
                                                            "+x"+arriving_number+"_5*x"+leaving_number+"_6*"+str(walking_weight[5][6])+\
                                                            "+x"+arriving_number+"_6*x"+leaving_number+"_3*"+str(walking_weight[6][3])+\
                                                            "+x"+arriving_number+"_6*x"+leaving_number+"_4*"+str(walking_weight[6][4])+\
                                                            "+x"+arriving_number+"_6*x"+leaving_number+"_5*"+str(walking_weight[6][5])+\
                                                            "+x"+arriving_number+"_6*x"+leaving_number+"_6*"+str(walking_weight[6][6])+")"

    #01 TS 3*4
    string = string + "+(1-x"+arriving_number+")*"+"x"+leaving_number+"*("\
                                                            +"x"+arriving_number+"_0*x"+leaving_number+"_3*"+str(walking_weight[0][3])+\
                                                            "+x"+arriving_number+"_0*x"+leaving_number+"_4*"+str(walking_weight[0][4])+\
                                                            "+x"+arriving_number+"_0*x"+leaving_number+"_5*"+str(walking_weight[0][5])+\
                                                            "+x"+arriving_number+"_0*x"+leaving_number+"_6*"+str(walking_weight[0][6])+\
                                                            "+x"+arriving_number+"_1*x"+leaving_number+"_3*"+str(walking_weight[1][3])+\
                                                            "+x"+arriving_number+"_1*x"+leaving_number+"_4*"+str(walking_weight[1][4])+\
                                                            "+x"+arriving_number+"_1*x"+leaving_number+"_5*"+str(walking_weight[1][5])+\
                                                            "+x"+arriving_number+"_1*x"+leaving_number+"_6*"+str(walking_weight[1][6])+\
                                                            "+x"+arriving_number+"_2*x"+leaving_number+"_3*"+str(walking_weight[2][3])+\
                                                            "+x"+arriving_number+"_2*x"+leaving_number+"_4*"+str(walking_weight[2][4])+\
                                                            "+x"+arriving_number+"_2*x"+leaving_number+"_5*"+str(walking_weight[2][5])+\
                                                            "+x"+arriving_number+"_2*x"+leaving_number+"_6*"+str(walking_weight[2][6])+")"

    #10ST 4*3
    string = string +"+x"+arriving_number+"*"+"(1-x"+leaving_number+")*(" \
                                                             +"x" + arriving_number + "_3*x" + leaving_number + "_0*" + str(walking_weight[3][0]) + \
                                                             "+x" + arriving_number + "_3*x" + leaving_number + "_1*" + str(walking_weight[3][1]) + \
                                                             "+x" + arriving_number + "_3*x" + leaving_number + "_2*" + str(walking_weight[3][2]) + \
                                                             "+x" + arriving_number + "_4*x" + leaving_number + "_0*" + str(walking_weight[4][0]) + \
                                                             "+x" + arriving_number + "_4*x" + leaving_number + "_1*" + str(walking_weight[4][1]) + \
                                                             "+x" + arriving_number + "_4*x" + leaving_number + "_2*" + str(walking_weight[4][2]) + \
                                                             "+x" + arriving_number + "_5*x" + leaving_number + "_0*" + str(walking_weight[5][0]) + \
                                                             "+x" + arriving_number + "_5*x" + leaving_number + "_1*" + str(walking_weight[5][1]) + \
                                                             "+x" + arriving_number + "_5*x" + leaving_number + "_2*" + str(walking_weight[5][2]) + \
                                                             "+x" + arriving_number + "_6*x" + leaving_number + "_0*" + str(walking_weight[6][0]) + \
                                                             "+x" + arriving_number + "_6*x" + leaving_number + "_1*" + str(walking_weight[6][1]) + \
                                                             "+x" + arriving_number + "_6*x" + leaving_number + "_2*" + str(walking_weight[6][2]) + ")"
    #00TT 3*3
    string = string + "+(1-x"+arriving_number+")*"+"(1-x"+leaving_number+")*(" \
                                                             +"x" + arriving_number + "_0*x" + leaving_number + "_0*" + str(walking_weight[0][0]) + \
                                                             "+x" + arriving_number + "_0*x" + leaving_number + "_1*" + str(walking_weight[0][1]) + \
                                                             "+x" + arriving_number + "_0*x" + leaving_number + "_2*" + str(walking_weight[0][2]) + \
                                                             "+x" + arriving_number + "_1*x" + leaving_number + "_0*" + str(walking_weight[1][0]) + \
                                                             "+x" + arriving_number + "_1*x" + leaving_number + "_1*" + str(walking_weight[1][1]) + \
                                                             "+x" + arriving_number + "_1*x" + leaving_number + "_2*" + str(walking_weight[1][2]) + \
                                                             "+x" + arriving_number + "_2*x" + leaving_number + "_0*" + str(walking_weight[2][0]) + \
                                                             "+x" + arriving_number + "_2*x" + leaving_number + "_1*" + str(walking_weight[2][1]) + \
                                                             "+x" + arriving_number + "_2*x" + leaving_number + "_2*" + str(walking_weight[2][2]) + ")"
    return string


# 跑一次就够了
dicFormula, dicFormulaReverse = generateFormula_problem3()

# 抽出最优解
# 设航站楼为0,卫星厅为1
answers = extractExcel.extractFile('answer2.xlsx')
for i in range(answers.__len__()):
    answers[i][0] = answers[i][0][1:]
# 用于分析时间，参数选择停靠的登机口序列和对应飞机序列

def generateAllInfo(plane_gate_mapper, dicFormula, dicFormulaReverse, answers):
    plane_situation = []
    for i in range(plane_gate_mapper.__len__()):
        planeFlag, planeBestFlag, resultGate, resultArriveTime, resultLeaveTime = SolvingProblem.problem2_plane_gate(
            plane_gate_mapper[i][0],
            plane_gate_mapper[i][1], dicFormula,
            dicFormulaReverse,
            answers)
        for j in range(planeBestFlag.size):
            plane_situation.append([plane_gate_mapper[i][0][j][0], planeFlag[j], planeBestFlag[j], resultGate[j]])
    return plane_situation

plane_gate_mapper =[]
plane_gate_mapper.append([DD_N_pucks_matrix_sorted,D_D_N_gates])
plane_gate_mapper.append([II_W_pucks_matrix_sorted,I_I_W_gates])
plane_gate_mapper.append([II_N_pucks_matrix_sorted,I_I_N_gates])
plane_gate_mapper.append([DI_W_pucks_matrix_sorted,DI_I_W_gates+DI_DI_W_gates[1:3]])
plane_gate_mapper.append([ID_W_pucks_matrix_sorted,I_DI_W_gates+DI_DI_W_gates[0:1]])
plane_gate_mapper.append([ID_N_pucks_matrix_sorted,DI_D_N_gates+DI_DI_N_gates[1:2]])
plane_gate_mapper.append([DI_N_pucks_matrix_sorted,D_DI_N_gates+DI_DI_N_gates[0:1]])
plane_situation = generateAllInfo(plane_gate_mapper,dicFormula,dicFormulaReverse,answers)
countSuc = 0
countFail = 0
sum = 0
time = 0    #总花费时间
ti_situation = []
for ti in arriving_pucks_tickets_leaving_pucks:
    sum = sum + float(ti[13])
    for plane_si in plane_situation:
        if str(plane_si[0]) == str(ti[0]) :
            if plane_si[1] == 1:
                countSuc = countSuc + float(ti[13])
                ti_situation.append([ti,True])
            else:
                ti_situation.append([ti,False])
                countFail = countFail+ float(ti[13])
walking_weight =     [10,15,20,25,20,25,25,
                      15,10,15,20,15,20,20,
                      20,15,10,25,20,25,25,
                      20,20,25,10,15,20,20,
                      25,15,20,15,10,15,15,
                      25,20,25,20,15,10,20,
                      25,20,25,20,15,20,10]
walking_weight = np.asarray(walking_weight,dtype=np.float).reshape((7,7))
dictionary_time={}
dictionary_density = np.zeros(11)

for ti in ti_situation:
    if ti[1] :
        for plane_si in plane_situation:
            if str(plane_si[0]) == str(ti[0][0]):
                for gate in gates_matrix:
                    if gate[0] == plane_si[3]:
                        come_gate = gate[1]
                        com_dir = -1
                        if come_gate == 'S':
                            if gate[2] == "North":
                                com_dir = 3
                            elif gate[2] == "Center":
                                com_dir =4
                            elif gate[2] == "South":
                                com_dir = 5
                            else:
                                com_dir = 6
                        else:
                            if gate[2] == "North":
                                com_dir = 0
                            elif gate[2] == "Center":
                                com_dir = 1
                            else:
                                com_dir = 2
            if str(plane_si[0] == str(ti[0][18])):
                for gate in gates_matrix:
                    if gate[0] == plane_si[3]:
                        go_gate = gate[1]
                        go_dir = -1
                        if go_gate == 'S':
                            if gate[2] == "North":
                                go_dir = 3
                            elif gate[2] == "Center":
                                go_dir =4
                            elif gate[2] == "South":
                                go_dir = 5
                            else:
                                go_dir = 6
                        else:
                            if gate[2] == "North":
                                go_dir = 0
                            elif gate[2] == "Center":
                                go_dir = 1
                            else:
                                go_dir = 2
        if come_gate == 'S' and go_gate == 'T' and ti[0][4] == 'I' and ti[0][27] == 'I':
            value = (30+ walking_weight[com_dir][go_dir]+8)/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))
        if come_gate == 'S' and go_gate == 'T' and ti[0][4] == 'I' and ti[0][27] == 'D':
            value =(40 + walking_weight[com_dir][go_dir] + 8) / (float(ti[0][24]) * 24 * 60 + float(ti[0][25]) - float(ti[0][1]) * 24 * 60 - float(ti[0][2]))
        if come_gate == 'S' and go_gate == 'T' and ti[0][4] == 'D' and ti[0][27] == 'I':
            value = (40+ walking_weight[com_dir][go_dir]+8)/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))
        if come_gate == 'S' and go_gate == 'T' and ti[0][4] == 'D' and ti[0][27] == 'D':
            value = (20 + walking_weight[com_dir][go_dir] + 8) / (
                        float(ti[0][24]) * 24 * 60 + float(ti[0][25]) - float(ti[0][1]) * 24 * 60 - float(ti[0][2]))


        if come_gate == 'S' and go_gate == 'S' and ti[0][4] == 'I' and ti[0][27] == 'I':
            value =(20+ walking_weight[com_dir][go_dir])/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))

        if come_gate == 'S' and go_gate == 'S' and ti[0][4] == 'I' and ti[0][27] == 'D':
            value =(45 + walking_weight[com_dir][go_dir] + 16) / (
                        float(ti[0][24]) * 24 * 60 + float(ti[0][25]) - float(ti[0][1]) * 24 * 60 - float(ti[0][2]))
        if come_gate == 'S' and go_gate == 'S' and ti[0][4] == 'D' and ti[0][27] == 'I':
            value = (35+ walking_weight[com_dir][go_dir])/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))

        if come_gate == 'S' and go_gate == 'S' and ti[0][4] == 'D' and ti[0][27] == 'D':
            value =(15+ walking_weight[com_dir][go_dir])/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))



        if come_gate == 'T' and go_gate == 'T' and ti[0][4] == 'I' and ti[0][27] == 'I':
            value =(20+ walking_weight[com_dir][go_dir])/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))

        if come_gate == 'T' and go_gate == 'T' and ti[0][4] == 'I' and ti[0][27] == 'D':
            value=(35 + walking_weight[com_dir][go_dir]) / (
                        float(ti[0][24]) * 24 * 60 + float(ti[0][25]) - float(ti[0][1]) * 24 * 60 - float(ti[0][2]))

        if come_gate == 'T' and go_gate == 'T' and ti[0][4] == 'D' and ti[0][27] == 'I':
            value =(35 + walking_weight[com_dir][go_dir]) / (
                        float(ti[0][24]) * 24 * 60 + float(ti[0][25]) - float(ti[0][1]) * 24 * 60 - float(ti[0][2]))

        if come_gate == 'T' and go_gate == 'T' and ti[0][4] == 'D' and ti[0][27] == 'D':
            value = (15+ walking_weight[com_dir][go_dir])/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))



        if come_gate == 'T' and go_gate == 'S' and ti[4] == 'I' and ti[27] == 'I':
            value =(30+ walking_weight[com_dir][go_dir]+8)/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))

        if come_gate == 'T' and go_gate == 'S' and ti[4] == 'I' and ti[27] == 'D':
            value =(40+ walking_weight[com_dir][go_dir]+8)/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))

        if come_gate == 'T' and go_gate == 'S' and ti[4] == 'D' and ti[27] == 'I':
            value =(40 + walking_weight[com_dir][go_dir] + 8) / (
                        float(ti[0][24]) * 24 * 60 + float(ti[0][25]) - float(ti[0][1]) * 24 * 60 - float(ti[0][2]))

        if come_gate == 'T' and go_gate == 'S' and ti[4] == 'D' and ti[27] == 'D':
            value =(20+ walking_weight[com_dir][go_dir]+8)/(float(ti[0][24])*24*60+float(ti[0][25])-float(ti[0][1])*24*60-float(ti[0][2]))
        time = time + float(ti[0][13]) * value

        if value<0.1:
            dictionary_density[0] = dictionary_density[0] +float(ti[0][13])
        elif value<0.2:
            dictionary_density[1] = dictionary_density[1] + float(ti[0][13])
        elif value < 0.3:
            dictionary_density[2] = dictionary_density[2] + float(ti[0][13])
        elif value < 0.4:
            dictionary_density[3] = dictionary_density[3] + float(ti[0][13])
        elif value < 0.5:
            dictionary_density[4] = dictionary_density[4] + float(ti[0][13])
        elif value < 0.6:
            dictionary_density[5] = dictionary_density[5] + float(ti[0][13])
        elif value < 0.7:
            dictionary_density[6] = dictionary_density[6] + float(ti[0][13])
        elif value < 0.8:
            dictionary_density[7] = dictionary_density[7] + float(ti[0][13])
        elif value < 0.9:
            dictionary_density[8] = dictionary_density[8] + float(ti[0][13])
        elif value < 1.0:
            dictionary_density[9] = dictionary_density[9] + float(ti[0][13])
        else:
            dictionary_density[10] = dictionary_density[10] + float(ti[0][13])
print(countSuc,countFail,sum,time )

# print(planeFlag.sum())
# print(planeFlag)
# print(planeBestFlag.sum())
# print(planeBestFlag)



#设计找到多个最优解导出使用lingo
def generateFormulaCheck(answers):
    # 设航站楼T为0,卫星厅S为1
    dicFormula = {}
    dicFormulaReverse = {}
    i = 0
    string = "0"
    for arriving_puck_ticket_leaving_ticket in arriving_pucks_tickets_leaving_pucks:
        if not dicFormula.__contains__(arriving_puck_ticket_leaving_ticket[0]):
            dicFormula[arriving_puck_ticket_leaving_ticket[0]] = i
            dicFormulaReverse[i] = arriving_puck_ticket_leaving_ticket[0]
            i = i + 1
        if not dicFormula.__contains__(arriving_puck_ticket_leaving_ticket[18]):
            dicFormula[arriving_puck_ticket_leaving_ticket[18]] = i
            dicFormulaReverse[i] = arriving_puck_ticket_leaving_ticket[0]
            i = i + 1
    for a in arriving_pucks_tickets_leaving_pucks:
        if a[4] == 'I' and a[27] == 'I':
            # 1 1
            string = string + "+(" + "x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "20"
            # 0 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "30"
            # 1 0
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "30"
            # 0 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "20)"
            string = string + "*" + str(a[13])
        if a[4] == 'I' and a[27] == 'D':
            # 1 1
            string = string + "+(" + "x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "45"
            # 0 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "40"
            # 1 0
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "40"
            # 0 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "35)"
            string = string + "*" + str(a[13])
        if a[4] == 'D' and a[27] == 'I':
            # 1 1
            string = string + "+" + "(x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "35"
            # 1 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "40"
            # 0 1
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "40"
            # 0 0
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "35)"
            string = string + "*" + str(a[13])
        if a[4] == 'D' and a[27] == 'D':
            # 1 1
            string = string + "+" + "(x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "15"
            # 0 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "20"
            # 1 0
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "20"
            # 1 1
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "15)"
            string = string + "*" + str(a[13])
    print("Model:")
    print("min=" + string + ";")
    for value in dicFormula.values():
        print("!x" + str(value) + "="+str(answers[value]*0+(1-answers[value])*1)+";")
    for value in dicFormula.values():
        print("@bin(x" + str(value) + ");")
    print("end")
#多找几个最优解
# generateFormulaCheck(answers)





