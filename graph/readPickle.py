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