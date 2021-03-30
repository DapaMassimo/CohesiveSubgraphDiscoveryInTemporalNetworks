import networkx as nx
import fib_heap_mod
import copy
from goldberg_weighted import get_solution



def charikarHeapWeighted(G):
    """
    Returns the subgraph of G with highest average degree
    and the average degree of said subgraph. If you want the 
    density then divide the average degree by 2 after calling 
    this function
    """         
    E = G.number_of_edges()
    N = G.number_of_nodes()
    fib_heap = fib_heap_mod.FibonacciHeap()
    entries = {}
    order = []
    S = copy.deepcopy(G)
    
    #calculate degree of each node as the sum of
    #the weights of all edges incident on the node
    degree = {}
    W = 0 #sum of all the weights of the graph
    for n in S.nodes():
        degree[n] = 0
        for edge in S.edges(n):
            degree[n] += S.get_edge_data(*edge)['weight']
        W += degree[n]
    W = W/2
    
    for n, d in degree.items():
        entries[n] = fib_heap.insert(d, n)
    
    best_avg = 0.0    
    best_iter = iter = 0
    
    while fib_heap:
        avg_degree = (2.0 * W)/N
        if best_avg <= avg_degree:
            best_avg = avg_degree
            best_iter = iter
            
        min_deg_obj = fib_heap.extract_min()
        min_deg_node = min_deg_obj.get_value()
        order.append(min_deg_node)
        for n in list(S.neighbors(min_deg_node)):
            new_key = entries[n].get_key() - S.get_edge_data(min_deg_node, n)['weight']
            fib_heap.decrease_key(entries[n], new_key)
        
        
        W -= min_deg_obj.get_key()
        E -= len(list(S.neighbors(min_deg_node)))
        N -= 1
        iter += 1
        S.remove_node(min_deg_node)
        
        
    S = copy.deepcopy(G)       
    for i in range(best_iter):
        S.remove_node(order[i])
    
    dens = weighted_density(S)

    return S, dens


def weighted_density(g):
    W = 0

    for node in g.nodes():
        for edge in g.edges(node):
            W += g.get_edge_data(*edge)['weight']

    W = W/2
    
    return W/len(g.nodes())
    



    
    
