import pandas as pd
import networkx as nx
import random
import numpy as np
file_src = "../data/git_web_ml/musae_git_edges.csv"
file_src="data/lastfm/lastfm_asia_edges.csv"
#file_src = "../data/twitch_gamers/large_twitch_edges.csv"
def csv_2_UGraph(file_src=file_src,test=False,rw_ratio='balanced',count=1):
    '''
    The function read the csv file and then create a undirected but WEIGHTED  graph
    :param file_src:
    :param rw_ratio: read write weight
    :return:the ud, uw graph G
    '''
    csv_src = pd.read_csv(file_src)
    if test:
        csv_src = csv_src.sample(frac=0.1)
    node_1 = csv_src.node_1
    node_2 = csv_src.node_2
    edges = list(zip(node_1,node_2))
    G = nx.Graph()
    G.add_edges_from(edges)
    # then assign read weight
    for edge in G.edges:
        if rw_ratio=='balanced':
            G[edge[0]][edge[1]]['weight'] = random.randint(1,10)
        elif rw_ratio =='read':
            G[edge[0]][edge[1]]['weight'] = random.randint(7, 10)
        else:
            G[edge[0]][edge[1]]['weight'] = random.randint(1, 3)

    unique_node = list(G.nodes.keys())
    if rw_ratio == 'balanced':
        node_weight = np.random.randint(1, 10, len(unique_node))
    elif rw_ratio == 'read':
        node_weight = np.random.randint(1, 3, len(unique_node))
    else:
        node_weight = np.random.randint(7, 10, len(unique_node))


    for node_index in range(len(unique_node)):
        G.nodes[unique_node[node_index]]['write_weight'] = node_weight[node_index]

    # then save the graph as pickle
    # pre_fix = file_src.split('/')[2]
    # nx.write_gpickle(G, "../graph/"+pre_fix+"-"+rw_ratio+str(count)+".gpickle")
    # readPickle("../graph/"+pre_fix+"-"+rw_ratio+str(count)+".gpickle")
    return G



def ug_2_InteractionG(G:nx.Graph,loaded=False,file_src = None):
    '''
    Take an undirected graph and then generated an interaction graph
    :param G:
    :return:
    '''
    if loaded:
        G = nx.read_gpickle(file_src)
        return

    interactionG = nx.MultiDiGraph()

    # assign weight for edges, weight is from 1-10
    for edge in G.edges:
        interactionG.add_edge(edge[0],edge[1],G[edge[0]][edge[1]]['weight'])
        interactionG.add_edge(edge[1], edge[0], weight=random.randint(1, 10))

    # assign weight for nodes
    unique_node = list(G.nodes.keys())


    for node_index in range(len(unique_node)):
        interactionG.nodes[unique_node[node_index]]['write_weight'] = G.nodes[unique_node[node_index]]['write_weight']
    return interactionG

def ug_2_lineG(G:nx.Graph,loaded=False):
    '''
    given an undirected graph, generated a
    :param G:
    :param loaded:
    :return:
    '''

    L = nx.line_graph(G)

    # assign weight to graph edge

    for edge in L.edges:
        common_node = list(set(edge[0]).intersection(set(edge[1])))[0]
        weight = G.nodes[common_node]['write_weight']
        L[edge[0]][edge[1]]['weight'] = weight

    return L
def readPickle(file_src):
    G = nx.read_gpickle(file_src)
    #  to node list neighbors and weight
    node_list = list(G.nodes.keys())
    neighbors = {}
    write_weight = {}
    for node in node_list:
        neighbors[node] = list(G.neighbors(node))
        write_weight[node] = G.nodes[node]['write_weight']
    #print(neighbors,write_weight)
    return  node_list,neighbors,write_weight







