"""Algorithms for processing graphs discussed in lectures and tutorials"""

import Queue
import graph
import traversal

import forest

def dfs(g, u):
    """Visit all the nodes of g, starting from u, in a DFS manner"""
    result = traversal.Traversal(g)
    dfsVisit(g, u, result)
    for v in g.nodes():
        if not result.isVisited(v):
            dfsVisit(g, v, result)
    return result

def dfsVisit(g, u, result):
    """DFS visit connnected component of g containing u, starting from u"""
    # result.markStart(u)
    result.visit(u)
    for v in g.nbrs(u):
        if not result.isVisited(v):
            result.discover(v, u)
            # do anything related to edge (u,v)
            dfsVisit(g, v, result)
    result.markFinish(u)

def bfs(g, u):
    """Perform a BFS on g starting from u"""
    discovery = Queue.Queue(maxsize=0)
    result = traversal.Traversal(g)
    result.visit(u)
    for neigh in g.nbrs(u):
        if result.isUnseen(neigh):
            result.discover(neigh,u)
            discovery.put(neigh)
    while not discovery.empty():
        work = discovery.get()
        result.visit(work);
        for x in g.nbrs(work):
            if result.isUnseen(x):
                result.discover(x,work)
                discovery.put(x)
    

    return result

def tester():
    g = graph.Graph({'a':['b', 'c', 'd'], 'b':['c', 'e', 'f'], 'c':['d', 'e'],
                     'd':['b', 'f'], 'e':['a'], 'f':['c', 'a']})
    dt = dfs(g, 'a')
    f = dt.makeForest()
    poop = f.getMaxDepth()
    print poop
