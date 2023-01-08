import sys
from queue import Queue
from Graph import Graph
from Graph import Vertex
from PriorityQueue import PriorityQueue

class ISPNetwork:    # Class that holds graphs for the network
    def __init__(self, network = None, MST = None):
        self.network = network  # holding the graph for the network
        self.MST = MST  # holding the Minimum spanning tree

    def buildGraph(self, filename: str) -> None:  # function to store graph as network class attribute
        Graph1 = Graph()   # create graph instance
        file = open(filename, 'r').readlines()
        for line in file:
            connection = [x.strip() for x in line.split(",")]
            Net1 = connection[0]
            Net2 = connection[1]
            dist = connection[2]
            Graph1.addEdge(Net1,Net2,float(dist))   # add bi-directional edges for each connection
            Graph1.addEdge(Net2,Net1,float(dist))
        self.network = Graph1
        return

    def pathExist(self, router1: str, router2: str) -> bool: # function to determine if a path between two nodes exists
        for i in self.network:    # resetting attributes for color, pred and distance
            i.color = 'white'
            i.setPred(None)
            i.setDistance(0)
        if router1 not in self.network.vertList.keys():  # check if router1 vertex exists
            return False
        if router2 not in self.network.vertList.keys():  # check if router1 vertex exists
            return False
        else:
            r1 = self.network.getVertex(router1)  # get vertex of router1
            r2 = self.network.getVertex(router2)  # get vertex of router2
            vertQueue = Queue()       # create queue
            vertQueue.put(r1)         # put r1 in queue
            while (vertQueue.qsize)() > 0 and r1.id in self.network.vertList.keys(): # while queue not empty
                currentVert = vertQueue.get()        # get the first item
                for nbr in currentVert.getConnections():
                    if nbr == r2:    # check to see if popped vertex connected to r2
                        return True
                    if (nbr.getColor() == 'white'):  # if hasn't been searched
                        nbr.setColor('gray')      # set to searched color
                        vertQueue.put(nbr)      # add it to queue
                currentVert.setColor('black')     # set checked vertex to black
            return False        # when queue is empty, and r1 != r2, return False

    def buildMST(self):      # function to build minimum spanning tree
        start =  list(self.network.vertList.values())[0]       # choosing first vertex to make tree
        NG = Graph()       # creating graph object
        for i in self.prim(start):     # calling prim function to create MST
            if i.pred == None:  # checking each Vertex has pred
                continue
            else:      # creating edges in our graph object with the MST attributes
                NG.addEdge(i,i.pred,i.dist)
                NG.addEdge(i.pred,i,i.dist)
                NG.getVertex(i).setPred(i.pred)
                NG.getVertex(i).setDistance(i.dist)
        self.MST = NG     # set our graph instance to ISP Network MST attribute
        return

    def prim(self, start):   # Function used to create MST
        G = self.network
        pq = PriorityQueue()
        for v in G:   # initializing values
            v.setDistance(sys.maxsize)
            v.setPred(None)
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in G])
        while not pq.isEmpty():
            currentVert = pq.delMin()  # getting min item in pq
            for nextVert in currentVert.getConnections():
                newCost = currentVert.getWeight(nextVert)
                if nextVert in pq and newCost < nextVert.getDistance():  # if in pq and weight less than distance
                    nextVert.setPred(currentVert)     # set pred to current
                    nextVert.setDistance(newCost)    # set distance to weight
                    pq.decreaseKey(nextVert, newCost)   # decrease key
        return G

    def findPath(self, router1: str, router2: str):
        start = None   # initialze start and end to none
        end = None
        for i in self.MST.vertList:  # initialize vertex attributes in MST
            i.color = 'white'
            i.setPred(None)
            i.setDistance(0)
        for i in self.MST.vertList:   # find router1 and router2 vertex
            if i.id == router1:
                start = i
            if i.id == router2:
                end = i
        if start == None or end == None:  # if neither exist, return not exist
            return "path not exist"
        return self.bfs(start,end)     # return BFS with vertices found above

    def bfs(g, start,end):     # function used to find and hold path
        for i in g.MST:             # initialize vertex attributes
            i.color = 'white'
            i.setPred(None)
            i.setDistance(0)
        path = []   # create empty path list
        start.setDistance(0)
        start.setPred(None)
        vertQueue = Queue()
        vertQueue.put(start)   # put start into queue
        while (vertQueue.qsize() > 0):    # while queue is not empty
            currentVert = vertQueue.get()   # pop vertex
            for nbr in currentVert.getConnections():    # check each neighbor to vertex
                if (nbr.getColor() == 'white'):  # if unvisited
                    nbr.setColor('gray')   # set to visited
                    nbr.setPred(currentVert)
                    vertQueue.put(nbr)    # add to queue
                if nbr == end:       # if nbr == end, than path exists
                    while nbr != start:  # backtrack from nbr
                        path.append(nbr.id)   # append to path list until nbr = start
                        nbr = nbr.pred
                    final = ""   # create empty string
                    path.append(start.id)    # add start id
                    for v in range(1, len(path)):  # for loop to add path values to final string
                        final = path[v] + " -> " + final
                    final = final + "" + path[0]
                    return final  # return final string
            currentVert.setColor('black')   # if nbr's checked, set vertex to black
        return "path not exist"  # if all vertices are black, path not exist

    def findForwardingPath(self, router1:str,router2:str):  # function to find path with total link weight
        for i in self.network:  # initialize vertex attributes for each vertex in network
            i.color = 'white'
            i.setPred(None)
            i.setDistance(sys.maxsize)
        start = self.network.getVertex(router1)  # get router1 and router2 vertices
        end = self.network.getVertex(router2)
        if start == None or end == None:  # if router1 or 2 not found, return not exist
            return 'path not exist'
        path = []  # create path list
        cost = 0  # initialize cost to 0
        pq = PriorityQueue()   # create priority queue
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in self.network])
        while not pq.isEmpty():
            currentVert = pq.delMin()   # get min value
            for nextVert in currentVert.getConnections():  # for each neighbor
                newDist = currentVert.getDistance() \
                          + currentVert.getWeight(nextVert) # if current.dist + weight
                if newDist < nextVert.getDistance():  # if less than nextvert.dist
                    nextVert.setDistance(newDist)    # set to newdist
                    nextVert.setPred(currentVert)    # set pred to current
                    pq.decreaseKey(nextVert, newDist)  # decrease key
        while end != start and end != None:  # while loop to add path to pathlist
            if end == None:
                return "path not exist"
            else:
                path.append(end.id)
                dist = end.connectedTo[end.pred]
                cost = cost + dist
                end = end.pred
        if end == start:  # used to create final string
            final = ""
            path.append(start.id)
            for v in range(1, len(path)):
                final = path[v] + " -> " + final
            final = final + "" + path[0] + " (" + str(cost) + ")"

            return final   # return final string if end == start
        return "path not exist"  # else, return path not exist

    def findPathMaxWeight(self, router1:str,router2:str):   # function to return min path with max single link weight
        for i in self.network:  # initialize vertices
            i.color = 'white'
            i.setPred(None)
            i.setDistance(sys.maxsize)
        start = self.network.getVertex(router1)  # get vertex for router1 and router2
        end = self.network.getVertex(router2)
        if start == None or end == None:  # if none, r1 or r2 doesnt exist
            return 'path not exist'
        path = []  # create empty path list
        pq = PriorityQueue()   # create priority queue
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in self.network])
        while not pq.isEmpty():   # while pq not empty
            currentVert = pq.delMin()    # get min vertex
            for nextVert in currentVert.getConnections():  # for every neighbor
                newDist = max(currentVert.getDistance(), currentVert.getWeight(nextVert)) # max(current.dist, weight)
                if nextVert.getDistance() > newDist:  # checking if this has larger link
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert, newDist)
        while end != start and end != None:  # while loop to create path list
            if end == None:
                return "path not exist"
            else:
                path.append(end.id)
                end = end.pred
        if end == start:
            final = ""
            path.append(start.id)
            for v in range(1, len(path)):
                final = path[v] + " -> " + final
            final = final + "" + path[0]

            return final
        return "path not exist"


if __name__ == "__main__":
    Net = ISPNetwork()
    Net.buildGraph("3967.csv")
    Net.network.getVertices()
    print(Net.pathExist("ChicagoIL155","Santa+ClaraCA443"))
    Net.buildMST()
    #print(Net.findPath("TukwilaWA509","Santa+ClaraCA443"))

    #print(Net.findPath("TukwilaWA509","Santa+ClaraCA443"))
    print(Net.findForwardingPath("ChicagoIL155","Santa+ClaraCA443"))
    print(Net.findPathMaxWeight("ChicagoIL155","Santa+ClaraCA443"))

'''
    g = Graph()
    g.addEdge('A','F',4)
    g.addEdge('A','E',100)
    g.addEdge('D','E',200)
    g.addEdge('F','D',5)
    g.addEdge('C','F',1)
    g.addEdge('B','C',2)
    g.addEdge('B','E',3)

    g.addEdge('F', 'A', 4)
    g.addEdge('E', 'A', 100)
    g.addEdge('E', 'D', 200)
    g.addEdge('D', 'F', 5)
    g.addEdge('F', 'C', 1)
    g.addEdge('C', 'B', 2)
    g.addEdge('E', 'B', 2)
    Net.network = g
    Net.buildMST()
    Net.findPath('A','E')
'''