import graphviz
import math

# GLOBAL VAR STUFF
l=0.4
globalX = 0
globalY = 0
globalId = 0
scalingFactorGap=2.5
XLimit=15
YLimit = 25
pdfNumber=1

#

import itertools
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

def edgesOutsideNode(n):
    edges00=edges
    for n0 in n:
        edges00= list(filter(lambda x: not(x[0]==n0 or x[1]==n0),edges00))
    return edges00

def numberOfDrawnEdgesForAnNOfIsolatedVertices(n):
    global globalX,globalY,globalId,pdfNumber,e


    combinations=list(itertools.combinations(vertices,n))
    nC=len(combinations)
    
    for combination in combinations:
        #print(combination)
        allEdgesOutSideIsolated=edgesOutsideNode(combination)
        #print(allEdgesOutSideIsolated)
        aeoiLen=len(allEdgesOutSideIsolated)
        twoToThePowerOfKCombinations=[]
        for K in range(aeoiLen):
            twoToThePowerOfKCombinations.extend(list(list(allEdgesOutSideIsolated[j] for j in combOfEdges) for combOfEdges in list(itertools.combinations(range(aeoiLen),K))))
        twoToThePowerOfKCombinations.append(allEdgesOutSideIsolated)
        #print(twoToThePowerOfKCombinations)



        for prGraph in twoToThePowerOfKCombinations:
            if globalX > XLimit*l:
                globalX = 0
                globalY-=l*scalingFactorGap
            if globalY < -YLimit*l:
                globalY = 0
                pdfNumber+=1
                e.render(directory='Downloads').replace('\\', '/')
                #e.view()
                e = graphviz.Graph('ER', filename='output/er'+str(pdfNumber)+'.gv', engine='neato')
            globalId+=1
            graphPart(globalX,globalY,str(globalId),combination,prGraph)
            globalX+=l*scalingFactorGap


###
trigX=l*math.cos(60*math.pi/180)
trigY=l*math.sin(60*math.pi/180)
e = graphviz.Graph('ER', filename='output/er1.gv', engine='neato')
def graphPart(stX,stY,id,combination,restEdges):
    e.attr('node', shape='point',color='black')
    nodeToggleOn=list(combination)
    nodeToggleOn.extend(list((k1) for k2 in restEdges for k1 in k2))
    e.node('0_'+id,pos=str(stX)+","+str(stY)+"!",color='black' if 0 in nodeToggleOn else 'grey')
    e.node('1_'+id,pos=str(stX-trigX)+","+str(stY-trigY)+"!",color='black' if 1 in nodeToggleOn else 'grey')
    e.node('2_'+id,pos=str(stX+trigX)+","+str(stY-trigY)+"!",color='black' if 2 in nodeToggleOn else 'grey')
    e.node('3_'+id,pos=str(stX-2*trigX)+","+str(stY-2*trigY)+"!",color='black' if 3 in nodeToggleOn else 'grey')
    e.node('4_'+id,pos=str(stX)+","+str(stY-2*trigY)+"!",color='black' if 4 in nodeToggleOn else 'grey')
    e.node('5_'+id,pos=str(stX+2*trigX)+","+str(stY-2*trigY)+"!",color='black' if 5 in nodeToggleOn else 'grey')

    edgeToggle = lambda x,y: ('black' if y==0 else 'bold') if x in restEdges else ('grey' if y==0 else 'dashed')
    e.edge('0_'+id, '1_'+id,color=edgeToggle((0,1),0),style=edgeToggle((0,1),1))
    e.edge('0_'+id, '2_'+id,color=edgeToggle((0,2),0),style=edgeToggle((0,2),1))
    e.edge('1_'+id, '2_'+id,color=edgeToggle((1,2),0),style=edgeToggle((1,2),1))
    e.edge('1_'+id, '3_'+id,color=edgeToggle((1,3),0),style=edgeToggle((1,3),1))
    e.edge('1_'+id, '4_'+id,color=edgeToggle((1,4),0),style=edgeToggle((1,4),1))
    e.edge('2_'+id, '4_'+id,color=edgeToggle((2,4),0),style=edgeToggle((2,4),1))
    e.edge('2_'+id, '5_'+id,color=edgeToggle((2,5),0),style=edgeToggle((2,5),1))
    e.edge('3_'+id, '4_'+id,color=edgeToggle((3,4),0),style=edgeToggle((3,4),1))
    e.edge('4_'+id, '5_'+id,color=edgeToggle((4,5),0),style=edgeToggle((4,5),1))

globalX=0
for ii in range(len(vertices)+1):
    numberOfDrawnEdgesForAnNOfIsolatedVertices(ii)

print(globalId)
e.render(directory='Downloads').replace('\\', '/')
#e.view()

## Merging PDF files generated https://youtu.be/D1Yf7fF12-g
from PyPDF2 import PdfMerger
import os
merger=PdfMerger()
pdf_files=['Downloads/output/er'+str(k+1)+'.gv.pdf' for k in range(pdfNumber)]
print(pdf_files)
for pdf_file in pdf_files:
    merger.append(pdf_file)

merger.write('Downloads/output/erOUTPUT.gv.pdf')
merger.close()

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        os.remove(pdf_file)
    if os.path.exists(pdf_file[:-4]):
        os.remove(pdf_file[:-4])
