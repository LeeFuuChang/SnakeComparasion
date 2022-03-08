class HamiltonianCycle():
    numOfVertexes = 0
    hamiltonianPath = []
    adjacencyMatrix = [[]]
    def __init__(self, adjacencyMatrix):
        self.adjacencyMatrix = adjacencyMatrix
        self.hamiltonianPath = [0]*len(self.adjacencyMatrix)
        self.numOfVertexes = len(self.adjacencyMatrix)

        self.hamiltonianPath[0] = 0

    def find(self):
        if(not self.findFeasibleSolution(1)):
            print("No Feasible Solution. . .")
        else:
            self.showHamiltonianPath()

    def showHamiltonianPath(self):
        print(*self.hamiltonianPath, self.hamiltonianPath[0])

    def findFeasibleSolution(self, position):
        if position == self.numOfVertexes:
            if self.adjacencyMatrix[self.hamiltonianPath[position-1]][self.hamiltonianPath[0]] == 1:
                return True
            else:
                return False
        for vertexIndex in range(1, self.numOfVertexes):
            if self.isFeasible(vertexIndex, position):
                self.hamiltonianPath[position] = vertexIndex
                if self.findFeasibleSolution(position+1):
                    return True
        return False
    
    def isFeasible(self, vertexIndex, actualPosition):
        if self.adjacencyMatrix[self.hamiltonianPath[actualPosition-1]][vertexIndex] == 0:
            return False
        for i in range(actualPosition):
            if self.hamiltonianPath[i] == vertexIndex:
                return False
        return True


