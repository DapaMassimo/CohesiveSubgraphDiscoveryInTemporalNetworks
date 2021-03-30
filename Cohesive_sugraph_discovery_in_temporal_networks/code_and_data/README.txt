Code implementation of algorithms described in:
"Cohesive subgraph discovery in temporal networks", undergrad thesis of Massimo D'Apa.
-------------------------------------------------------------------------------------------------------------
The 'data' folder contains the real-world datasets used to test the algorithms
-------------------------------------------------------------------------------------------------------------
The code in 'fib_heap_mod.py' was taken from: https://github.com/danielborowski/fibonacci-heap-python

The code was not working correctly, so I've made the following changes:

    - getter methods for key and value in Node class.
    
    - __bool__ method for the FibonacciHeap class.
     
    - comparison with <= instead of just < in the last cicle of function
      consolidate.

    - pointer setting: self.root_list = self.min_node at the end of function
      consolidate.
      
    - the size of A[d] is set to:
      A = [None] * int(math.log(self.total_nodes) * 2.08 + 1)
-------------------------------------------------------------------------------------------------------------
All the code was run on 64bit machines with the following versions:
    - Python 3.7.3
    - networkx 2.3
    - numpy 1.16.4
