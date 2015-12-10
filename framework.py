# coding=utf-8
import networkx as nx
import numpy as np
import statist as st

def init(user_id, u_network):
    graph = nx.Graph()

    all_friend = u_network.keys()

    for u in all_friend:
        for v in all_friend:
            if v <> u:
                if v in u_network[u]:
                    w = 1
                else:
                    w = 0

                graph.add_edge(int(u),int(v), weight = w)

    graph.remove_node(user_id)

    return graph



class my_map(object):

    def __init__(self, network):
        self.num_of_id = dict(enumerate(network.keys()))
        self.id_of_num = dict(zip( network.keys(), range(len(network.keys()))))

    def get_id(self, num):
        return self.num_of_id[num]
    def get_num(self, id):
        return self.id_of_num[id]
    def ids(self):
        return self.id_of_num.keys()
    def nums(self):
        return self.num_of_id.keys()

    def __repr__(self):
        return self.num_of_id.__repr__() + "\n\n" + self.id_of_num.__repr__()

def find_A(id_num, user_network):
    n = len(id_num.nums())
    A = np.zeros([n, n])

    for k, v in user_network.items():
        for f in v:
            i = id_num.get_num(str(k))
            j = id_num.get_num(str(f))
            A[i, j] = A[j, i] = 1

    return A


def find_classes(id_num):
    classes = {}
    for _id in id_num.ids():
        # получение возраста

        age = st.get_age(_id)
        print _id
        print age
        print "_______"
        if age:
            _class = age
        else:
            _class = -1

        classes[id_num.get_num(_id)] = _class

    return classes

def get_Y(C):
    n = len(C)
    k = 20

    Y = np.zeros((n,k))

    for k, v in C.items():
        if v > -1:
            Y[k][v] = 1

    return Y



def classification(user_network, tau = 0.001, q = 0.75):
    id_num = my_map(user_network)
    A = find_A(id_num, user_network)
    C = find_classes(id_num)
    Y = get_Y(C)

    L = np.diag(np.sum(A, axis = 1)) - A  #L = D - A
    beta = tau * (1/q - 1)

    TMP = ( np.eye(L.shape[0]) + beta * L )
    TMP = np.linalg.inv(TMP)
    F = TMP.dot(Y)


    ANSWER = np.argmax(F, axis = 1)

    D = dict(id_num.id_of_num)
    for k,v in D.items():
        D[k] = str(ANSWER[v])

    return D