def isPossible(n,graph,colors,i):

    j=0
    while (j<3):
        if (graph[n][j] and i ==colors[j]):
            return False
        j=j+1
    return True

def assignColor(graph, numofColors, colors, n):

    if (n==N):
        return True
    i=1
    while i<=numofColors:
        if (isPossible(n, graph, colors, i)):
            colors[n]=i

            if (assignColor(graph,numofColors,colors,n+1)==True):
                return True
            colors[n]=0;
        i=i+1
    return False



def findSolution(graph, numofColors):

    i=0
    while (i<N):
        colors[i]=0;
        i=i+1
        
    if ((assignColor(graph, numofColors, colors, 0))==False):
        print "No possible solution"
        return False
    else:
        print "True"
        printSolution(colors)
        return True

def printSolution(colours):

    print "solution exists"
    k=0
    while k<N:
        if colors[k]==1:
            print "Red"
        elif colors[k]==2:
            print "Blue"
        else:
            print "Yellow"
        ##print colors[k]
        k=k+1


def main():



    numofColors=3
    findSolution(graph, numofColors);

    
graph=[[0,1,1,1,0],[1,1,1,1,1],[1,1,0,1,0],[1,1,1,1,1],[1,1,0,0,0]]
N=len(graph)
colors=[1,2,3,4,5]
main()
