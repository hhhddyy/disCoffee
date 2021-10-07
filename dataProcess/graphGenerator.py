import pandas as pd
import networkx as nx
import random
import numpy as np
def csv_2_UGraph(file_src="../data/lastfm/lastfm_asia_edges.csv",test=False):
    '''
    The function read the csv file and then create a undirected but WEIGHTED  graph
    :param file_src:
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
    # then assign weight
    for edge in G.edges:
        G[edge[0]][edge[1]]['weight'] = random.randint(1,10)

    unique_node = list(G.nodes.keys())

    node_weight = np.random.randint(1, 10, len(unique_node))

    for node_index in range(len(unique_node)):
        G.nodes[unique_node[node_index]]['write_weight'] = node_weight[node_index]
    return G



def ug_2_InteractionG(G:nx.Graph,loaded=False):
    '''
    Take an undirected graph and then generated an interaction graph
    :param G:
    :return:
    '''
    if loaded:
        #todo
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







