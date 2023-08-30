import itertools
import math
vertices=range(6)
edges=[(0,1),(0,2),(1,2),(1,3),(1,4),(2,4),(2,5),(3,4),(4,5)]
v=len(vertices)
e=len(edges)

def degOfVertex(n):
    deg=0
    for edge in edges:
        if edge[0]==n or edge[1]==n:
            deg+=1

    return deg

def edgeExists(tup1):
    if tup1 in edges or (tup1[1],tup1[0]) in edges:
        return True
    return False

def numberOfDrawnEdgesForAnNOfIsolatedVertices(n):
    combinations=list(itertools.combinations(vertices,n))
    nC=len(combinations)
    print(combinations)
    AllPossibleEdgesInCombinations=(list(list(itertools.combinations(combinations[k],2)) for k in range(nC)))
    print(AllPossibleEdgesInCombinations)
    n2=len(AllPossibleEdgesInCombinations[0])
    NumberOfEdgesExistingAmongstThem=(list(map(lambda x: sum(edgeExists(x[k]) for k in range(n2)),AllPossibleEdgesInCombinations)))
    print(NumberOfEdgesExistingAmongstThem)
    SumOfDegreesOfVertices=list(map(lambda x: sum(degOfVertex(x[k]) for k in range(n)),combinations))
    print(SumOfDegreesOfVertices)
    print('\n')
    return sum(math.pow(2,e-SumOfDegreesOfVertices[k]+NumberOfEdgesExistingAmongstThem[k]) for k in range(nC))



NumberOfSubgraphs=sum(numberOfDrawnEdgesForAnNOfIsolatedVertices(k) for k in range(v))

print("Total number of subgraphs", NumberOfSubgraphs)

