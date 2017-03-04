def is_possible(n, matrix, vertices, i):
    j = 0
    while j < len(vertices):
        if matrix[n][j] and i == vertices[j]:
            return False
        j += 1
    return True


def assign_colour(graph, num_colours, vertices, n):
    #base case
    if (n == len(vertices)):
        return True

    i=1
    while i <= num_colours:
        #check if colour i will work with vertex n
        if (is_possible(n, graph, vertices, i)):
            vertices[n] = i
            
            #assign colours to rest of vertices
            if assign_colour(graph, num_colours, vertices, n+1):                 
                return True
        
            vertices[n] = 0 #if does not provide solution set to zero
        i=i+1
    return False


# checks if assign_colour returns true or false
def findSolution(matrix, num_colours):
    vertices = [0 for vertex in matrix] 
    if assign_colour(matrix, num_colours, vertices, 0):
        return solution(vertices)
    else:
        return False

# returns a list of values R, G or B for each index of the vertices
def solution(vertices):
    return ['R' if v == 1 else 'G' if v == 2 else 'B' for v in vertices]

def tcp(matrix):
    num_colours = 3
    return findSolution(matrix, num_colours)
