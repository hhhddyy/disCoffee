import  networkx as nx
import numpy as np
from lib_repo import  Coarse as metis
import community
import partition_networkx
import dataProcess.graphGenerator as gen
from networkx.algorithms import community
def jpr():

    # create input line graph
    input_g = gen.ug_2_lineG(gen.csv_2_UGraph())
    # get adjacency matrix

    coarse_max = 100
    #xadj, adjncy, weight, match, cmap = metis.coarse(input_g, coarse_max)
    communities_generator = community.girvan_newman(input_g)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    print(sorted(map(sorted, next_level_communities)))





    # phase 1

jpr()