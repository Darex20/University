# Taking input
fileName = input("Unesite ime datoteke: ")
file = open(fileName, "r")

# Loading in the data
lines = file.readlines()
vertices = int(lines[0])
a = []
for i in range(2, vertices + 2):
    a.append(lines[i].rstrip('\n'))

# Filling out the matrix with characters representing ones and zeroes
y = []
matrix = []
for i in range(0, vertices):
    y = a[i]
    y = y.replace(" ", "")
    z = []
    for j in range(0, vertices):
        z.append(y[j])
    matrix.append(z)

# Converting characters of a matrix to an integer type
for i in range(0, vertices):
    for j in range(0, vertices):
        matrix[i][j] = int(matrix[i][j])

# Input taking part is done ([vertices] = num of vertices, [matrix] = adjacency matrix)
# -------------------------------------------------------------------------------------

# Algorithm part
def DFS_Algorithm(counter, length, checked, vertex, otherVertex, matrix):
    # Putting the current vertex as visited
    checked[vertex] = True

    # Starting condition of a recursive function - if the path of length-1  is found
    if (length == 0):
        # Marking the vertex as usable again
        checked[vertex] = False
        if (matrix[vertex][otherVertex] == 1):
            counter = counter + 1
            return counter
        else:
            return counter

    # Searching every possible path of length - 1
    for i in range(vertices):
        if (checked[i] == False and matrix[vertex][i] == 1):
            # Recursively calling a function and giving it a length-1 cycle
            counter = DFS_Algorithm(counter, length - 1, checked, i, otherVertex, matrix)
    checked[vertex] = False
    return counter
# Algorithm part done

# Main Part of a program - calling the algorithm function and giving it certain parameters
largestLength = 0
for j in range(3, vertices+2):
    counter = 0
    # Putting all vertices as unchecked initially
    checked = [False] * vertices
    for i in range(vertices - j + 1):
        counter = DFS_Algorithm(counter, j - 1, checked, i, i, matrix)
        checked[i] = True
    length = int(counter / 2)
    if(length != 0):
        # If j-length cycle was found then put it as the largestLength
        largestLength = j
print(largestLength)

