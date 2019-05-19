# Distance calculator and matrix engine. 

# Generally clean up code and make it presentable, test thoroughly. COMMENT



import os
from dependencies.matrixClass import Matrix


# Just a quick function so I dont have to type the backslash every time. 
def newLine():
    print("\n")
    
def exportMode():
    os.chdir("..")
    
def normalMode():
    os.chdir(".\dependencies")

# Matrix class, allows creation and manipulation of 2D Matrices with labels for both axis. 



class Globals:
    
    binaryDict = {'A': [0, 1, 1, 0, 1, 1, 0, 0], 'B': [0, 1, 0, 1, 1, 1, 1, 1], 'C': [1, 1, 0, 0, 0, 1, 0, 1], 'D': [1, 1, 1, 1, 0, 1, 1, 0], 'E': [1, 1, 1, 1, 1, 0, 0, 0], 'F': [1, 1, 0, 0, 1, 0, 1, 1], 'G': [1, 0, 0, 0, 1, 1, 0, 0], 'H': [1, 0, 1, 1, 1, 1, 1, 1], 'I': [0, 0, 1, 0, 0, 1, 0, 1], 'J': [0, 0, 0, 1, 0, 1, 1, 0], 'K': [0, 1, 0, 1, 0, 0, 0, 1], 'L': [0, 1, 1, 0, 0, 0, 1, 0], 'M': [1, 0, 1, 1, 0, 0, 0, 1], 'N': [1, 0, 0, 0, 0, 0, 1, 0], 'O': [0, 0, 0, 1, 1, 0, 0, 0], 'P': [0, 0, 1, 0, 1, 0, 1, 1], 'AR': [1, 1, 0, 0, 0, 1, 1, 0], 'BR': [1, 1, 1, 1, 0, 1, 0, 1], 'CR': [0, 1, 0, 1, 1, 1, 0, 0], 'DR': [0, 1, 1, 0, 1, 1, 1, 1], 'ER': [1, 0, 0, 0, 1, 1, 1, 1], 'FR': [1, 0, 1, 1, 1, 1, 0, 0], 'GR': [1, 1, 0, 0, 1, 0, 0, 0], 'HR': [1, 1, 1, 1, 1, 0, 1, 1], 'IR': [0, 1, 0, 1, 0, 0, 1, 0], 'JR': [0, 1, 1, 0, 0, 0, 0, 1], 'KR': [0, 0, 0, 1, 0, 1, 0, 1], 'LR': [0, 0, 1, 0, 0, 1, 1, 0], 'MR': [0, 0, 0, 1, 1, 0, 1, 1], 'NR': [0, 0, 1, 0, 1, 0, 0, 0], 'OR': [1, 0, 0, 0, 0, 0, 0, 1], 'PR': [1, 0, 1, 1, 0, 0, 1, 0]}
    currentMatrix = None



def dictionary_generator():
    

    
    file = open("8bit.txt")
    myDict = {}
    
    for line in file:
        
        lineList = line.split()
        
        key = lineList[0]
        value = lineList[1:]
        
        for index in range(len(value)):
            value[index] = int(value[index])
            
        
        myDict[key] = value 
    
    print(myDict)
    
    
def hamming_difference_generator():
    

        
    file = open("outputFile.txt","w")
    
    dict1 = Globals.binaryDict
    dict2 = Globals.binaryDict
    
    for key1 in dict1.keys():
        
        binary1 = dict1[key1] 
        
        for key2 in dict2.keys():
            
            binary2 = dict2[key2]
        
            index = 0
            counter = 0 
            
            while index < len(binary1):
                
                if binary1[index] == binary2[index]:
                    pass
                else:
                    counter += 1 
                    
                index +=1 
            
            buildString = "{} {} {}".format(key1,key2,counter)
            file.write(buildString)
            file.write("\n")

    
def generate_matrix_dictionary():
    
    
    file = open("outputFile.txt","r")
    
    runningTotal = 0 
    
    runningCount = 0 
    
    average = 0
    
    for line in file:
        
        workingList = line.split()
        
        runningCount += 1
        runningTotal = runningTotal + int(workingList[2])
        
        #print(runningCount,runningTotal)
        
    
    average = runningTotal / runningCount
    
    file.close()
    
    file = open("outputFile.txt")
    
    matrixDict = {}
    
    
    for line in file:
        
        workingList = line.split()
        
        key = workingList[0] + "," + workingList[1]
        
        matrixDict[key] = str(int(average - int(workingList[2])))
        
       
    return matrixDict


def generate_distance_matrix():
    
    checkList = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","AR","BR","CR","DR","ER","FR","GR","HR","IR","JR","KR","LR","MR","NR","OR","PR"]
    newLine()
    
    matrixDict = generate_matrix_dictionary()
    
    label1 = input("Enter your first family chain, seperated by commas: \n")
    label1 = label1.upper()
    
    for element in label1.split(","):
        
        if element not in checkList:
            
            print("Invalid family chain entered - Try again: \n")
            label1 = input("Enter your first family chain, seperated by commas: \n")
            label1 = label1.upper()
    
    label2 = input("Enter your second family chain, seperated by commas: \n")
    label2 = label2.upper()
    
    for element in label2.split(","):
        
        if element not in checkList:
            
            print("Invalid family chain entered - Try again: \n")
            label2 = input("Enter your second family chain, seperated by commas: \n")    
            label2 = label2.upper()
    
    if len(label1) > len(label2):
        topLabel = label1.split(",")
        sideLabel = label2.split(",")
    else:
        topLabel = label2.split(",")
        sideLabel = label1.split(",")
    
   
    
    
    
    finalMatrix = Matrix(topLabel,sideLabel)
    
    matrixDict = generate_matrix_dictionary()
    

    
    for element1 in topLabel:
        
        for element2 in sideLabel:
            
            item = matrixDict[str(element1) + "," + str(element2)]
            
            finalMatrix.addItem(element1,element2,item)
            
    
    
    newLine()
    print("Pairwise Mismatch Table Generation Complete")
    print("-------------------------------------------")
    print(finalMatrix)   
    print("-------------------------------------------")
    newLine()
    
    Globals.currentMatrix = finalMatrix

    #outputExcel()
    
    return finalMatrix

def outputExcel():
    
    
    
    import dependencies.xlsxwriter as excel
    
    exportMode()
    
    workbook = excel.Workbook("Pairwise Mismatch Table.xlsx")
    worksheet = workbook.add_worksheet()
    
    row = 0 
    column = 0 
    
    for innerList in Globals.currentMatrix.rows:
        
        for element in innerList:
            
            worksheet.write(row,column,element)
            
            column += 1 

        row +=1 
        column = 0 
    
    
    try:
        workbook.close()
        newLine()
        print("[Pairwise mismatch table also exported to excel worksheet 'Pairwise Mismatch Table.xlsx]'")
        newLine()
    except:
        print("[Error: Excel export failed.]")
        print("[The Excel file is currently open - please close the file and try again.]")
        newLine()
    
    normalMode()