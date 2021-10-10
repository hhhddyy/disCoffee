import metis
import networkx as nx
import dataProcess.graphGenerator as gen

# THE CODE IS ONLY TEST ON UBUNTU
#
# sudo apt-get install metis
#
# then pip3 install metis

def metiis_api(test=False):
    if test:
        G= gen.csv_2_UGraph(test=True)
        input_g = gen.ug_2_lineG(G)

    # create input line graph
    else:
        G=gen.csv_2_UGraph(test=True)
        input_g = gen.ug_2_lineG(G)


    (edgecuts, parts)  = metis.part_graph(input_g,3)
    print(edgecuts,parts)
# G = metis.example_networkx()
# (edgecuts, parts) = metis.part_graph(G, 3)
# print(edgecuts)
metiis_api(test=True)