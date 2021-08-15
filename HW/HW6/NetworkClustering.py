import sys
import Dijkstra
import Graph
import Prim
import TreeBalancing

class NewmanClustering:

    def __init__(self):
        pass

    def performNewmanClustering(self, graph, K):
        lstVertices = graph.vertices

        print("-------------------------------")
        print("Initial Dataset")
        graph.printComponent()

        cnt = 0
        while True:
            matBetweenness = self.calculateEdgeBetweenness(graph)
            maxBetweenness = 0.0
            idxSrcEdge = -1
            idxDstEdge = -1
			
            for itr1 in range(len(lstVertices)):
                for itr2 in range(len(lstVertices)):
                    if matBetweenness[lstVertices[itr1]][lstVertices[itr2]] > maxBetweenness:
                        maxBetweenness = matBetweenness[lstVertices[itr1]][lstVertices[itr2]]
                        idxSrcEdge = itr1
                        idxDstEdge = itr2

            graph.removeEdge(lstVertices[idxSrcEdge],lstVertices[idxDstEdge])
            graph.removeEdge(lstVertices[idxDstEdge],lstVertices[idxSrcEdge])
            components = graph.findComponent()
            print("-------------------------------")
            print("Iteration "+str(cnt))
            graph.printComponent()
            if len(components) == K:
                break
            cnt = cnt + 1

    def calculateEdgeBetweenness(self, graph):
        lstVertices = graph.vertices
        matBetweenness = {}
        for itr1 in range(len(lstVertices)):
            matBetweenness[lstVertices[itr1]] = {}
            for itr2 in range(len(lstVertices)):
                matBetweenness[lstVertices[itr1]][lstVertices[itr2]] = 0.0

        print("Calculating Betweenness ")
        for itr1 in range(len(lstVertices)):
            print(".",end="")
            sys.stdout.flush()
            dist, path, routes = Dijkstra.performAllDestinationDijkstra(graph, lstVertices[itr1])
            for itr2 in range(len(lstVertices)):
                if itr1 == itr2:
                    continue
                if routes[lstVertices[itr2]] != None:
                    for itr3 in range(len(routes[lstVertices[itr2]])-1):
                        srcIncludedEdge = routes[lstVertices[itr2]][itr3]
                        dstIncludedEdge = routes[lstVertices[itr2]][itr3+1]
                        matBetweenness[srcIncludedEdge][dstIncludedEdge] = matBetweenness[srcIncludedEdge][dstIncludedEdge] + 1
                        matBetweenness[dstIncludedEdge][srcIncludedEdge] = matBetweenness[dstIncludedEdge][srcIncludedEdge] + 1
        print()
        return matBetweenness

    def makeMSTforCompoent(self, graph):
        components=graph.findComponent()
        for itr in range(len(components)):
            print("-------------------------------")
            print(str(itr+1)+". Component of",components[itr])
            Prim.performPrim(graph, components[itr][0])
            TreeBalancing.performTreeBalancing(graph, components[itr])


if __name__ == "__main__":
    #g = Graph.DenseGraph('Subway-Seoul-ver-2.csv')
    g = Graph.DenseGraph('Subway-Seoul.csv')
    clustering = NewmanClustering()
    clustering.performNewmanClustering(g,10)
    clustering.makeMSTforCompoent(g)