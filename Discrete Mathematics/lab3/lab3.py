import numpy
# Taking input
fileName = input("Unesite ime datoteke: ")
file = open(fileName, "r")

# Loading in the data
lines = file.readlines()
n = int(lines[0])
a = []
for i in range(2, n + 2):
    a.append(lines[i].rstrip('\n'))

# Filling out the matrix with characters representing ones and zeroes
y = []
matrix = []
for i in range(0, n):
    y = a[i]
    y = y.replace(" ", "")
    z = []
    for j in range(0, n):
        z.append(y[j])
    matrix.append(z)

# Converting characters of a matrix to an integer type
for i in range(0, n):
    for j in range(0, n):
        matrix[i][j] = int(matrix[i][j])

# Input taking part is done ([n] = num of vertices, [matrix] = adjacency matrix)
# ------------------------------------------------------------------------------

# Algorithm part of the program
# Recursive Function, returns true is the graph is k-colored
def colorGraph(matrix, k, i, colors):
    if i == n:
        for j in range(n):
            for l in range(j + 1, n):
                if matrix[j][l] and colors[l] == colors[j]:
                    print(colors)
                    return False
        return True
    for z in range(1, k + 1):
        colors[i] = z
        if colorGraph(matrix, k, i + 1, colors):
            return True
        colors[i] = 0
    return False

# Function that checks if the graph is nul-graph
def checkNulGraph(matrix):
    list = numpy.array(matrix)
    check = numpy.all(list == 0)
    return check

# Function that checks if the graph is complete
def checkCompleteGraph(matrix):
    counter = 0
    for i in matrix:
        for j in i:
            if(j == 0):
                counter += 1
    if(counter == n):
        return True
    else:
        return False 

# Putting input in Algorithms
def findChromaticNumber(matrix, n):
    colors = [0] * n
    # if nul-graph, return 1
    if checkNulGraph(matrix):
        return 1
    # if completeGraph, return number of vertices(n)
    elif checkCompleteGraph(matrix):
        return n
    # else find chromatic number
    else:
        for i in range(2, n+1):
            if colorGraph(matrix, i, 0, colors):
                return i

# Main part of the program, calling findChromaticNumber function
print(findChromaticNumber(matrix, n))

