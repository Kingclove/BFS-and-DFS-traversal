"""Module to test the functionality of the BFS and DFS traversals, and
 display the respective trees."""

import random
from graph_algs import dfs, bfs
import graph

def test():
    g = graph.Graph({'a':['b','c', 'g','h'], 'b':['a', 'c', 'd','g','h'], 'c':['a','b', 'd','e'],
                     'd':['b', 'c','f'], 'e':['c','f','h'], 'f':['d', 'e','g','h'], 'g':['a', 'b','f'], 'h':['a','b', 'e','f']})
    print "Graph: %s" % g.nbhds
    print "Running DFS..."
    dt = dfs(g, 'a')
    dt.printTree()
    dt.showTree()
    print "Running BFS..."
    bt = bfs(g, 'a')
    bt.printTree()
    bt.showTree()
    print "Traversals completed!"

if __name__ == '__main__':
    test()
