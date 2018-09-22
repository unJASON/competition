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
import xlwt
import xlrd
from xlutils.copy import copy
plane_gate_mapper =[]
plane_gate_mapper.append([DD_N_pucks_matrix_sorted,D_D_N_gates])
plane_gate_mapper.append([II_W_pucks_matrix_sorted,I_I_W_gates])
plane_gate_mapper.append([II_N_pucks_matrix_sorted,I_I_N_gates])
plane_gate_mapper.append([DI_W_pucks_matrix_sorted,DI_I_W_gates+DI_DI_W_gates[1:3]])
plane_gate_mapper.append([ID_W_pucks_matrix_sorted,I_DI_W_gates+DI_DI_W_gates[0:1]])
plane_gate_mapper.append([ID_N_pucks_matrix_sorted,DI_D_N_gates+DI_DI_N_gates[1:2]])
plane_gate_mapper.append([DI_N_pucks_matrix_sorted,D_DI_N_gates+DI_DI_N_gates[0:1]])
def generateAllInfo(plane_gate_mapper):
    plane_situation = []
    workbook = xlrd.open_workbook(path)
    new_excel = copy(workbook)
    for i in range(plane_gate_mapper.__len__()):
        planeFlag, resultGate, resultArriveTime, resultLeaveTime = SolvingProblem.solveProblem_1(
            plane_gate_mapper[i][0],
            plane_gate_mapper[i][1])
        ws = new_excel.get_sheet(0)
        sheet = workbook.sheet_by_index(0)
        for ii in range(plane_gate_mapper[i][0].__len__()):
            for j in range(workbook.sheet_by_index(0).nrows):
                if sheet.cell(j, 0).value == plane_gate_mapper[i][0][ii][0]:
                    ws.write(j, 12, resultGate[ii])
    new_excel.save('new_file.csv', )
    return plane_situation

generateAllInfo(plane_gate_mapper)



