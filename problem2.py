import extractExcel
import numpy as np
import time
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
##################预处理ticket######################################
import itertools
tickets_matrix_array = np.asarray(tickets_matrix)
pucks_matrix_array = np.asarray(pucks_matrix)
pucks_join_tickets = []
# 做笛卡尔积

tickets_final_matrix = []
# print(tickets_matrix.__len__())
#找到需要考虑的飞机班次
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
        if(ticket[3] == float(puck_consider[1]) and ticket[2] == puck_consider[3]):
            flag1 = True
            break
    for puck_consider in pucks_consider:
        if ticket[5] == float(puck_consider[6]) and ticket[4] == puck_consider[8]:
            flag2 = True
            break
    if flag1 and flag2 :
        tickets_final_matrix.append(ticket)
# print(tickets_final_matrix.__len__())
tickets_final_matrix = np.asarray(tickets_final_matrix)
pucks_consider = np.asarray(pucks_consider)
for x in itertools.product(pucks_consider,tickets_final_matrix ):
    y = list(x[0]) + list(x[1])
    pucks_join_tickets.append(y)
#找到某个降落飞机中有哪些乘客
#找到某个起飞飞机中有哪些乘客
arriving_pucks_tickets = []
leaving_pucks_tickets = []
arriving_pucks_tickets_leaving_tickets = []
#不同天有相同班次的飞机
for puck_join_ticket in pucks_join_tickets:
    if(puck_join_ticket[3] == puck_join_ticket[14] and puck_join_ticket[1] == puck_join_ticket[15] ):
        arriving_pucks_tickets.append(puck_join_ticket)
    if(puck_join_ticket[8] == puck_join_ticket[16] and puck_join_ticket[6] == puck_join_ticket[17]):
        leaving_pucks_tickets.append(puck_join_ticket)
for arriving_puck_ticket in arriving_pucks_tickets:
    for leaving_puck_ticket in leaving_pucks_tickets:
        if (arriving_puck_ticket[12] == leaving_puck_ticket[12]):
            arriving_pucks_tickets_leaving_tickets.append(arriving_puck_ticket+leaving_puck_ticket)
            break
# result = list(filter(lambda a : a[4] == 'I' and a[27] =='I'  ,arriving_pucks_tickets_leaving_tickets))
# print(result.__len__())
# result = list(filter(lambda a : a[4] == 'I' and a[27] =='D'  ,arriving_pucks_tickets_leaving_tickets))
# print(result.__len__())
# result = list(filter(lambda a : a[4] == 'D' and a[27] =='I'  ,arriving_pucks_tickets_leaving_tickets))
# print(result.__len__())
# result = list(filter(lambda a : a[4] == 'D' and a[27] =='D'  ,arriving_pucks_tickets_leaving_tickets))
# print(result.__len__())

def generateFormula():
    #设航站楼为0,卫星厅为1
    dicFormula = {}
    i = 1
    string ="0"
    for arriving_puck_ticket_leaving_ticket in arriving_pucks_tickets_leaving_tickets:
        if not dicFormula.__contains__(arriving_puck_ticket_leaving_ticket[0]):
            dicFormula[arriving_puck_ticket_leaving_ticket[0]] = i
            i = i + 1
        if not dicFormula.__contains__(arriving_puck_ticket_leaving_ticket[18]):
            dicFormula[arriving_puck_ticket_leaving_ticket[18]] = i
            i = i + 1
    for a in arriving_pucks_tickets_leaving_tickets:
        if a[4] == 'I' and a[27] == 'I':
            string =string+"+("+"x"+str(dicFormula[a[0]])+"*x"+str(dicFormula[a[18]])+"*"+"20"
            string =string+"+"+"(1-x"+str(dicFormula[a[0]])+")*x"+str(dicFormula[a[18]])+"*"+"30"
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "30"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "20)"
            string =string +"*"+str(a[13])
        if a[4] == 'I' and a[27] == 'D':
            string = string + "+(" + "x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "350"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "40"
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "40"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "45)"
            string = string + "*" + str(a[13])
        if a[4] == 'D' and a[27] == 'I':
            string = string + "+" + "(x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "35"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "40"
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "40"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "35)"
            string = string + "*" + str(a[13])
        if a[4] == 'D' and a[27] == 'D':
            string = string + "+" + "(x" + str(dicFormula[a[0]]) + "*x" + str(dicFormula[a[18]]) + "*" + "15"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*x" + str(dicFormula[a[18]]) + "*" + "20"
            string = string + "+" + "x" + str(dicFormula[a[0]]) + "*(1-x" + str(dicFormula[a[18]]) + ")*" + "20"
            string = string + "+" + "(1-x" + str(dicFormula[a[0]]) + ")*(1-x" + str(dicFormula[a[18]]) + ")*" + "15)"
            string = string + "*" + str(a[13])
    print("min="+string+";")
    for value in dicFormula.values():
        print("@bin(x"+str(value)+");")
    return string
string=generateFormula()


####根据排队论+流水线处理第一问并画图
#飞机型号对应登机门，并针对不同问题画图
def plane_gate(planes,gatesList,arriving_puck_ticket,leaving_puck_ticket):
    gatesTime = np.zeros( gatesList.__len__() )
    planeFlag = np.zeros(planes.__len__())
    resultGate = []
    resultArriveTime = []
    resultLeaveTime = []
    for i in range( planes.__len__() ):
        flag = 0
        gateNum = 0       #记录选择的gate的number
        bestWeight = -1    #记录优先权
        for j in range( gatesTime.__len__() ):
            if planes[i][1]*24*60 + planes[i][2] >= gatesTime[j]:
                #登机口独占 动态优先权算法
                flag = 1    #找到至少一个
                if bestWeight < gatesTime[j]:   #比较有限权
                    bestWeight = gatesTime[j]
                    # gatesTime[j] = planes[i][6] * 24 * 60 + planes[i][7] + 45
                    gateNum = j

        planeFlag[i] = flag
        if flag == 1:
            gatesTime[gateNum] = planes[i][6] * 24 * 60 + planes[i][7] + 45
            resultArriveTime.append( planes[i][1]*24*60 + planes[i][2] )
            resultLeaveTime.append(planes[i][6]*24*60 + planes[i][7])
            resultGate.append( gatesList[gateNum][0] )
        else:
            resultArriveTime.append( -1 )
            resultLeaveTime.append( -1 )
            resultGate.append( 'fail')
    return planeFlag,resultGate,resultArriveTime,resultLeaveTime

#用于分析时间，参数选择停靠的登机口序列和对应飞机序列
def analyseTime(gates,planes):
    pass
planeFlag,resultGate,resultArriveTime,resultLeaveTime=plane_gate(ID_N_pucks_matrix_sorted,D_DI_N_gates,arriving_pucks_tickets,leaving_pucks_tickets)
print(planeFlag)
print(  ( np.asarray(resultArriveTime,dtype= np.float)  ) )
print(  ( np.asarray(resultLeaveTime,dtype= np.float)  ) )
print( np.asarray(resultGate) )







