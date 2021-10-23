from alg.metis_linux import  *
from alg.jpr import *
import networkx as nx
import  os
from os import listdir
from os.path import isfile, join
import csv
onlyfiles = [f for f in listdir('graph/') if isfile(join('graph/', f))]
f = open("balance-experiment12.csv", 'w')

# create the csv writer
writer = csv.writer(f)
writer.writerow(['num_servers','file_name','metis_write','metis_read','metis_num_rep'])
for part in [2,4,8,16,32,64,96,128,256,512]:
    for file_src in onlyfiles:
        if "balanced" in file_src:
            print(file_src)
            G =  nx.read_gpickle('graph/'+file_src)
            metis_write,metis_num_rep=weight_calcuate(test=False,part=part,G = G)
            # jpr_wirte_cost, jpr_total_traffic, jpr_num_rep = jpr(test=False,num_servers=part)

            writer.writerow([part,file_src,metis_write,0,metis_num_rep])
