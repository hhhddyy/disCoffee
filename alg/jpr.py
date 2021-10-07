import copy
import random

import  networkx as nx
import numpy as np
from lib_repo import  Coarse as metis
import community
import partition_networkx
import dataProcess.graphGenerator as gen
from networkx.algorithms import community
from karateclub import LabelPropagation,EdMot,SCD
from threading import  Thread
def jpr(test=False):
    if test:
        G= gen.csv_2_UGraph(test=True)
        input_g = gen.ug_2_lineG(G)

    # create input line graph
    else:
        G=gen.csv_2_UGraph(test=True)
        input_g = gen.ug_2_lineG(G)
    # mapping ={}
    # index =0
    # for node in input_g.nodes:
    #     mapping[node] = index
    #     index = index+1
    # input_g = nx.relabel_nodes(input_g, mapping)
    models = [LabelPropagation(),EdMot(component_count=10),SCD()]
    threads = [None] * 3
    results = [None] * 3
    inputs = [copy.deepcopy(input_g),copy.deepcopy(input_g),copy.deepcopy(input_g)]
    alg=['gmc','lp','alpa']
    for i in range(len(threads)):
        threads[i] = Thread(target=coarse_by_networkX, args=(inputs[i], alg[i],results, i))
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    #phase2


    #suppose result is a list
    cut_weight_eachP = [0,0,0]


    p_index =0
    for p_list in results:
        cut_in_p = [True] * len(input_g.edges)
        cut_index = 0
        # find possible cut
        for edge in input_g.edges:
            for p in p_list:
                p = list(p)
                if edge[0] in p and edge[1] in p:
                    cut_in_p[cut_index] =False
                    break
            cut_index = cut_index+1
        cut_index=0
        for edge in input_g.edges:
            if cut_in_p[cut_index]:
                common_node = list(set(edge[0]).intersection(set(edge[1])))[0]
                cut_weight_eachP[p_index] = cut_weight_eachP[p_index]+ G.nodes[common_node]['write_weight']
            cut_index = cut_index +1
        p_index = p_index +1

    min_index = np.argwhere(cut_weight_eachP==np.amin(cut_weight_eachP))

    q=results[min_index[0][0]]

    # then place master
    #find si
    server_dict ={}
    user_each_serverHold ={}
    for user in G.nodes:
        server_dict[user] =[]
        server_index =0
        for part in q:
            part = list(part)
            for pair in part:
                pair = list(pair)
                if user in pair:
                    server_dict[user].append(server_index)
            server_index = server_index +1

    server_index = 0
    for part in q:
        user_each_serverHold[server_index] =[]
        server_index = server_index+1

    for user in G.nodes:
        for server in list(server_dict[user]):
            user_each_serverHold[server].append(user)

    mas_each_user = {}
    print("write: ",cut_weight_eachP[min_index[0][0]])
    total_traffic = cut_weight_eachP[min_index[0][0]]
    for user in G.nodes:
        min_T = 999999999
        master = -1
        for server in server_dict[user]:
            traffic = 0
            for other_user in G.neighbors(user):
                if other_user not in user_each_serverHold[server]:
                    traffic = traffic + G[user][other_user]['weight']
            if traffic < min_T:
                master = server
                min_T = traffic
        mas_each_user[user] = master
        total_traffic = total_traffic+min_T


    print(total_traffic)


































def coarse(input,model_list,result,index):
    input_g = input[index]
    model = model_list[index]
    model.fit(input_g)
    cluster_membership = model.get_memberships()

    result[index] = cluster_membership

def coarse_by_networkX(input,alg,result,index):
    if alg =='gmc':
        gmc_p = list(community.greedy_modularity_communities(input))
        result[index] = gmc_p
    if alg =='lp':

        lp_p= list(community.label_propagation_communities(input))
        result[index]=lp_p
    if alg == 'alpa':
        alpa_p=list(community.asyn_lpa_communities(input))
        result[index] = alpa_p

jpr(test=False)