import metis
import networkx as nx
import dataProcess.graphGenerator as gen
import numpy as np

# THE CODE IS ONLY TEST ON UBUNTU
#
# sudo apt-get install metis
#
# then pip3 install metis

def metiis_api(input_graph,part):
    (edgecuts, parts)  = metis.part_graph(input_graph,part)
    #print(edgecuts,parts)
    return edgecuts,parts

def weight_calcuate(test,part):
    '''
    In order to calcuate the cost, we only need to calcuate the write cost after performing
    the rep
    :param test:
    :param part: num of parts
    :return:
    '''
    if test:
        G= gen.csv_2_UGraph(test=test)
        # input_g = gen.ug_2_lineG(G)

    # create input line graph
    else:
        G=gen.csv_2_UGraph(test=test)
        # input_g = gen.ug_2_lineG(G)

    # edgecut is the num of cuts in G and parts tell us which part the node belongs to
    edgecuts,parts=metiis_api(G,part)
    # each server hold which node
    severs = {}

    node_in_sever = dict(zip(list(G.nodes.keys()),parts))

    for i in range(part):
        severs[i] = []
    nodes = list(G.nodes.keys())

    # store as a list
    for node in nodes:
        node_in_sever[node] = [node_in_sever[node]]
    for index in range(len(parts)):
        node = nodes[index]
        severs[parts[index]].append(node)
    cost = 0
    num_rep=0
    for edge in list(G.edges):
        w = G[edge[0]][edge[1]]['weight']
        # perform rep
        if len(set(node_in_sever[edge[0]]).intersection(set(node_in_sever[edge[1]])))==0:
            num_rep+=1
            # compare the write cost
            if G.nodes[edge[0]]['write_weight'] < G.nodes[edge[1]]['write_weight']:
                #severs[node_in_sever[edge[1]]].append(edge[0])
                #then load balance, choose the one server with min number node
                min_load_server = node_in_sever[edge[1]][0]
                for s in node_in_sever[edge[1]]:
                    if len(severs[min_load_server]) > len(severs[s]):
                        min_load_server = s
                # then add edge[0] to server s
                severs[s].append(edge[0])
                node_in_sever[edge[0]].append(s)


                cost+=G.nodes[edge[0]]['write_weight']
            else:
                min_load_server = node_in_sever[edge[0]][0]
                for s in node_in_sever[edge[0]]:
                    if len(severs[min_load_server]) > len(severs[s]):
                        min_load_server = s
                # then add edge[1] to server s
                severs[s].append(edge[1])
                node_in_sever[edge[1]].append(s)
                #severs[node_in_sever[edge[0]]].append(edge[1])
                cost += G.nodes[edge[1]]['write_weight']
    print("cost:",cost)
    print("num of rep:",num_rep)











weight_calcuate(test=False,part=64)
