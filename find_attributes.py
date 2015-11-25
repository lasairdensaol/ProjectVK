import numpy as np
import pandas as pd
from collections import Counter
import datetime as dt


year = dt.datetime.now().year

def map_age(x):
    if x is not None:
        splited = x.split('.')
        if len(splited) == 3:
            return year - int(splited[2])
    return None

def average_moda(c, n, ave_moda):
    for k in c.keys():
        if c[k] == max(c.values()):
               if n != 0:
                   ave_moda.append((ave_moda.pop() + k)/(n + 1))
                   continue

               ave_moda.append(k)
               n = n + 1
    return ave_moda

def average(ccce):
    if ccce:
        return np.sum([ccce[k]*k for k in ccce.keys()]) / np.sum(ccce.values())
    else:
        return 0

def find_key(dic, v):
    res = []
    for k in dic.keys():
        if dic[k] == v:
            res.append(k)
    return res

def find_age_1(df):
    has_age = pd.notnull(df['age'])
    count_has_age = Counter(has_age)[True]

    if count_has_age == 0:
        return 0
    else:
        return int(df['age'].sum()/count_has_age)

def find_age_2(count_f_in_comm, new_df):
    ave_moda = []
    for i in range(len(count_f_in_comm)):
        n = 0
        if count_f_in_comm.values()[i] > 3:
            tmp_df = Counter(new_df[new_df['community'] == i]['age'])
            if len(tmp_df) == 0:
                continue

            ave_moda = average_moda(tmp_df, n, ave_moda)

    if len(ave_moda) == 0:
        return 0
    else:
        return int(np.sum(ave_moda)/len(ave_moda))

def find_age_3(count_f_in_comm, new_df):
    huge_comm = max(count_f_in_comm.values())
    nums_of_hugest_comm = []

    for k in count_f_in_comm.keys():
        if count_f_in_comm[k] == huge_comm:
            nums_of_hugest_comm.append(k)


    ave_moda_2 = []

    for i in nums_of_hugest_comm:
        n = 0
        tmp_df = Counter(new_df[new_df['community'] == i]['age'])
        if len(tmp_df) == 0:
            continue

        ave_moda_2 = average_moda(tmp_df, n, ave_moda_2)

    if len(ave_moda_2)  == 0:
        return 0
    else:
        return int(np.sum(ave_moda_2)/len(ave_moda_2))

def find_age_4(count_f_in_comm, new_df):
    variance = dict()

    for i in count_f_in_comm.keys():
        tmp_df = new_df[new_df['community'] == i]['age']
        if len(tmp_df) > 1:
            variance[i] = np.var(tmp_df)

    if len(variance) == 0:
        return 0
    else:
        find_min = min(variance.values())
        k = find_key(variance,find_min)

        if len(k) > 1:
            ave = []
            for i in k:
                comm_min_var = Counter(new_df[new_df['community'] == i]['age'])
                ave.append(average(comm_min_var))
            return int(np.sum(ave)/len(ave))
        else:
            comm_min_var = new_df[new_df['community'] == k[0]]['age']
            return int(np.sum(comm_min_var)/len(comm_min_var))

def find_age_5(count_f_in_comm, new_df):
    mean_var = dict()

    for i in count_f_in_comm.keys():
        tmp_df = new_df[new_df['community'] == i]['age']
        if len(tmp_df) > 1:
            mean_var[i] = [np.var(tmp_df), np.mean(tmp_df)]

    if len(mean_var) <= 1:
        return 0
    else:
        sum_var_1 = np.sum([x[0] for x in mean_var.values()])
        sum_var_2 = np.sum([sum_var_1 - x[0] for x in mean_var.values()])

        for x in mean_var.keys():
            mean_var[x].append((sum_var_1 - mean_var[x][0])/sum_var_2)

        return int(np.sum([x[1]*x[2] for x in mean_var.values()]))

def find_city(df):
    has_city = pd.notnull(df['city.title'])
    new_df_c = df[has_city]['city.title']

    cities_friends = Counter(new_df_c)
    numb_most_comm_city = max(cities_friends.values())

    return find_key(cities_friends, numb_most_comm_city)