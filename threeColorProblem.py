

def isPossible(n,graph,colors,i):

    j=0
    while (j<3):
        if (graph[n][j] and i ==colors[j]):
            return False
        j=j+1
    return True


def assignColor(graph, numofColors, colors, n):

    #base case, if N is 0
    if (n==N):
        return True
    i=1
    while i<=numofColors:
        if (isPossible(n, graph, colors, i)): #check if color i will work with vertex n
            colors[n]=i
            
            if (assignColor(graph,numofColors,colors,n+1)==True): #assign colors to rest of vertices
                return True
        
            colors[n]=0; #if does not provide solution set to zero
        i=i+1
    return False


##checks if assignColor returns true or false
def findSolution(graph, numofColors):
        
    if ((assignColor(graph, numofColors, colors, 0))==False):
        print ("No possible solution")
        return False
    else:
        printSolution(colors)
        return True

#if there is a solution, this function will convert the numbers assigned to each vertex
# 1 = red, 2 = blue and 3 = yellow
def printSolution(colors):

    print ("solution exists")
    k=0
    while k<N:
        if colors[k]==1:
            print ("Red")
        elif colors[k]==2:
            print ("Blue")
        else:
            print ("Yellow")
        k=k+1
    
       
def main():

    numofColors=3
 ##   userInput=input("please enter formula: ")
 ##   formula = (nestgen(parse(userInput)))

    findSolution(graph, numofColors);

    
graph=[[0,0,1,1],[1,0,1,0],[1,1,0,1],[1,0,1,0]]
N=len(graph)
colors=[1,2,3,4]
main()
