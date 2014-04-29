"""Module to support various graph traversal algorithms.

The Clock class maintains a counter that is automatically incremented
whenever it is read.  It also supports being reset.

The Traversal class maintains all the information that is needed by the common
traversals (e.g. BFS and DFS).  The Traversal class also provides functions
for producing a tree of the traversal carried out, which is reconstructed from
the edges used to visit each node over the course of the traversal.
"""

import forest

class Clock():
    """The Clock class maintains a non-local counter that is updated
    automatically every time it is read with the getTime() function.  It is
    intended to be used with a graph traversal that maintains an ordering on
    the start and completion of the visit process for each node.
    """
    def __init__(self):
        """Initialise the clock to read zero"""
        self.time = 0

    def getTime(self):
        """Return the current reading on the clock, and as a side effect
        advance the clock by 1 after reading it.
        """
        result = self.time
        self.time = self.time + 1
        return result

    def reset(self):
        """Reset the clock counter to 0."""
        self.time = 0
        return self.time

# statuses used to mark nodes during a traversal
UNSEEN = 0
VISITED = 1
DISCOVERED = 2

class Traversal:
    status = {}                 # node statuses (UNSEEN, DISCOVERED, VISITED)
    src = {}                    # 'v' --> 'u' means visited v from u
    start = {}                  # start times  ('v' --> int)
    finish = {}                 # finish times ('v' --> int)
    sequence = []               # order in which nodes were visited

    def __init__(self, g):
        self.clock = Clock()
        self.reset(g)

    def reset(self, g):
        self.clock.reset()
        self.status = {}
        self.src = {}
        self.start = {}
        self.finish = {}
        self.sequence = []
        for v in g.nodes():
            self.status[v] = UNSEEN
            self.src[v] = None

    def discover(self, v, u):
        """Discover node v from node u.  All appropriate variables to
        represent this are updated here.
        """
        self.status[v]= DISCOVERED
        self.src[v] = u

        pass

    def visit(self, v):
        """Visit node v.  All appropriate variables of the traversal process
        are updated here.
        """
        self.status[v] = VISITED
        self.markStart(v)
        self.sequence.append(v)
        if  self.src[v] == None:
            self.src[v]= self.findSource(v);
        
    def findSource(self,v):
        if self.start[v]==0:
            return None

        y= self.start[v] -1
       
        for key in self.start:
            
            if self.start[key]==y:
                return key

        for key in self.finish:
            if self.finish[key]==y:
                return self.src[key]

        return None

         
        

    def isVisited(self, v):
        """Return True if the status of v is VISITED"""
        if self.status[v]== VISITED:
            return True
        else:
            return False
        

    def isDiscovered(self, v):
        """Return True if the status of v is DISCOVERED"""
        if self.status[v]== DISCOVERED:
            return True
        else:
            return False
    

    def isUnseen(self, v):
        """Return True if the status of v is UNSEEN"""
        if self.status[v]== UNSEEN:
            return True
        else:
            return False

    def isStatus(self, v, status):
        """Return True if the current status of v is the same as the given
           status
        """
        if self.status[v] == status:
            return True
        else:
            return False

    def markStart(self, v):
        """Set the start time for v to the time on the clock."""
        self.start[v]=self.clock.getTime()
        pass

    def markFinish(self, v):
        """Set the finish time for v to the time on the clock."""
        self.finish[v]=self.clock.getTime()
        pass

    def makeForest(self):
        """Create a forest, represented as a collection of roots and a
        dictionary of children, from the information contained in the
        src array."""
        children = {}
        roots = []
        for v in self.src.keys():
            children[v] = []
            
        for (u, v) in self.src.items():
            if v == None:
                roots.append(u)
            else:
                children[v].append(u)

        return forest.Forest(roots, children)

    def showTree(self, nodeSize=20, leafSpacing=50, levelSpacing=50):
        f = self.makeForest()
        f.draw(nodeSize, leafSpacing, levelSpacing)

    def printTree(self):
        """Output a text representation of the tree"""
        print "Sequence: %s" % self.sequence
        print "Sources:  %s" % self.src

    def __str__(self):
        return str(self.sequence) + "\n" + str(self.src)


