import graphviz
import math

# GLOBAL VAR STUFF
globalX = 0
globalY = 0
globalId = 0
pdfNumber=1

#
vertices=range(6)
edges=[(0,1),(0,2),(1,2),(1,3),(1,4),(2,4),(2,5),(3,4),(4,5)]

#SETTINGS
l=0.4
scalingFactorGap=2.5
XLimit = 6 #When it reaches the XLimit it goes to the next line
YLimit = 10 #When it reaches the YLimit it goes to the next page

trigX=l*math.cos(60*math.pi/180)
trigY=l*math.sin(60*math.pi/180)
posCoords=[(0,0),(-trigX,-trigY),(trigX,-trigY),(-2*trigX,-2*trigY),(0,-2*trigY),(2*trigX,-2*trigY)] #make this array [] for letting graphviz choose the position of nodes
#

import itertools

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
            if globalX > XLimit:
                globalX = 0
                globalY-=l*scalingFactorGap
            if globalY < -YLimit:
                globalY = 0
                pdfNumber+=1
                e.render(directory='Downloads').replace('\\', '/')
                #e.view()
                e = graphviz.Graph('ER', filename='output/er'+str(pdfNumber)+'.gv', engine='neato')
            globalId+=1
            graphPart(globalX,globalY,str(globalId),combination,prGraph)
            globalX+=l*scalingFactorGap


###
e = graphviz.Graph('ER',filename='output/er1.gv', engine='neato')

def graphPart(stX,stY,id,combination,restEdges):
    e.attr('node', shape='point',color='black')
    nodeToggleOn=list(combination)
    nodeToggleOn.extend(list((k1) for k2 in restEdges for k1 in k2))

    for node00,index in enumerate(vertices):
        e.node(str(node00)+'_'+id,color='black' if node00 in nodeToggleOn else 'grey',pos=((str(stX+posCoords[index][0])+','+str(stY+posCoords[index][1])+'!') if posCoords else ''))


    edgeToggle = lambda x,y: ('black' if y==0 else 'bold') if x in restEdges else ('grey' if y==0 else 'dashed')

    for edge00 in edges:
        e.edge(str(edge00[0])+'_'+id, str(edge00[1])+'_'+id,color=edgeToggle(edge00,0),style=edgeToggle(edge00,1))

for ii in range(len(vertices)+1):
    numberOfDrawnEdgesForAnNOfIsolatedVertices(ii)

print(globalId-1)
e.render(directory='Downloads').replace('\\', '/')
#e.view()

######################################################################
## Merging PDF files generated https://youtu.be/D1Yf7fF12-g
from PyPDF2 import PdfMerger
import os
merger=PdfMerger()
pdf_files=['Downloads/output/er'+str(k+1)+'.gv.pdf' for k in range(pdfNumber)]
for pdf_file in pdf_files:
    merger.append(pdf_file)

merger.write('Downloads/output/erOUTPUT.gv.pdf')
merger.close()

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        os.remove(pdf_file)
    if os.path.exists(pdf_file[:-4]):
        os.remove(pdf_file[:-4])
