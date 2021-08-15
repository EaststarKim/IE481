
def computeMaxDepth(graph, node, parent):
    children, weights = graph.getNeighbors(node)
    maxDepth=0
    for itr in range(len(children)):
        if children[itr]!=parent:
            maxDepth=max(maxDepth,computeMaxDepth(graph,children[itr],node)+weights[itr])

    return maxDepth

def performTreeBalancing(graph, component):
    root = ""
    answer = 99999999
    for node in component:
        subDepth=computeMaxDepth(graph,node,"")
        if answer>subDepth:
            answer=subDepth
            root=node

    print("Local Supply Tree")
    printMST(graph,root,"","")
    print("Max. Depth =",float(answer))

def printMST(graph, node, parent, level):
    print(level+node)
    children, weights = graph.getNeighbors(node)
    for child in children:
        if child!=parent:
            printMST(graph,child,node,level+"....")