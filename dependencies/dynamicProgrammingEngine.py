# Dynamic Programming Engine



#from matrixClass import Matrix

from dependencies.matrixClass import Matrix

def newLine():
    
    print("\n")


# This function just builds a gap score list ie [-2,-4,-6,-8 etc] to be used in the dynamic programming. 

def generate_gap_score_list(inputMatrix):
    
    newLine()
    
    gapScoreCheckList = list(range(-20,21))
    gapScoreCheckList = [str(element) for element in gapScoreCheckList]
    
    gapScore = input("Please enter a gap Score: \n")
    
    
    while gapScore not in gapScoreCheckList:
        newLine()
        print("Error: Invalid gap score - please try again")
        newLine()
        gapScore = input("Please enter a gap Score: \n")
    
    gapScore = int(gapScore)
    
    gapScoreList = []
    
    for i in range(max(len(inputMatrix[0]),len(inputMatrix))):
        
        gapScoreList.append(gapScore * (i+1))

    return gapScore,gapScoreList



# Ok this is the main thing. 

# Takes as input a Matrix class - presumably generated from the distanceMatrixEngine. 


def generate_dyanmic_programming_matrix(pairwiseMismatchTable):
    
    
    # First we just strip away the matrix class stuff to just get the list of lists stored within. 
    
    inputMatrix = pairwiseMismatchTable.rows
    
    # Call the gapScoreList function to generate our lists and get a user inputed gap score. 
    
    gapScore,gapScoreList = generate_gap_score_list(inputMatrix)
    
    # Create an output list that will become a list of lists as we at to it for output. 
    outputMatrix = []
    
    # This wierd bit of code that I found online just converts all the strings in the mismatch table to integers. 
    inputMatrix  = [[int(float(j)) for j in i] for i in inputMatrix]
    
    
    
    row = 0 
    
    for rowNumber in inputMatrix:
        
        index = 0 
        buildRow = []
        
        #print("GAP SCORE:", gapScore)
        #print("GAP LIST: ", gapScoreList)
        
        for element in rowNumber:
            
            if (row == 0) and (index == 0):
                
                buildItem = max( (inputMatrix[row][index])   ,   (gapScoreList[0] + gapScore) )
                #print("Case 1 Triggered:",buildItem)
                
            elif (row == 0) and (index !=0):
                
                buildItem = max(  (buildRow[-1] + gapScore), (gapScoreList[index-1] + gapScore) , (gapScoreList[index-1] + inputMatrix[row][index]) )
                #print("Case 2 Triggered:",buildItem)
                
            elif (index == 0) and (row != 0): 
                
                
                
                buildItem = max(  (gapScoreList[row] + gapScore) , (outputMatrix[row-1][index] + gapScore) , (gapScoreList[row-1] + inputMatrix[row][index]) ) 
                #print("Case 3 Triggered:",buildItem)
            else:
                
            
                buildItem = max(   (buildRow[-1] + gapScore) , (outputMatrix[row-1][index] + gapScore), (outputMatrix[row-1][index-1] + inputMatrix[row][index])  )
                #print("Case 4 Triggered:",buildItem)
            
            
              
            buildRow.append(buildItem)
            
            index += 1 
            
            #print("\n")
            
        
        
        #print("Built row:",buildRow)
        outputMatrix.append(buildRow) 
        
        #print("\n")
        #print("\n")
        #print("\n")
        
        row += 1 
        
        
    #outputMatrix.append(buildRow)      
           

    
    
    printableMatrix = Matrix(pairwiseMismatchTable.topLabel,pairwiseMismatchTable.sideLabel)
    
    printableRows = [[str(int(j)) for j in i] for i in outputMatrix]
    
    printableMatrix.rows = printableRows
    
    
    
    newLine()
    print("Dynamic Programming Matrix Generation Complete")
    print("----------------------------------------------")
    print(printableMatrix)   
    print("----------------------------------------------")
    newLine()    
    
    
    
    return printableMatrix,outputMatrix, gapScore
    
    

def traceback(printableMatrix,outputMatrix,gapScore,pairwiseDistanceTable):
    
    sideLabel = printableMatrix.sideLabel
    topLabel = printableMatrix.topLabel
    
    gapScoreList = [gapScore*i for i in range(1,100)]

    #This just gets everything into the right form, strips it down to a simple 2d array of ints. 
    
    dpMatrix = outputMatrix
    pairwiseDistanceTable = pairwiseDistanceTable.rows
    pairwiseDistanceTable = [[int(str(j)) for j in i] for i in pairwiseDistanceTable]
    
    # These little two for loops add rows for the gap score to the existing matrices. 
    
    for i in range(len(dpMatrix)):
        dpMatrix[i].insert(0,gapScoreList[i])
    
    dpMatrix.insert(0,gapScoreList[:len(dpMatrix[0])-1])
    dpMatrix[0].insert(0,0)
    
    for i in range(len(pairwiseDistanceTable)):
        pairwiseDistanceTable[i].insert(0,gapScoreList[i])
    
    pairwiseDistanceTable.insert(0,gapScoreList[:len(pairwiseDistanceTable[0])-1])
    pairwiseDistanceTable[0].insert(0,0)    
    
    
    
    #print("-------DPMATRIX-------")
    #print(dpMatrix)
    #print("------PAIRWISE------")
    #print(pairwiseDistanceTable)
    
    
    # Set the initial coordinates to the bottom right. 
    
    i  = len(dpMatrix) -1 
    j = len(dpMatrix[0]) -1
    
    sList = []
    tList = []
    
    
    # Main traceback algorithm, some elements transcribed form Derek Gatherers Perl Script. 
    
    while i!=-1 and j!=0:
        
        #print("Now at {}, {}".format(i,j))
        
        
        
        if i>0 and j>1 and (dpMatrix[i][j] == (dpMatrix[i-1][j-1] + pairwiseDistanceTable[i][j])) :
            #print("Going diagonally")
            i = i-1
            j = j-1
            
            sList.append(sideLabel[i])
            tList.append(topLabel[j])        
        
        elif j>=0 and (dpMatrix[i][j] == dpMatrix[i][j-1] + gapScore):
            #print("Going left")
            j = j - 1 
            sList.append("-")
            tList.append(topLabel[j])
        
        
        elif (dpMatrix[i][j]) == (dpMatrix[i-1][j] + gapScore):
            #print("Going up")
            i = i -1 
            sList.append(sideLabel[i])
            tList.append("-")
        
        else:
            #print("Going diagonally")
            i = i-1
            j = j-1
            
            sList.append(sideLabel[i])
            tList.append(topLabel[j])            
        
        
    
    # Just reverse the lists at the end so we get back to the original order. 
    
    sList.reverse()
    tList.reverse()
    
    
    # Printing in a pretty format
    
    alignmentTopLabel = []
    
    index = 0
    
    while index < len(sList):
        
        if sList[index] == tList[index]:
            alignmentTopLabel.append("*")
        elif sList[index] == "-" or tList[index] == "-":
            alignmentTopLabel.append(" ")
        else:
            alignmentTopLabel.append("x")
    
        index +=1
        
        
    alignmentSideLabel = ["1","2"]
    
    printableAlignment = Matrix(alignmentTopLabel,alignmentSideLabel)
    printableAlignment.rows = []
    printableAlignment.rows.append(sList)
    printableAlignment.rows.append(tList)
    
    newLine() 
    print("Sequence Alignment Complete")
    print("-" * (len(sList) * 5))
    #print(sList)
    #print(tList)
    print(printableAlignment)
    print("* = Match   x = Mismatch   Blank = Gap")
    print("-" * (len(sList) * 5)) 
    newLine()
    
    
    
    

    # Returns the two list channels to be used to build the two audio channels. 
    
    return sList,tList


    
    
    


