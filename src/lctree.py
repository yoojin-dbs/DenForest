import splaytree

# Link-Cut Tree Node
class Node:
    def __init__(self, x, y, T):
        self.parent = None        
        self.left = None
        self.right = None
        
        self.flip = False
        
        self.x = x
        self.y = y
        self.T = T

        self.label = ''
        self.Tc = 0
    
# Link-Cut Tree Edge
class Edge:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.weight = 0
        
# find the root of the tree
def FindRoot(n):
    Access(n)
    while n.left != None:
        n = n.left
    splaytree.Splay(n)
    return n

# check if a path exists between nodes n and m
def Connected(n, m):
    if FindRoot(n) == FindRoot(m):
        return True
    else:
        return False

# find lowest common ancestor of two nodes
def LCA(n, m):
    Access(n)
    return Access(m)

# link n to link-cut tree's root with chain
def Access(n):
    splaytree.Splay(n)
    n.right = None
    
    res = n
    
    while n.parent != None:
        m = n.parent
        res = m
        splaytree.Splay(m)
        m.right = n
        splaytree.Splay(n)

    return res

# link nodes n and m in different trees
def Link(n, m, edgeTable):
    if Connected(n, m) == True:
        return
    
    Access(n)
    Access(m)
    n.left = m
    m.parent = n
    
    # add edge n to m to the edgeTable
    edge1 = Edge(n, m)
    edge1.weight = min(n.Tc, m.Tc)
    
    if n in edgeTable:
        edgeTable[n].append(edge1)
    else:
        edgeTable.update({n:[edge1]})
    
    # add edge m to n to the edgeTable
    edge2 = Edge(m, n)
    edge2.weight = min(m.Tc, n.Tc)
    
    if m in edgeTable:
        edgeTable[m].append(edge2)
    else:
        edgeTable.update({m:[edge2]})

# cut a link between nodes n and m
def Cut(n, m, edgeTable):
    Access(n)
    Access(m)
    
    m.left = None
    n.parent = None
    
    # delete edge n to m from the edge table
    for edge in edgeTable[n]:
        if edge.m == m:
            edgeTable[n].remove(edge)
                
    if not edgeTable[n]:
        edgeTable.pop(n)
    
    # delete edge m to n from the edge table
    for edge in edgeTable[m]:
        if edge.m == n:
            edgeTable[m].remove(edge)
            
    if not edgeTable[m]:
        edgeTable.pop(m)

# find the minimum weighted edge on the path between nodes n and m
def FindMinE(n, m, edgeTable):
    lca = LCA(n, m)
    Access(n)
    splaytree.Splay(lca)
    
    Access(m)
    
    minEdge = None
    if edgeTable.get(n) != None:
        minEdge = edgeTable[n][0]
    temp = n
    
    while temp.parent != None and edgeTable.get(temp) != None:
        for edge in edgeTable[temp]:
            if edge.m == temp.parent and edge.weight < minEdge.weight:
                minEdge = edge
        temp = temp.parent
    
    splaytree.Splay(lca)
    
    return minEdge