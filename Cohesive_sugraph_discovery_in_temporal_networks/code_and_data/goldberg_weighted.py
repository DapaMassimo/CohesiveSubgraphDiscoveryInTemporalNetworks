from networkx.algorithms.flow import minimum_cut 

def get_solution(G):
    """
    Goldberg's densest subgraph algorithm implementation for integer edge 
    weighted graphs.
    G is an undirected graph with edge attributes 'weight'.
    G does not contain self-loops or multiple edges between the same pair of 
    nodes.
    """
    weighted_degrees = {}
    W = 0

    for node in G.nodes():
        weighted_degrees[node] = 0
        for edge in G.edges(node):
            weighted_degrees[node] += G.get_edge_data(*edge)['weight']
        W += weighted_degrees[node]
    W = W/2

    l = 0
    u = W
    n = len(G.nodes())
    m = len(G.edges())
    g = (u + l) / 2
    
    G_dir = G.to_directed()
    for node in G.nodes():
        G_dir.add_edge('s', node, weight = W)
        G_dir.add_edge(node, 't', weight = W + 2*g - weighted_degrees[node])
        
    while u - l >= 1/(n*(n - 1)):
        min_cut_val, (S, T)  = minimum_cut(G_dir, 's', 't', capacity='weight')
        
        if (len(S) - 1) == 0:
            u = g
        else:
            l = g
            
        g = (u + l) / 2
        for node in G.nodes():
            G_dir[node]['t']['weight'] = W + 2*g - weighted_degrees[node]
    
    #what I care is the lower bound l
    g = l
    G_dir = G.to_directed()
    for node in G.nodes():
        G_dir.add_edge('s', node, weight = W)
        G_dir.add_edge(node, 't', weight = W + 2*g - weighted_degrees[node])

    cut_value, (S, T) = minimum_cut(G_dir, 's', 't', capacity='weight')
    S.remove('s')
    D = G.subgraph(S)
    dens = weighted_density(D)

    return D, dens    
    

def weighted_density(g):
    W = 0

    for node in g.nodes():
        for edge in g.edges(node):
            W += g.get_edge_data(*edge)['weight']

    W = W/2
    
    return W/len(g.nodes())

        
        

        
        
