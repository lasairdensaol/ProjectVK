import networkx as nx


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