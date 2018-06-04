from pythonds.graphs import Graph,Vertex
from pythonds.basic import Queue

import csv

def buildGraph(filename):
    movieDict = {}
    # actorDict = {} # probably not needed, mainly for testing numVertices vs num of Actors
    graph = Graph()

    with open(filename, 'r') as f:
        moviereader = csv.reader(f, delimiter='|')
        for row in moviereader:
            actor = row[1]
            movie = row[0]
            if movie in movieDict:
                movieDict[movie].append(actor)
            else:
                movieDict[movie] = [actor]

    for movie in movieDict.keys():
        for actor1 in movieDict[movie]:
            for actor2 in movieDict[movie]:
                if actor1 != actor2:
                    graph.addEdge(actor1, actor2, movie)

    return graph

def bfs(start):
    start.setDistance(0)
    start.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(start)
    while (vertQueue.size() > 0):
        currentVert = vertQueue.dequeue()
        for nbr in currentVert.getConnections():
            if (nbr.getColor() == 'white'):
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)
        currentVert.setColor('black')

def traverse(y):
    x = y
    print("The Kevin Bacon Number for", x.getId(), "is", x.getDistance())
    while (x.getPred()):
        print(x.getId(), "acted with", x.getPred().getId(), "in", x.getWeight(x.getPred()))
        x = x.getPred()
    print("\n")

def main():
    g = buildGraph('movie_actors.csv')
    actorName = input(str("What Actor would you like to trace? (exit to quit)  "))
    bfs(g.getVertex('Kevin Bacon'))
    while actorName != "exit":
        if g.getVertex(actorName) != None:
            traverse(g.getVertex(actorName))
        else:
            print("Actor name may be spelt wrong or not in graph")
        actorName = input(str("What Actor would you like to trace? (exit to quit)  "))


main()