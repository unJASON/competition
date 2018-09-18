import extractExcel
import numpy as np
import plotProblem
import PreOperation
import SolvingProblem
def printListAsMatrix(list):
    print(list.__len__())
    for i in list:
        print(i)
    print("\n")
    return
path = 'InputData.xlsx'

tickets, tickets_matrix = extractExcel.extractTicket(path)
pucks, pucks_matrix = extractExcel.extractPuck(path)
DI_W_pucks_matrix_sorted, DI_N_pucks_matrix_sorted, ID_W_pucks_matrix_sorted, ID_N_pucks_matrix_sorted, \
DD_W_pucks_matrix_sorted, DD_N_pucks_matrix_sorted, II_W_pucks_matrix_sorted, II_N_pucks_matrix_sorted= PreOperation.PreOperation_Pucks(path)

###############预处理GATE################################
I_I_N_gates,I_I_W_gates,I_DI_W_gates,D_D_N_gates,\
D_D_W_gates,D_DI_N_gates,DI_DI_W_gates,DI_DI_N_gates,DI_D_N_gates,DI_I_W_gates = PreOperation.PreOperation_Gates(path)
##################预处理gate结束####################################
####根据排队论+流水线处理第一问并画图
planeFlag, resultGate, resultArriveTime, resultLeaveTime = SolvingProblem.solveProblem_1(DD_N_pucks_matrix_sorted,D_D_N_gates)




