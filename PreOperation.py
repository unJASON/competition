import numpy as np
import extractExcel
def PreOperation_Gates(path):
    gates, gates_matrix = extractExcel.extractGate(path)
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
    return I_I_N_gates,I_I_W_gates,I_DI_W_gates,D_D_N_gates,\
           D_D_W_gates,D_DI_N_gates,DI_DI_W_gates,DI_DI_N_gates,DI_D_N_gates,DI_I_W_gates
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
W_type = ['332', '333', '33E', '33H', '33L','773']
N_type = ['319', '320', '321', '323', '325', '738', '73A', '73E', '73H', '73L']
def PreOperation_Pucks(path):
    # pucks分组
    pucks, pucks_matrix = extractExcel.extractPuck(path)
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
    # 按照时间顺序排列
    DI_W_pucks_matrix_sorted = sorted(DI_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
    DI_N_pucks_matrix_sorted = sorted(DI_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)

    ID_W_pucks_matrix_sorted = sorted(ID_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
    ID_N_pucks_matrix_sorted = sorted(ID_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)

    DD_W_pucks_matrix_sorted = sorted(DD_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
    DD_N_pucks_matrix_sorted = sorted(DD_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)

    II_W_pucks_matrix_sorted = sorted(II_W_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
    II_N_pucks_matrix_sorted = sorted(II_N_pucks_matrix, key=lambda ele: ele[1] + ele[2] / 24 / 60)
    return DI_W_pucks_matrix_sorted,DI_N_pucks_matrix_sorted,ID_W_pucks_matrix_sorted,ID_N_pucks_matrix_sorted,\
           DD_W_pucks_matrix_sorted,DD_N_pucks_matrix_sorted,II_W_pucks_matrix_sorted,II_N_pucks_matrix_sorted