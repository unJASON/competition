import numpy as np
import xlrd
import xlwt
from Gate import Gate
from Ticket import Ticket
from Puck import Puck
from xlrd import xldate_as_tuple
import itertools

def extractGate(path):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name('Gates')
    gates = []
    gates_matrix = []
    for i in range(sheet.nrows):
        if i != 0:
            data = sheet.row_values(i)
            gate = Gate(data[0],data[1],data[2],data[3],data[4],data[5])
            gates.append(gate)
            gates_matrix.append(data)

    return gates,gates_matrix

def extractTicket(path):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name('Tickets')
    tickets = []
    tickets_matrix = []
    for i in range(sheet.nrows):
        if i != 0:
            data = sheet.row_values(i)
            ticket = Ticket(data[0],data[1],data[2],data[3],data[4],data[5])
            tickets.append(ticket)
            tickets_matrix.append(data)
    return tickets,tickets_matrix
def extractPuck(path):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name('Pucks')
    pucks=[]
    pucks_matrix=[]
    for i in range(sheet.nrows):
        if i != 0:
            # data = sheet.row_values(i)
            # arrive date 为0，1 ，2分别为2018/1/19, 2018/1/20, 2018/1/21
            # print(data)
            data = []
            for j in range(sheet.ncols):
                if (j == 2 or j == 7) and sheet.cell(i,j).ctype == 3:
                    date =  xldate_as_tuple(sheet.cell(i,j).value, 0)
                    data.append(float (date[3]*60+date[4]) )
                else:
                    data.append( sheet.cell(i,j).value )
            if isinstance(data[7], str):
                stri = data[7].split(':')
                flt = 0
                if (stri[0][0] == ' '):
                    flt = float(stri[0][1])*60
                else:
                    flt = float(stri[0])*60
                if (stri[1][0] == ' '):
                    flt = flt + float(stri[1][1])
                else:
                    flt = flt + float(stri[1])
                data[7] = flt
            if isinstance(data[2], str):
                stri = data[2].split(':')
                flt = 0
                if (stri[0][0] == ' '):
                    flt = float(stri[0][1])*60
                else:
                    flt = float(stri[0])*60
                if (stri[1][0] == ' '):
                    flt = flt + float(stri[1][1])
                else:
                    flt = flt + float(stri[1])
                data[2] = flt
            # print(data)
            puck = Puck(data[0], int(data[1]) - 43119, data[2] , (int(data[1]) - 43119) * 24*60 + data[2],
                        data[3], data[4], data[5], int(data[6]) - 43119, data[7] ,
                        (int(data[6]) - 43119) * 24*60 + data[7], data[8], data[9], data[10], data[11])
            pucks.append(puck)
            pucks_matrix.append(data)
    return pucks,pucks_matrix

#计算笛卡尔积并保存
def saveAsMul(path,matrix_1,matrix_2):
    mapper = []
    for x in itertools.product(matrix_1, matrix_2):
        y = x[0] + x[1]
        mapper.append(y)
    np.savetxt(path,mapper,delimiter=',',fmt='%s')

def extractFile(path,containTitle = False):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    matrix = []
    for i in range(sheet.nrows):
        if containTitle:
            if i != 0:
                data = sheet.row_values(i)
        else:
            data = sheet.row_values(i)
        matrix.append(data)
    return matrix