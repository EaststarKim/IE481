import queue

def performPrim(graph, src):
    dist = {}
    path = {}
    order = {}
    vertices = []
    edges = {}
    pqueue = queue.PriorityQueue()
    for itr in range(len(graph.vertices)):
        dist[graph.vertices[itr]] = 99999999
        path[graph.vertices[itr]] = None
        order[graph.vertices[itr]]=itr
        edges[graph.vertices[itr]]={}
    dist[src] = 0
    pqueue.put([0,order[src],src])

    while pqueue.empty()==False:
        minDist, tmp, min_vertex = pqueue.get()
        if minDist!=dist[min_vertex]:
            continue
        vertices.append(min_vertex)
        if min_vertex!=src:
            edges[path[min_vertex]][min_vertex]=edges[min_vertex][path[min_vertex]]=\
                graph.edges[path[min_vertex]][min_vertex]
        neighbors, weights = graph.getNeighbors(min_vertex)
        for itr in range(len(neighbors)):
            if dist[neighbors[itr]] > minDist + weights[itr]:
                dist[neighbors[itr]] = minDist + weights[itr]
                path[neighbors[itr]] = min_vertex
                pqueue.put([dist[neighbors[itr]],order[neighbors[itr]],neighbors[itr]])

    for vertex1 in vertices:
        for vertex2 in vertices:
            if vertex2 in graph.edges[vertex1]:
                graph.removeEdge(vertex1,vertex2)
        for vertex2 in edges[vertex1].keys():
            graph.addEdge(vertex1,vertex2,edges[vertex1][vertex2])

    return dist