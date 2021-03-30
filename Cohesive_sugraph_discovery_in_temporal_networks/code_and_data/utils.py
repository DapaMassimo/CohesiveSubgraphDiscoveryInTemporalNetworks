import pickle
import time
import networkx as nx
from numpy import random
from datetime import datetime
from charikar_heap_weighted import charikarHeapWeighted
from goldberg_weighted import get_solution


#Function that reads real-world datasets from file 
#(look into the 'data' folder to see the format of the data).
#Returns a dictionary where the keys are the single timestamps and 
#the values are lists of edges available in that timestamp.
def read_time_stamps(file_name):
    """
    Function to read the real-world datasets in the ./data folder
    and get them ready for GrdWeightedDP or OptWeightedDP
    """
    time_stamp_dict = {}
    
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:                
            line = line.strip().split(' ')
            
            time_str =  line[0][1:] + ' ' + line[1][0:-1]
            t = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            time_stamp = time.mktime(t.timetuple())
                
            ts, n1, n2 = int(time_stamp), line[2], line[3]

            if n1 == n2: continue #self loop edges are not allowed
            
            if n2 < n1:
                n1, n2 = n2, n1

            if ts not in time_stamp_dict:
                time_stamp_dict[ts] = [(n1, n2)]
            else:
                time_stamp_dict[ts].append((n1, n2))
                
    return dict(sorted(time_stamp_dict.items()))

def save_data(data, file):
    if file[-4:] == '.txt':
        name = file
    else:
        name = file + '.txt'
    
    with open(name, 'wb') as f:
        pickle.dump(data, f, 0)
        
def read_data(file):
    if file[-4:] == '.txt':
        name = file
    else:
        name = file + '.txt'
    
    with open(name, 'rb') as f:
        return pickle.load(f)

#%%
#a couple of functions to test goldberg_weighted and charikar_weighted
def generate_weighted_graphs(list_length, num_node_max, edge_prob_max, weight_max):
    log = []
    for i in range(list_length):
        num_nodes = random.randint(2, num_node_max)
        edge_prob = round(random.uniform(0.1, edge_prob_max), 2)
        g = nx.erdos_renyi_graph(num_nodes, edge_prob)
        for n1, n2 in g.edges():
            g[n1][n2]['weight'] = random.randint(1, weight_max)
        log.append(g)
        
    return log


def testCharikarHeapWeighted(list_length, num_node_max, edge_prob_max, weight_max):
    log = generate_weighted_graphs(list_length, num_node_max, edge_prob_max, weight_max)
    num_graphs = len(log)
    res_charikar = []
    res_goldberg = []
    
    for i in range(num_graphs):
        print('%d: %d , %d ' % (i, len(log[i].nodes()), len(log[i].edges)))
        res_charikar.append(charikarHeapWeighted(log[i]))
        res_goldberg.append(get_solution(log[i]))

        
    return log, res_charikar, res_goldberg

    

