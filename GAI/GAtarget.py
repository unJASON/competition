#Importing required modules
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import PreOperation
import extractExcel
path = 'InputData.xlsx'
tickets, tickets_matrix = extractExcel.extractTicket(path)
pucks, pucks_matrix = extractExcel.extractPuck(path)
# solution = [min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)]
DI_W_pucks_matrix_sorted, DI_N_pucks_matrix_sorted, ID_W_pucks_matrix_sorted, ID_N_pucks_matrix_sorted, \
DD_W_pucks_matrix_sorted, DD_N_pucks_matrix_sorted, II_W_pucks_matrix_sorted, II_N_pucks_matrix_sorted= PreOperation.PreOperation_Pucks(path)
I_I_N_gates,I_I_W_gates,I_DI_W_gates,D_D_N_gates,\
D_D_W_gates,D_DI_N_gates,DI_DI_W_gates,DI_DI_N_gates,DI_D_N_gates,DI_I_W_gates = PreOperation.PreOperation_Gates(path)
planes = DD_N_pucks_matrix_sorted
gatesList = D_D_N_gates
previlege = np.random.permutation(planes.__len__())
generationList=[]
for i in range(1000):
    a = np.zeros(planes.__len__())
    for ser_i in range( planes.__len__() ):
        gatesLength = gatesList.__len__()
        a[ser_i] = previlege[(ser_i+i)%planes.__len__()] % gatesLength
    generationList.append(a)
# generationList = np.asarray(generationList,dtype=np.int)

def function1(x):
    # value = -x**2
    # return value
    count = 1
    time_gate = {}

    for i in range(planes.__len__()):
        if(type(x) == float):
            print("hahah")
        if not time_gate.__contains__(str(x[i])):
            time_gate[str(x[i])] = planes[i][6] * 24 * 60 + planes[i][7] + 45
        else:
            if planes[i][1] * 24 * 60 + planes[i][2] < time_gate[str(x[i])]:
                count = count + 1
            else:
                time_gate[str(x[i])] = planes[i][6] * 24 * 60 + planes[i][7] + 45
    return 1 / count


def function2(x):
    time_gate = {}
    count = 1
    total_time = 0
    for plane in planes:
        total_time = total_time + plane[6] * 24 * 60 + plane[7] - plane[1] * 24 * 60 - plane[2]
    for i in range(planes.__len__()):
        if not time_gate.__contains__(str(x[i])):
            time_gate[str(x[i])] = planes[i][6] * 24 * 60 + planes[i][7] + 45
        else:
            if planes[i][1] * 24 * 60 + planes[i][2] < time_gate[str(x[i])]:
                count = count + 1
            else:
                time_gate[str(x[i])] = planes[i][6] * 24 * 60 + planes[i][7] + 45
    return total_time/(count*24*60)
    # value = -(x-2)**2
    # return value


#Function to find index of list
#函数查找列表的索引
def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

#Function to sort by values 函数根据值排序
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list

#Function to carry out NSGA-II's fast non dominated sort
#函数执行NSGA-II的快速非支配排序
"""基于序列和拥挤距离"""
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0,len(values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(values1)):
             #p > q
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]

    return front

#Function to calculate crowding distance
#计算拥挤距离的函数
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance

#Function to carry out the crossover
#函数进行交叉
def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutation((a+b)/2)
    else:
        return mutation((a-b)/2)

#Function to carry out the mutation operator
#函数进行变异操作
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob <1:
        solution = min_x+(max_x-min_x)*random.random()
    return solution

#Main program starts here
pop_size = 1000
max_gen = 921

#Initialization
min_x=-55
max_x=55




solution=[min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)]
solution = generationList
gen_no=0
while(gen_no<max_gen):
    function1_values = [function1(solution[i])for i in range(0,pop_size)]
    function2_values = [function2(solution[i])for i in range(0,pop_size)]
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:],function2_values[:])
    print("The best front for Generation number ",gen_no, " is")
    for valuez in non_dominated_sorted_solution[0]:
        # print(round(solution[valuez],3),end=" ")
        print(solution[valuez], end=" ")
    print("\n")
    crowding_distance_values=[]
    for i in range(0,len(non_dominated_sorted_solution)):
        crowding_distance_values.append(crowding_distance(function1_values[:],function2_values[:],non_dominated_sorted_solution[i][:]))
    solution2 = solution[:]

    #Generating offsprings
    while(len(solution2)!=2*pop_size):
        a1 = random.randint(0,pop_size-1)
        b1 = random.randint(0,pop_size-1)
        if( type (crossover(solution[a1], solution[b1])) == float):
            print("H")
        solution2.append(crossover(solution[a1],solution[b1]))

    function1_values2 = [function1(solution2[i])for i in range(0,2*pop_size)]
    function2_values2 = [function2(solution2[i])for i in range(0,2*pop_size)]
    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:],function2_values2[:])
    crowding_distance_values2=[]
    for i in range(0,len(non_dominated_sorted_solution2)):
        crowding_distance_values2.append(crowding_distance(function1_values2[:],function2_values2[:],non_dominated_sorted_solution2[i][:]))
    new_solution= []
    for i in range(0,len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
        front.reverse()
        for value in front:
            new_solution.append(value)
            if(len(new_solution)==pop_size):
                break
        if (len(new_solution) == pop_size):
            break
    solution = [solution2[i] for i in new_solution]
    gen_no = gen_no + 1

#Lets plot the final front now
function1 = [i * -1 for i in function1_values]
function2 = [j * -1 for j in function2_values]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()