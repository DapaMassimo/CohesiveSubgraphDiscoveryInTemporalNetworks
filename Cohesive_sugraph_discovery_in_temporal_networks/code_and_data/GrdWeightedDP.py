import networkx as nx
import numpy as np
from charikar_heap_weighted import charikarHeapWeighted
from goldberg_weighted import get_solution
import time

def GrdWeightedDP(k, timestamps):
    start_time = time.time()
    sorted_keys = sorted(timestamps.keys())
    m = len(timestamps)
    DP = np.full((k, m), -1.0, dtype='float')
    C = np.full((k, m), -1, dtype='int')
    
    #base case
    AD = {}
    for i in range(0,m):
        for (n1, n2) in timestamps[sorted_keys[i]]:
            if (n1, n2) not in AD:
                AD[(n1,n2)] = 0
            AD[(n1, n2)] += 1 
        edge_freq = [(*key, AD[key]) for key in AD]
        g = nx.Graph()
        g.add_weighted_edges_from(edge_freq)
        DP[0,i] = round(charikarHeapWeighted(g)[1]/(i+1), 8)
        C[0,i] = 0
        
    #recurrence
    for l in range(1, k):
        #print('row %d' % (l))
        for i in range(l, m):
            #print('row: %d, col: %d' % (l, i))
            best = -1
            idx = -1
            for j in range(l-1, i):
                #gather the edges with relative occurrences
                AD = {}
                for t in range(j+1, i+1):
                    for (n1, n2) in timestamps[sorted_keys[t]]:
                        if (n1, n2) not in AD:
                            AD[(n1, n2)] = 0
                        AD[(n1, n2)] += 1
                edge_freq = [(*key, AD[key]) for key in AD]

                g = nx.Graph()
                g.add_weighted_edges_from(edge_freq)
                choice = DP[l-1, j] + charikarHeapWeighted(g)[1]/(i-(j+1)+1)
                
                if choice >= best:
                    best = choice
                    idx = j+1 #index starting the newfound interval
                    
            DP[l, i] = round(best, 8)
            C[l, i] = idx
    
    running_time = (time.time() - start_time)
    print('running time of %d rows (seconds): %s' %(k, running_time))
    return DP,C

#%%
def get_sol_intervals(c, k, m):
    """
    c : c matrix returned from GrdWeightedDP
    k : c.shape[0]
    m : c.shape[1]
    """
    starts = []
    j = m-1
    
    for i in range(k-1, -1, -1):
        cut = int(c[i][j])
        starts.append(cut)
        j = cut - 1
        if j <0:
            break
        
    starts = starts[::-1]
    intervals = []
    for s in range(len(starts)-1):
        intervals.append((starts[s],starts[s+1]-1))
        
    intervals.append((starts[len(starts)-1], m-1))    
    
    return intervals

#%%
def get_sol_graphs(intervals, ts):
    sorted_keys = sorted(ts.keys())
    results = []

    for (l, r) in intervals:
        
        AD = {}
        for i in range(l, r+1):
            for (n1, n2) in ts[sorted_keys[i]]:
                if (n1, n2) not in AD:
                    AD[(n1, n2)] = 0
                AD[(n1, n2)] += 1
                
        edge_freq = [(*key, AD[key]) for key in AD] 
        g = nx.Graph()
        g.add_weighted_edges_from(edge_freq)
        
        gold = get_solution(g)
        subgraph = gold[0]
        dens = gold[1]/(r-l+1)
        dens = round(dens, 8)
        
        results.append((subgraph, dens))
        
    return results

#%%
def GrdWeightedDP_keep_going(dp, c, k_left, timestamps):
    """
    If initially GrdWeightedDP was called with k=3 for example, and now I 
    want it with k=5, I don't have to start from scratch.
    In this example I would call this function with: (dp_k3, c_k3, 2, ts)
    """
    sorted_keys = sorted(timestamps.keys())
    m = len(timestamps)
    DP = np.full((k_left, m), -1.0, dtype='float')
    C = np.full((k_left, m), -1, dtype='int')
    
    DP = np.concatenate((dp, DP), axis=0)
    C = np.concatenate((c, C), axis=0)
    
    start_time = time.time()
    #recurrence
    for l in range(dp.shape[0], dp.shape[0] + k_left):
        for i in range(l, m):
            print('row: %d, col: %d' % (l, i))
            best = -1
            idx = -1
            for j in range(l-1, i):
                #gather the edges with relative occurrences
                AD = {}
                for t in range(j+1, i+1):
                    for (n1, n2) in timestamps[sorted_keys[t]]:
                        if (n1, n2) not in AD:
                            AD[(n1, n2)] = 0
                        AD[(n1, n2)] += 1
                        
                edge_freq = [(*key, AD[key]) for key in AD]
                g = nx.Graph()
                g.add_weighted_edges_from(edge_freq)
                choice = DP[l-1, j] + charikarHeapWeighted(g)[1]/(i-(j+1)+1)
                
                if choice >= best:
                    best = choice
                    idx = j+1 #index starting the newfound interval
                    
            DP[l, i] = round(best, 8)
            C[l, i] = idx
    
    running_time = (time.time() - start_time)
    print('REMEMBER TO ADD THE RUNNING TIME FOR THE FIRST %d ROWS' % (dp.shape[0]))
    print('running time of %d rows (seconds): %s' %(k_left,running_time))
    return DP,C
        