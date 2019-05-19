# Temporary Traceback


import random
import time
import os 
import os.path
import shutil
from dependencies.distanceMatrixEngine import generate_distance_matrix
from dependencies.matrixClass import Matrix
from dependencies.pydub import AudioSegment
from dependencies.dynamicProgrammingEngine import generate_dyanmic_programming_matrix
from dependencies.distanceMatrixEngine import generate_distance_matrix
from dependencies.matrixClass import Matrix
from dependencies.dynamicProgrammingEngine import generate_dyanmic_programming_matrix
os.chdir(".\dependencies")



pairwiseDistanceTable = generate_distance_matrix()

printableMatrix,outputMatrix,gapScore = generate_dyanmic_programming_matrix(pairwiseDistanceTable)




























def traceback(printableMatrix,outputMatrix,gapScore,pairwiseDistanceTable):
    
    sideLabel = printableMatrix.sideLabel
    topLabel = printableMatrix.topLabel
    
    gapScoreList = [gapScore*i for i in range(1,100)]

    #This just gets everything into the right form, strips it down to a simple 2d array of ints. 
    
    dpMatrix = outputMatrix
    pairwiseDistanceTable = pairwiseDistanceTable.rows
    pairwiseDistanceTable = [[int(str(j)) for j in i] for i in pairwiseDistanceTable]
    
    
    
    for i in range(len(dpMatrix)):
        dpMatrix[i].insert(0,gapScoreList[i])
    
    dpMatrix.insert(0,gapScoreList[:len(dpMatrix[0])-1])
    dpMatrix[0].insert(0,0)
    
    for i in range(len(pairwiseDistanceTable)):
        pairwiseDistanceTable[i].insert(0,gapScoreList[i])
    
    pairwiseDistanceTable.insert(0,gapScoreList[:len(pairwiseDistanceTable[0])-1])
    pairwiseDistanceTable[0].insert(0,0)    
    

    print("-------DPMATRIX-------")
    print(dpMatrix)
    print("------PAIRWISE------")
    print(pairwiseDistanceTable)
    
    
    i  = len(dpMatrix) -1 
    j = len(dpMatrix[0]) -1
    
    sList = []
    tList = []
    
    
    # Main traceback algorithm, ngl, mainly copied from Gatherer's Perl script. Let's hope its right lol. 
    
    while i!=-1 and j!=0:
        
        print("Now at {}, {}".format(i,j))
        
        if j>=0 and (dpMatrix[i][j] == dpMatrix[i][j-1] + gapScore):
            print("Going left")
            j = j - 1 
            sList.append("-")
            tList.append(topLabel[j])
        
        
        elif (dpMatrix[i][j]) == (dpMatrix[i-1][j] + gapScore):
            print("Going up")
            i = i -1 
            sList.append(sideLabel[i])
            tList.append("-")
        
        elif i>0 and j>1 and (dpMatrix[i][j] == (dpMatrix[i-1][j-1] + pairwiseDistanceTable[i][j])) :
            print("Going diagonally")
            i = i-1
            j = j-1
            
            sList.append(sideLabel[i])
            tList.append(topLabel[j])
        
        else:
            print("Going diagonally")
            i = i-1
            j = j-1
            
            sList.append(sideLabel[i])
            tList.append(topLabel[j])            
        
        
        
    sList.reverse()
    tList.reverse()
        
    print("FINAL ALIGNMENT")
    print("---------------")
    print(sList)
    print(tList)
        

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 





























traceback(printableMatrix,outputMatrix,gapScore,pairwiseDistanceTable)