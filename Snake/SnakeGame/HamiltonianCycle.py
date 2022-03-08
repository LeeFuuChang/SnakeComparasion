from .globals import *

import random





def dist(x1, y1, x2, y2):
    a = abs(x1-x2)
    b = abs(y1-y2)
    return (a**2 + b**2)**(1/2)


def getLeftOf(d):
    if(d.x == 0 and d.y == 1):
        x, y = 1, 0
    elif(d.x == 0 and d.y == -1):
        x, y = -1, 0
    elif(d.x == 1):
        x, y = 0, -1
    else:
        x, y = 0, 1
    return Point(x, y, [])


def getRightOf(d):
    if(d.x == 0 and d.y == 1):
        x, y = -1, 0
    elif(d.x == 0 and d.y == -1):
        x, y = 1, 0
    elif(d.x == 1):
        x, y = 0, 1
    else:
        x, y = 0, -1
    return Point(x, y, [])





class HNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spanningTreeAdjacentNodes = []
        self.cycleNo = -1

        #A* vars
        self.alreadyVisited = False
        self.shortestDistanceToThisPoint = 0


    def setEdges(self, allNodes):
        self.edges = [n for n in allNodes if dist(n.x, n.y, self.x, self.y)==1]


    def setSpanningTreeEdges(self, spanningTree):
        for e in spanningTree:
            if e.contains(self):
                self.spanningTreeAdjacentNodes.append(e.getOtherNode(self))


    def getNextNodeMovingLeft(self, previousNode):
        direction = previousNode.getDirectionTo(self)

        possibleDirections = []
        for n in self.spanningTreeAdjacentNodes:
            possibleDirections.append(self.getDirectionTo(n))

        checkingDirection = getLeftOf(direction);
        while(checkingDirection not in possibleDirections):
            checkingDirection = getRightOf(checkingDirection);
        return self.spanningTreeAdjacentNodes[possibleDirections.index(checkingDirection)];


    def getDirectionTo(self, other):
        return {"x":other.x - self.x, "y":other.y - self.y}


    def resetForAStar(self):
        self.alreadyVisited = False;
        self.shortestDistanceToThisPoint = 0;





class HEdge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2


    def isEqualTo(self, otherEdge):
        return (self.node1 == otherEdge.node1 and self.node2 == otherEdge.node2) or (self.node1 == otherEdge.node2 and self.node2 == otherEdge.node1)


    def contains(self, n):
        return (n == self.node1 or n == self.node2)


    def getOtherNode(self, n):
        if n == self.node1:
            return self.node2
        else:
            return self.node1


    def connectNodes(self):
        self.node1.spanningTreeAdjacentNodes.append(self.node2)
        self.node2.spanningTreeAdjacentNodes.append(self.node1)





class HPath:
    def __init__(self, startingNode, finishingNode):
        self.pathLength = 0
        self.nodesInPath = [startingNode]
        self.finishNode = finishingNode

        self.distanceToApple = 0
        self.setDistanceToApple()
        self.pathCounter = 0


    def setDistanceToApple(self):
        lastNode = self.getLastNode()
        self.distanceToApple = dist(self.finishNode.x, self.finishNode.y, lastNode.x, lastNode.y)


    def addToTail(self, node):
        self.nodesInPath.append(node)
        self.pathLength += 1
        self.setDistanceToApple()


    def getLastNode(self):
        return self.nodesInPath[-1]


    def getSnakeTailPositionAfterFollowingPath(self, snake):
        if(self.pathLength-snake.addCount < len(snake.tailBlocks)):
            return snake.tailBlocks[max(0, self.pathLength-snake.addCount)]
        tailMoved = self.pathLength-snake.addCount
        return self.nodesInPath[tailMoved-len(snake.tailBlocks)]


    def getNextMove(self):
        x = self.nodesInPath[self.pathCounter+1].x - self.nodesInPath[self.pathCounter].x;
        y = self.nodesInPath[self.pathCounter+1].y - self.nodesInPath[self.pathCounter].y;
        self.pathCounter += 1
        return (x, y)


    def clone(self):
        clone = HPath(self.nodesInPath[0], self.finishNode)
        clone.nodesInPath = self.nodesInPath[:]
        clone.pathLength = self.pathLength
        clone.distanceToApple = self.distanceToApple
        return clone





class HamiltonianCycle:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.createCycle()


    def createCycle(self):
        self.createSpanningTree()

        cycle = []
        cycleNodes = []

        for i in range(self.rows):
            for j in range(self.cols):
                cycleNodes.append(HNode(i, j))

        for n in cycleNodes:
            n.setEdges(cycleNodes)
        for i in range(len(self.spanningTreeNodes)):
            currentSpanningTreeNode = self.spanningTreeNodes[i]

            for other in currentSpanningTreeNode.spanningTreeAdjacentNodes:
                def connectNodes(x1, y1, x2, y2):
                    print(x1, y1, x2, y2)
                    if y1 + self.cols*x1 >= len(cycleNodes) or y2 + self.cols*x2 >= len(cycleNodes):
                        return
                    a = cycleNodes[y1 + self.cols*x1]
                    b = cycleNodes[y2 + self.cols*x2]
                    a.spanningTreeAdjacentNodes.append(b)
                    b.spanningTreeAdjacentNodes.append(a)

                direction = currentSpanningTreeNode.getDirectionTo(other)
                x = currentSpanningTreeNode.x*2
                y = currentSpanningTreeNode.y*2
                if direction["x"] == 1:
                    connectNodes(x+1, y  , x+2, y  )
                    connectNodes(x+1, y+1, x+2, y+1)
                elif direction["y"] == 1:
                    connectNodes(x  , y+1, x  , y+2)
                    connectNodes(x+1, y+1, x+1, y+2)

        # make a list of all the nodes which only have 1 adjacent node
        # then make a list of all the edges we need to add
        degree1Nodes = [n for n in cycleNodes if len(n.spanningTreeAdjacentNodes)==1]
        newEdges = []
        for n in degree1Nodes:
            # get the direction from the other node to this one
            d = n.spanningTreeAdjacentNodes[0].getDirectionTo(n)
            # add that direction again to get the next node
            d["x"] += n.x
            d["y"] += n.y
            print(len(cycleNodes), d["y"] + self.cols * d["x"])
            print(d, n, d["y"] + self.cols * d["x"], cycleNodes[d["y"] + self.cols * d["x"]])

            # d now points to the new node
            newEdge = HEdge(cycleNodes[d["y"] + self.cols * d["x"]], n)
            uniqueEdge = True
            for e in newEdges:
                if e.isEqualTo(newEdge):
                    uniqueEdge = False
                    break

            if uniqueEdge:
                newEdges.append(newEdge)

        for e in newEdges:
            print(e)
            e.connectNodes()

        # do it again to get the end nodes
        degree1Nodes = [n for n in cycleNodes if len(n.spanningTreeAdjacentNodes)==1]
        newEdges = []
        for n in degree1Nodes:
            for m in degree1Nodes:
                if dist(n.x, n.y, m.x, m.y) == 1:
                    if n.x//2 == m.x//2 and n.y//2 == m.y//2:
                        newEdge = HEdge(m, n)
                        uniqueEdge = True
                        for e in newEdges:
                            if e.isEqualTo(newEdge):
                                uniqueEdge = False
                                break
                        if uniqueEdge:
                            newEdges.append(newEdge)
                        break

        for e in newEdges:
            print(e)
            e.connectNodes()

        print(cycleNodes)
        for n in cycleNodes:
            if len(n.spanningTreeAdjacentNodes) != 2:
                print("oof1", n)

        cycle = [cycleNodes[random.randrange(0, len(cycleNodes))]]

        previous = cycle[0]
        node = cycle[0].spanningTreeAdjacentNodes[0]
        while node != cycle[0]:
            _next = node.spanningTreeAdjacentNodes[0]
            if _next == previous:
                _next = node.spanningTreeAdjacentNodes[1]

            if len(_next.spanningTreeAdjacentNodes) != 2:
                print("oof2", _next)

            cycle.append(node)
            previous = node
            node = _next

        print(cycle)
        self.cycle = cycle
        for i in range(len(self.cycle)):
            self.cycle[i].cycleNo = i

        # start from a random node and move in a random direction
        # let startingNode = this.spanningTree.getRandomElement().node1;
        # cycle.push(startingNode);
        # cycle.push(startingNode.spanningTreeAdjacentNodes[0]);
        # let currentNode = cycle[1];
        # let nextNode = currentNode.getNextNodeMovingLeft(startingNode);
        # while (nextNode !== startingNode || cycle.length !== this.w * this.h) {
        #     cycle.push(nextNode);
        #     nextNode = nextNode.getNextNodeMovingLeft(cycle[cycle.length - 2]);
        #     if (nextNode === cycle[cycle.length - 2]) {
        #         cycle.push(cycle[cycle.length - 1]);
        #     }
        # }
        
        # print(cycle);


    def createSpanningTree(self):
        stNodes = [] #SpanningTreeNodes
        for i in range(self.rows//2 + (1 if self.rows%2 else 0)):
            for j in range(self.cols//2 + (1 if self.cols%2 else 0)):
                stNodes.append(HNode(i, j))

        for n in stNodes:
            n.setEdges(stNodes)

        spanningTree = []
        randomNode = random.choice(stNodes)
        spanningTree.append(HEdge(randomNode, randomNode.edges[0]))
        nodesInSpanningTree = [randomNode, randomNode.edges[0]]

        while( len(nodesInSpanningTree) < len(stNodes) ):
            randomNode = random.choice(nodesInSpanningTree)
            edges = [n for n in randomNode.edges if n not in nodesInSpanningTree]
            if len(edges) != 0:
                randomEdge = random.choice(edges)
                nodesInSpanningTree.append(randomEdge)
                spanningTree.append(HEdge(randomNode, randomEdge))

        for n in stNodes:
            n.setSpanningTreeEdges(spanningTree)
        #spanning tree created
        for n in stNodes:
            if n not in nodesInSpanningTree:
                print("nooooooooooooooo")

        self.spanningTree = spanningTree
        print(spanningTree)
        self.spanningTreeNodes = stNodes


    def getNextPosition(self, x, y):
        for i in range(len(self.cycle)):
            if self.cycle[i].x == x and self.cycle[i].y == y:
                return self.cycle[(i + 1) % len(self.cycle)]
        return None


    def getNodeNo(self, x, y):
        for i in range(len(self.cycle)):
            if self.cycle[i].x == x and self.cycle[i].y == y:
                return i
        return -1


    def getPossiblePositionsFrom(self, x, y):
        currentNode = self.cycle[self.getNodeNo(x, y)]
        nodeNos = []
        for n in currentNode.edges:
            nodeNos.append(self.getNodeNo(n.x, n.y))
        return nodeNos


    def getDisplay(self):
        pass











