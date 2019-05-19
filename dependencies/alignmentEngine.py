# Alignment engine 


# Our heavily modified matrix class that we will be using extensively. 



# Coordinate system: The coordinate system here is a little wierd. 
# I made it so that X is left and right, and Y is up and down. 

# This is kinda the wrong way round when you access self.rows, so just use the addItem method. 

import random

from distanceMatrixEngine import generate_distance_matrix

class Matrix:
    
    
    def __init__(self,topLabel,sideLabel):
        
        self.topLabel = topLabel
        self.sideLabel = sideLabel
        self.rows = []
        self.previousItem = None
        self.currentItem = None
        self.currentX = None
        self.currentY = None
        self.previousX = None
        self.previousY = None
        
        for element in sideLabel:
            self.rows.append([])
            
        for innerList in self.rows:
            
            for element in topLabel:
                innerList.append(str(0))
                
    
    def changeCurrentItem(self,x,y):
        
        self.previousItem = self.currentItem
        
        self.currentItem = self.rows[y][x]
        
        
        
        
        self.previousX = self.currentX
        self.previousY = self.currentY
        
        self.currentX = x
        self.currentY = y 
        
        print("The current item is now {}".format(self.currentItem))
        print("The current coordinate is {},{}".format(self.currentX,self.currentY)) 
        print("The previous item is now {}".format(self.previousItem))
        print("The previous coordinate is now {},{}".format(self.previousX,self.previousY))
        
    def loadUpSequecne(self,upSequence):
        
        self.upSequence = upSequence
    
    def loadSideSequence(self,sideSequence):
        
        self.sideSequence = sideSequence
        
    def addItem(self,topName,sideName,item):
        
        outerIndexList = [i for i, x in enumerate(self.sideLabel) if x == sideName]
        innerIndexList = [i for i, x in enumerate(self.topLabel) if x == topName]
        
        for outerIndex in outerIndexList:
            
            for innerIndex in innerIndexList:
                
                self.rows[outerIndex][innerIndex] = item
    
    def addItemByCoordinate(self,x,y,item):
        
        self.rows[y][x] = item
    
    def modifyCurrentItem(self,item):
        
        self.rows[self.currentY][self.currentX] = item
        
    def goToBottomRight(self):
        
        self.changeCurrentItem(-1,-1)
        
        self.currentX = len(self.topLabel) -1
        self.currentY = len(self.sideLabel) - 1        
        
    def moveDiagonallyLeft(self):
        
        self.changeCurrentItem(self.currentX - 1, self.currentY -1 ) 
        
    def moveDiagonallyRight(self):
        
        self.changeCurrentItem(self.currentX + 1,self.currentY + 1) 
        
    def moveLeft(self):
        self.changeCurrentItem(self.currentX -1,self.currentY)
    
    def moveUp(self):
        
        self.changeCurrentItem(self.currentX,self.currentY -1)
        
    def goBackToPrevious(self):
        
        self.changeCurrentItem(self.previousX,self.previousY)
        
    
    
    
        
    def __repr__(self):
        
        biggestLength = 0
        
        for outerList in self.rows:
            
            for element in outerList:
                
                if len(element) > biggestLength:
                    biggestLength = len(element)
                    
        for element in self.sideLabel:
            
            if len(element) > biggestLength:
                
                biggestLength = len(element)
                
        for element in self.topLabel:
            
            if len(element) > biggestLength:
                
                biggestLength = len(element)
                
        
        
        
        printRows = []
        printTopLabel = []
        printSideLabel  = []
        spacesAdded = 0
        
        for element in self.sideLabel:
            
            if len(element) == biggestLength:
                printSideLabel.append(element)
            else:
                modifiedElement = element + (" " * (biggestLength - len(element) ) )
                
                if biggestLength - len(element) > spacesAdded:
                    
                    spacesAdded = biggestLength - len(element)
                    
                
                
                
                printSideLabel.append(modifiedElement)        
        
        
        
        for element in self.topLabel:
            
            if len(element) == biggestLength:
                printTopLabel.append(element)
            else:
                modifiedElement = element + (" " * (biggestLength - len(element) ) )
                
                printTopLabel.append(modifiedElement)
                
        for innerList in self.rows:
            
            buildList = []
            
            for element in innerList:
                
                if len(element) == biggestLength:
                    buildList.append(element)
                else:
                    modifiedElement = element + (" " * (biggestLength - len(element) ) )
                    buildList.append(modifiedElement)
                    
            printRows.append(buildList)
        
       
       
       
       
    
        buildString = "\n"
        
        buildString = buildString + (" " * (spacesAdded + 2)) + str(printTopLabel) + "\n"
        
        index = 0 
        
        for element in printSideLabel:
            
            
            buildString = buildString + element + " "  + str(printRows[index]) + "\n"
            
            index += 1 
        
        
        return buildString
        



def make_test_matrix():
    
    sideChain = input("Enter side chain \n")
    topChain = input("Enter top chain")
    
    matrix = Matrix(sideChain.split(","),topChain.split(","))
    
    for element1 in sideChain:
        
        for element2 in topChain:
            
            matrix.addItem(element1,element2,str(random.randint(1,10)))
    
    
    return matrix