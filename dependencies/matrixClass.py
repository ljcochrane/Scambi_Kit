class Matrix:
    
    
    def __init__(self,topLabel,sideLabel):
        
        self.topLabel = topLabel
        self.sideLabel = sideLabel
        self.rows = []
        
        for element in sideLabel:
            self.rows.append([])
            
        for innerList in self.rows:
            
            for element in topLabel:
                innerList.append(str(0))
                
    
        
        
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
        
    
    
    
    # Magic voodoo code that makes the matrix print nicely. 
    # It basically adds spaces to each element such that each element is the same length. 
    
        
        
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
        
       
       
       
       # Basically made this bit by trial and error. Eeesh. 
    
        buildString = "\n"
        
        buildString = buildString + (" " * (spacesAdded + 2)) + str(printTopLabel) + "\n"
        
        index = 0 
        
        for element in printSideLabel:
            
            
            buildString = buildString + element + " "  + str(printRows[index]) + "\n"
            
            index += 1 
        
        
        return buildString
        
