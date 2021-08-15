import queue

def performAllDestinationDijkstra(graph, src):
    dist = {}
    path = {}
    routes = {}
    order = {}
    pqueue = queue.PriorityQueue()
    for itr in range(len(graph.vertices)):
        dist[graph.vertices[itr]] = 99999999
        path[graph.vertices[itr]] = None
        order[graph.vertices[itr]]=itr
    dist[src] = 0
    pqueue.put([0,order[src],src])

    while pqueue.empty()==False:
        minDist, tmp, min_vertex = pqueue.get()
        if minDist!=dist[min_vertex]:
            continue
        neighbors, weights = graph.getNeighbors(min_vertex)
        for itr in range(len(neighbors)):
            if dist[neighbors[itr]] > minDist + weights[itr]:
                dist[neighbors[itr]] = minDist + weights[itr]
                path[neighbors[itr]] = min_vertex
                pqueue.put([dist[neighbors[itr]],order[neighbors[itr]],neighbors[itr]])

    for vertex in graph.vertices:
        next = vertex
        temp = [next]
        while next != src:
            next = path[next]
            if next == None:
                temp = None
                break
            temp = [next] + temp
        routes[vertex] = temp

    return dist, path, routes


