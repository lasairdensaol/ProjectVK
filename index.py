import pandas as pd
import json
import codecs
import os
from collections import Counter
import community
import find_attributes as fa
import statist as st
import framework as fr

class JsonUtils(object):
    @staticmethod
    def json_path(json, path, default=u''):
        splited = path.split(u'.')
        for p in splited:
            try:
                p_id = int(p)
                json = json[p_id]
            except:
                if p in json:
                    json = json[p]
                else:
                    return default

        return unicode(json)

fields = ['first_name', 'last_name', 'bdate','sex',
         'city.title',
         'universities.0.name',
         'schools.0.name', 'schools.0.year_graduated']

def transform_user_profile(user_profile):
    return [JsonUtils.json_path(user_profile, field, default=None) for field in fields]


id_users = os.listdir(r'E:\ids\\')
id_users_ex = os.listdir(r'E:\res\\')


for user_id in id_users:

    user_id = int(user_id)


    with codecs.open("E:\ids\\" + str(user_id) + '\\' + str(user_id) + '.txt', 'r', 'utf-8') as inf:
        inf_about_user = json.load(inf)
    inf.close()

    with codecs.open("E:\ids\\" + str(user_id) + "\user_network.txt", 'r','utf-8') as inf:
        u_network = json.load(inf)
    inf.close()

#here was a graph...
    graph = fr.init(user_id, u_network)

    id_friends = os.listdir(r'E:\ids\\' + str(user_id) + '\\')

    id_friends.remove(str(user_id)+'.txt')
    id_friends.remove('user_network.txt')

    friend_profiles = []

    for x in id_friends:
        with codecs.open("E:\ids\\" + str(user_id) + '\\' + x, 'r','utf-8') as inf:
            u_friend = json.load(inf)
            friend_profiles.append(u_friend)
        inf.close()

    index = [int(fp['id']) for fp in friend_profiles]
    data = [transform_user_profile(fp) for fp in friend_profiles]

    df = pd.DataFrame(index=index, data=data, columns=fields)

    df['age'] = df.loc[:, 'bdate'].map(fa.map_age)

    real_user_age = str(fa.map_age(inf_about_user['bdate']))
    real_user_city = inf_about_user['city']['title']


    communities = community.best_partition(graph)

    df['community'] = df.index.map(lambda x : communities[x] if x in communities else None)


    new_df = df[df['age'] >0][:]


    count_f_in_comm = Counter(communities.values())


    age_1 = str(fa.find_age_1(df))

    age_2 = str(fa.find_age_2(count_f_in_comm, new_df))

    age_3 = str(fa.find_age_3(count_f_in_comm, new_df))

    age_4 = str(fa.find_age_4(count_f_in_comm, new_df))

    age_5 = str(fa.find_age_5(count_f_in_comm, new_df))

    most_comm_city = fa.find_city(df)

    res_inf = []

    res_inf.append(real_user_age)
    res_inf.append(age_1)
    res_inf.append(age_2)
    res_inf.append(age_3)
    res_inf.append(age_4)
    res_inf.append(age_5)

    res_inf.append(real_user_city)
    res_inf.append(most_comm_city[0])

    st.save_result(user_id, res_inf)

st.check()