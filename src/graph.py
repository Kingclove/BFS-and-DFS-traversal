"""Module to support simple graph abstraction.  The Graph class is a simple
wrapper for a dictionary in which node names map to their adjacency lists.
"""

class Graph:
    def __init__(self, d):
        """Convert given dictionary into an adjacency list"""
        self.nbhds = d
        self.vertices = d.keys()

    def size(self):
        return len(self.vertices)

    def isEdge(self, u, v):
        return v in self.nbhds[u]

    def nbrs(self, u):
        return self.nbhds[u]

    def nodes(self):
        return self.vertices
