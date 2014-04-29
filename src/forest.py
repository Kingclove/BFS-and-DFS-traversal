import Tkinter

class Forest:
    roots = []            # list of nodes that have no tree parent
    children = {}         # node :--> list of tree children
    bounds = {}           # lower and upper leaf indexes for each node
    depths = {}           # depth of each node

    def __init__(self, roots, children):
        self.roots = roots
        self.children = children
        self.computeAllLeafIndexes()

    def getNodes(self):
        """Return a list of all nodes in the tree"""
        nodeList = []
        nodeList.extend(self.roots)
        for key in self.children:
            nodeList.extend(self.children[key])

        return nodeList


    def getChildren(self, node):
        """Return the children of node as a list"""
        return self.children[node]

    def isLeaf(self, node):
        """Return True if the node is a leaf."""
        if self.children[node] :
            return False
        else:
            return True


    def getDepth(self, node):
        """Return the depth of the given node."""
        child = node
        count = 0
        parent= self.findParent(node)
        while  not parent== None:
            parent = self.findParent(parent)
            count = count +1
        return count

    def findParent(self,node):
        for parent in self.children.keys():
            if node in self.children[parent]:
                return parent
        else:
            return None

    def getMaxDepth(self):
        """Return the depth of the deepest tree"""
        nodeList = self.getNodes()
        leafList = []
        maximumDepth = 0
        for node in nodeList:
            if self.isLeaf(node):
                leafList.append(node)
        for leaf in leafList:
            depth = self.getDepth(leaf)
            if depth > maximumDepth:
                maximumDepth = depth
        return maximumDepth

    def computeAllLeafIndexes(self):
        """Determine the lower and upper leaf indexes for each subtree in
        each tree of this forest"""
        index = 0
        self.depths = {}
        self.bounds = {}
        self.maxDepth = self.getMaxDepth();
        for r in self.roots:
            index = self._computeTreeBounds(r, index, 0)
            index = index + 1
        self.width = index

    def _computeTreeBounds(self, root, start, depth):
        """Given the depth and lowest indexed leaf of a node,
        determine and store the maximum leaf index, and the maximum
        depth of the subtree rooted at it.  Return the index of its rightmost
        leaf.
        """
        self.depths[root] = depth;
        if self.isLeaf(root):
            self.bounds[root] = (start,start)
            return start
        y = start
        count =0
        for child in self.getChildren(root):
            y = self._computeTreeBounds(child,y+count,depth+1) ;
            count=1

        self.bounds[root] = (start,y)
        return y

    def getPositions(self, leafSpacing, levelSpacing, ox=0, oy=0):
        """Compute the coordinates of each node based on the bounds of
        each node, its level in the tree, and the given spacings.  All
        coordinates will be offset by (ox, oy) (added as a
        displacement).  Return the set of coordinates as a dictionary
        mapping nodes to coordinates.

        This will generate a tree that grows downwards (deeper levels in the
        tree have larger y coordinates).
        """
        calpositions ={};
        for b in self.getNodes():
            x = (((self.bounds[b][0]+self.bounds[b][1])/2.0)*leafSpacing) + ox
            y = (self.depths[b]*levelSpacing) + oy
            calpositions[b]=(x,y)
        return calpositions

    def draw(self, nodeSize, leafSpacing, levelSpacing):
        """Render an image of the tree with the given sizing dimensions
        """
        # make a window big enough to hold the tree + margins
        window = Tkinter.Tk()
        canvas = Tkinter.Canvas(window,
                                width=leafSpacing * (self.width + 2),
                                height = levelSpacing * (self.maxDepth + 2))
        
        canvas.pack()
        positions = self.getPositions(leafSpacing, levelSpacing,
                                      nodeSize+leafSpacing,
                                      levelSpacing)
        for node in self.roots:
            self.drawTree(node, positions, canvas, nodeSize)
        canvas.mainloop()

    def _drawNode(self, node, positions, canvas, size):
        (x,y) = positions[node]
        r = size/2
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="green")
        text = canvas.create_text(x, y, text=str(node))

    def _drawEdge(self, src, dest, positions, canvas, size):
        (sx, sy) = positions[src]
        (dx, dy) = positions[dest]
        canvas.create_line(sx, sy, dx, dy, fill = "red")

    def drawTree(self, root, positions, canvas, nodeSize):
        """Draw the tree rooted at root on given canvas at given size.
        positions[node] ==> (x, y) # centre of node
        """
        for child in self.getChildren(root):
            self._drawEdge(root, child, positions, canvas, nodeSize)
            self.drawTree(child, positions, canvas, nodeSize)
        self._drawNode(root, positions, canvas, nodeSize)
