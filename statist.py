import os
import codecs
import json
import find_attributes as fa

number_of_algorithms = 5

def save_result(user_id, data):
    with codecs.open(r'E:\test\res\\' + str(user_id) + ".txt", 'a','utf-8') as ouf:
        for i in data:
            ouf.write(str(i) + '\r\n')
    ouf.close()

def save_tmp_result(user_id, tmp, encoding="cp1251"):
    with codecs.open(r'E:\test\tmp\\' + str(user_id) + "_class.txt", 'w', encoding=encoding) as ouf:
        json.dump(tmp, ouf, indent=1, ensure_ascii = 0)


all_id = [os.listdir(r'E:\test\id%d\\'%(i)) for i in range(1,5)]

def get_age(_id):
    for i in range(len(all_id)):
        if str(_id) + '.txt' in all_id[i]:
            num_dir = i + 1
            break

    with codecs.open(r'E:\test\id' + str(num_dir) + '\\' + str(_id) + ".txt", 'r','utf-8') as inf:
        profile_user = json.load(inf)
    inf.close()

    if 'bdate' in profile_user.keys():
        return fa.map_age(profile_user['bdate'])
    else:
        return None

def accuracy(number_alg):
    stat_of_age = []

    id_users = os.listdir(r'E:\test\res\\')

    for user_id in id_users:

        with codecs.open(r'E:\test\res\\' + str(user_id), 'r','utf-8') as inf:
            inf_for_stat = inf.readlines()
        inf.close()

        stat_of_age.append(abs(int(inf_for_stat[number_alg]) - int(inf_for_stat[0])))


    summ = 0
    for i in range(len(stat_of_age)):
        summ = stat_of_age[i]**2 + summ

    return (summ/len(stat_of_age))**0.5

def check():
    with codecs.open(r'E:\test\res\\' + "accuracy", 'w','utf-8') as ouf:
        for i in range(1,number_of_algorithms):
            ouf.write(accuracy(i) + '\r\n')
    ouf.close()

