import numpy as np
import os

import pandas as pd

## Data making    

import random
def fisher_yates_shuffle(list):##偏好序列　打乱偏好序列
    # apply for a new list
    res = []
    while list:
        p = random.randrange(0, len(list))
        res.append(list[p])
        list.pop(p)
    return res

Car_n = 1000
Car_list = []
Park_n = 1000
Park_list = []


ranklist = []
for i in range(Park_n):
    if i < Car_n:
        Car_list.append(i+1)
    Park_list.append(i+1)
    #构造车辆和车位序列

def make():
    for i in range(Park_n):
        if i < Car_n:
            Car_list.append(i+1)
        Park_list.append(i+1)
    return (Car_list,Park_list)

for i in range(Car_n):
    ranklist.append(fisher_yates_shuffle(make()[1]))
##构造所有车辆的偏好序列

Car_Time = []
for i in range(Car_n):
    temp = np.random.randint(0,3)
    if temp == 0:
        s = np.random.rand() + np.random.randint(6,9)#[6,9)
        e = np.random.rand() + np.random.randint(11,14)
        Car_Time.append([s,e])
    elif temp == 1:
        s = np.random.rand() + np.random.randint(12,14)
        e = np.random.rand() + np.random.randint(18,24)
        Car_Time.append([s,e])
    else:
        s = np.random.rand() + np.random.randint(6,20)
        e = np.random.rand() + np.random.randint(int(s)+1,24)
        Car_Time.append([s,e])
    ##make the time of the cars

Park_Time = []
for i in range(Park_n):
    s = np.random.rand() + np.random.randint(4,7)#
    e = np.random.rand() + np.random.randint(22,24)
    Park_Time.append([s,e])
    ##make the time of the cars
    

def data_rate(s_c,e_c,s_p,e_p):
    k1 = 0.65*2
    k2 = 0.35*2
    rate = k1*abs((s_c - s_p)/(e_p-s_p)) + k2*abs((e_p - e_c)/(e_p-s_p))
    return rate
## waste rate

#Car_Time

Car_Time = sorted(Car_Time)

### Slide Window

Suc_match = []
Matching = []
Car_sta = []
Park_sta = []
for i in range(Park_n):
    if i < Car_n:
        Car_sta.append(0)
    Park_sta.append(0)
    #initiate the list

def find_index(car_index):
    index = -1
    for i in range(len(Matching)):
        if Matching[i][1] == car_index:
            index = i
            break
    return index 

def find_car_index(park_index):
    car_index = -1
    for i in Matching:
        if i[2] == park_index:
            car_index = i[1]
            break
    return car_index 

def Modify(car_index):##DC-G-S
    #print(car_index)
    #print(Car_sta[car_index])
    now_park_index = ranklist[car_index][Car_sta[car_index]] - 1
    if Park_sta[now_park_index] == 0:
        #print('find_index:',find_index(car_index))
        Matching[find_index(car_index+1)] = [Car_Time[car_index][0],car_index+1,now_park_index+1]
        Park_sta[now_park_index] = 1
        return 
    if find_car_index(now_park_index+1) == -1:
        Car_sta[car_index] = Car_sta[car_index] + 1
        Modify(car_index)
    else:
        index = find_car_index(now_park_index+1) - 1
        now = data_rate(Car_Time[car_index][0],Car_Time[car_index][1],Park_Time[now_park_index][0],Park_Time[now_park_index][1])
        ago = data_rate(Car_Time[index][0],Car_Time[index][1],Park_Time[now_park_index][0],Park_Time[now_park_index][1])
        if now < ago:
            Car_sta[index] = Car_sta[index] + 1
            Modify(index)
        else:
            Car_sta[car_index] = Car_sta[car_index] + 1
            Modify(car_index)

def Modify1(car_index):## FIFO
    #print(car_index)
    #print(Car_sta[car_index])
    now_park_index = ranklist[car_index][Car_sta[car_index]] - 1
    if Park_sta[now_park_index] == 0:
        #print('find_index:',find_index(car_index))
        Matching[find_index(car_index+1)] = [Car_Time[car_index][0],car_index+1,now_park_index+1]
        Park_sta[now_park_index] = 1
        return 
    Car_sta[car_index] = Car_sta[car_index] + 1
    Modify1(car_index)
    '''if find_car_index(now_park_index+1) == -1:
        Car_sta[car_index] = Car_sta[car_index] + 1
        Modify(car_index)
    else:
        index = find_car_index(now_park_index+1) - 1
        now = data_rate(Car_Time[car_index][0],Car_Time[car_index][1],Park_Time[now_park_index][0],Park_Time[now_park_index][1])
        ago = data_rate(Car_Time[index][0],Car_Time[index][1],Park_Time[now_park_index][0],Park_Time[now_park_index][1])
        if now < ago:
            Car_sta[index] = Car_sta[index] + 1
            Modify(index)
        else:
            Car_sta[car_index] = Car_sta[car_index] + 1
            Modify(car_index)'''

def Match(car):
    Matching.append(car)
    Car_index = car[1]-1
    Modify(Car_index)

def Match1(car):
    Matching.append(car)
    Car_index = car[1]-1
    Modify1(Car_index)

point =0.012

Matching = []
Suc_match = []
for i in range(Park_n):
    if i < Car_n:
        Car_sta.append(0)
    Park_sta.append(0)
time1 = 0.0
time2 = point
for i in range(Car_n*2):
    if i < Car_n:
        tempdata = [Car_Time[i][0],i+1,ranklist[i][0]]
        Match(tempdata)
    
    count = 0
    for j in range(len(Matching)):
        if Matching[j][0] >= time1 and Matching[j][0] <= time2:
            Suc_match.append(Matching[count])
            count = count+1
    Matching = Matching[count:]
    if len(Suc_match) != 0:
        for k in Suc_match:
            if Car_Time[k[1]-1][1] >= time1 and Car_Time[k[1]-1][1] <= time2:
                Park_sta[k[2]-1] = 0
                #Park_Time[k[2]-1][0] = Car_Time[k[1]-1][1]
    time1 = time1 + point
    time2 = time2 + point
    '''input()
    print(time1,'            ',time2)
    print(i,':Matching:',Matching)
    print('Suc_match:',Suc_match)'''



len(Matching)

len(Suc_match)

def Index(car,park):
    ind = 0
    for i in range(len(ranklist[car])):
        if park == ranklist[car][i]:
            ind = i + 1
            break
    return ind

Match_num = []
Unique = []
for i in Suc_match:
    Match_num.append(Index(i[1]-1,i[2]))
    Unique.append(i[2])

num = len(np.unique(Unique))
num

sss = sorted(Match_num)



import matplotlib.pyplot as plt

'''plt.plot(sorted(Match_num))
plt.xlabel('Car ID')
plt.ylabel('Preference Number')
plt.savefig('/home/sunny/Paper/image/9.jpg')
'''

#Suc_match

Sum_rate = 0
for i in range(len(Suc_match)):
    rate = abs(Car_Time[Suc_match[i][1]-1][1] - Car_Time[Suc_match[i][1]-1][0])/abs(Park_Time[Suc_match[i][2]-1][1] - Park_Time[Suc_match[i][2]-1][0])
    #print(rate)
    Sum_rate = Sum_rate + rate
print(Sum_rate/num)

print(num)

print(sum(sss)/len(sss))