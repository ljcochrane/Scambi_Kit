'''

   _____                     _     _   _  ___ _   
  / ____|                   | |   (_) | |/ (_) |  
 | (___   ___ __ _ _ __ ___ | |__  _  | ' / _| |_ 
  \___ \ / __/ _` | '_ ` _ \| '_ \| | |  < | | __|
  ____) | (_| (_| | | | | | | |_) | | | . \| | |_ 
 |_____/ \___\__,_|_| |_| |_|_.__/|_| |_|\_\_|\__|
 

# A Tool to automate the generation of valid scambi progressions, build sound files,
# do pairwise alignment of scambi chains, and more!


# Written by Louis Cochrane: University of Lancaster 
# 2019
# All rights reserved.


'''


import random
import time
import os 
import os.path
import shutil


from dependencies.distanceMatrixEngine import generate_distance_matrix
from dependencies.matrixClass import Matrix
from dependencies.pydub import AudioSegment
from dependencies.dynamicProgrammingEngine import generate_dyanmic_programming_matrix,traceback
from dependencies.audioEngine import build_from_alignment

os.chdir(".\dependencies")


# Just to save me having to type the backslash every time!
#---------------------------------------------------------    
def newLine():
    print("\n")
    
# Change directory for export.

def exportMode():
    os.chdir("..")
    
def normalMode():
    os.chdir(".\dependencies")
    
def printASCI():
    print("  _   _   _   _   _   _     _   _   _  ")
    print(" / \ / \ / \ / \ / \ / \   / \ / \ / \ ")
    print("( S | c | a | m | b | i ) ( K | i | t ) ")
    print(" \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ ")


# Basic Globals class, just to store variables for access by all necessary functions. 
class Globals:
    
    startDict = {6:["1","2","7r","8r","19r","20r","23","24"],
             12:["1r","2r","5","6","11","12","13r","14r"],
             5:["3","4","5r","6r","17r","18r","21","22"],
             15:["3r","4r","7","8","9","10","15r","16r"],
             8:["9r","10r","13","14","27","28","29r","30r"],
             11:["11r","12r","15","16","25","26","31r","32r"],
             2:["17","18","23r","24r","27r","28r","31","32"],
             1:["19","20","21r","22r","25r","26r","29","30"]
             }
             
    
    endDict = {1:["19r","20r","21","22","25","26","29r","30r"],
               2:["17r","18r","23","24","27","28","31r","32r"],
               5:["3r","4r","5","6","17","18","21r","22r"],
               6:["1r","2r","7","8","19","20","23r","24r"],
               8:["9","10","13r","14r","27r","28r","29","30"],
               11:["11","12","15r","16r","25r","26r","31","32"],
               12:["1","2","5r","6r","11r","12r","13","14"],
               15:["3","4","7r","8r","9r","10r","15","16"]
               }
    
    sequenceDict = {"1":[6,12],
                    "2":[6,12],
                    "1r":[12,6],
                    "2r":[12,6],
                    "3":[5,15],
                    "4":[5,15],
                    "3r":[15,5],
                    "4r":[15,5],
                    "5":[12,5],
                    "6":[12,5],
                    "5r":[5,12],
                    "6r":[5,12],
                    "7":[15,6],
                    "8":[15,6],
                    "7r":[6,15],
                    "8r":[6,15],
                    "9":[15,8],
                    "10":[15,8],
                    "9r":[8,15],
                    "10r":[8,15],
                    "11":[12,11],
                    "12":[12,11],
                    "11r":[11,12],
                    "12r":[11,12],
                    "13":[8,12],
                    "14":[8,12],
                    "13r":[12,8],
                    "14r":[12,8],
                    "15":[11,15],
                    "16":[11,15],
                    "15r":[15,11],
                    "16r":[15,11],
                    "17":[2,5],
                    "18":[2,5],
                    "17r":[5,2],
                    "18r":[5,2],
                    "19":[1,6],
                    "20":[1,6],
                    "19r":[6,1],
                    "20r":[6,1],
                    "21":[5,1],
                    "22":[5,1],
                    "21r":[1,5],
                    "22r":[1,5],
                    "23":[6,2],
                    "24":[6,2],
                    "23r":[2,6],
                    "24r":[2,6],
                    "25":[11,1],
                    "26":[11,1],
                    "25r":[1,11],
                    "26r":[1,11],
                    "27":[8,2],
                    "28":[8,2],
                    "27r":[2,8],
                    "28r":[2,8],
                    "29":[1,8],
                    "30":[1,8],
                    "29r":[8,1],
                    "30r":[8,1],
                    "31":[2,11],
                    "32":[2,11],
                    "31r":[11,2],
                    "32r":[11,2]}
    
    lastGeneratedSequence = []
    
    fileCount = 0
    
    familyDict = {'1': 'A', '2': 'A', '3': 'B', '4': 'B', '5': 'C', '6': 'C', '7': 'D', '8': 'D', '9': 'E', '10': 'E', '11': 'F', '12': 'F', '13': 'G', '14': 'G', '15': 'H', '16': 'H', '17': 'I', '18': 'I', '19': 'J', '20': 'J', '21': 'K', '22': 'K', '23': 'L', '24': 'L', '25': 'M', '26': 'M', '27': 'N', '28': 'N', '29': 'O', '30': 'O', '31': 'P', '32': 'P', '1R': 'AR', '2R': 'AR', '3R': 'BR', '4R': 'BR', '5R': 'CR', '6R': 'CR', '7R': 'DR', '8R': 'DR', '9R': 'ER', '10R': 'ER', '11R': 'FR', '12R': 'FR', '13R': 'GR', '14R': 'GR', '15R': 'HR', '16R': 'HR', '17R': 'IR', '18R': 'IR', '19R': 'JR', '20R': 'JR', '21R': 'KR', '22R': 'KR', '23R': 'LR', '24R': 'LR', '25R': 'MR', '26R': 'MR', '27R': 'NR', '28R': 'NR', '29R': 'OR', '30R': 'OR', '31R': 'PR', '32R': 'PR'}
    
    reverseFamilyDict = {'-':['-'],'A': ['1', '2'], 'B': ['2', '3'], 'C': ['3', '4'], 'D': ['4', '5'], 'E': ['5', '6'], 'F': ['6', '7'], 'G': ['7', '8'], 'H': ['8', '9'], 'I': ['9', '10'], 'J': ['10', '11'], 'K': ['11', '12'], 'L': ['12', '13'], 'M': ['13', '14'], 'N': ['14', '15'], 'O': ['15', '16'], 'P': ['16', '17'], 'AR': ['1r', '2r'], 'BR': ['2r', '3r'], 'CR': ['3r', '4r'], 'DR': ['4r', '5r'], 'ER': ['5r', '6r'], 'FR': ['6r', '7r'], 'GR': ['7r', '8r'], 'HR': ['8r', '9r'], 'IR': ['9r', '10r'], 'JR': ['10r', '11r'], 'KR': ['11r', '12r'], 'LR': ['12r', '13r'], 'MR': ['13r', '14r'], 'NR': ['14r', '15r'], 'OR': ['15r', '16r'], 'PR': ['16r', '17r']}
    
    lastGeneratedFamilyChain = []
    
    lastGeneratedPairwiseMismatchTable = []
    
    lastGeneratedDynamicProgrammingMatrix = [] 
    
    rawMatrix = []
    
    gapScore = None
    
    leftChannel = []
    rightChannel = []
    
    
    
# Helper function to grab userinput for the sequence length and first note. 
#---------------------------------------------------------------------------

def get_length_and_note():
    
    newLine()
    
    sequenceLength = input("How long should the scambi chain be? \n")
    
    
    while sequenceLength.isdigit() == False:
        
        newLine()
        print("Error, invalid chain length entered. Try again. \n")
        sequenceLength = input("How long should the scambi chain be? \n")
        
    sequenceLength = int(sequenceLength)
        
        
    firstNote = input("Enter the first sequence to use, or enter 'r' for a random first sequence. \n")
    
    while (firstNote!= "r") and (firstNote not in list(Globals.sequenceDict.keys())):
        newLine()
        print("Error, invalid sequence entered. Try again. \n")
        firstNote = input("Enter the first sequence to use, or enter 'r' for a random first sequence. \n")   
        
        
    return sequenceLength,firstNote




# This is the core sequenece generator, it takes a sequence length and first note
# to use and returns a list containing a valid scambi sequence of set length. 
#--------------------------------------------------------------------------------


def core_random_sequence_generator(sequenceLength,firstNote):
    
    finalList= []
    
    if firstNote == "r":
        firstStart = random.choice( list( Globals.startDict.keys() ) )
        currentSequence = Globals.startDict[firstStart][random.randint(0, len(Globals.startDict[firstStart]) - 1) ]
    else:
        currentSequence = firstNote
    
    finalList.append(currentSequence)
    
    while len(finalList) < sequenceLength:
        
        nextStart = Globals.sequenceDict[currentSequence][1]
        nextSequence = random.choice(Globals.startDict[nextStart])
        
        finalList.append(nextSequence)
        
        currentSequence = nextSequence    
        
    return finalList


# Function to generate and print a basic sequence using the core generator. 
#--------------------------------------------------------------------------

def random_mono_scambi():
    
    sequenceLength,firstNote = get_length_and_note()
    
    
    finalList = core_random_sequence_generator(sequenceLength,firstNote)
        
    
    newLine()
    print("Chain Generation Complete")
    print("-------------------------")
    
    for element in finalList:
        
        print(element)
        
    print("-------------------------")
    newLine()
    
    
    return finalList


# Generates a valid dual channel scambi sequence.
#-----------------------------------------------------------------------------

def random_dual_scambi():
    
    
    # First we generate two mono sequences, using the core generator. 
    
    sequenceLength,firstNote = get_length_and_note()
    
    leftChannel = core_random_sequence_generator(sequenceLength-1,firstNote)
    
    rightChannel = core_random_sequence_generator(sequenceLength-1,firstNote)
    
    
    # The key here is that the two sequences must both end in the same binary.
    # If they do not match, we will redo the process. 
    
    leftEndSignature = leftChannel[-1]
    rightEndSignature = rightChannel[-1]
    
    while Globals.sequenceDict[leftEndSignature][1] != Globals.sequenceDict[rightEndSignature][1]:
        
        rightChannel = core_random_sequence_generator(sequenceLength-1,firstNote)
        rightEndSignature = rightChannel[-1]
    
    
    # Ok, now we have two valid sequences, we just need to select an end note!
    # We just use a random choice for the start dictionary again!
    
    endNote = random.choice( Globals.startDict[(Globals.sequenceDict[leftEndSignature][1])] ) 
    
    
    
    
    # Now we have all the information, time to print nicely!
    
    newLine()
    print("Chain Generation Complete")
    print("-------------------------")    
    print("First Sequence: {}".format(leftChannel[0]) )
    newLine()
    print("Left Channel: {}".format(leftChannel[1:]) ) 
    newLine()
    print("Right Channel: {}".format(rightChannel[1:] ) ) 
    newLine()
    print("Last Sequence: {}".format(endNote) )
    print("-------------------------")
    newLine()    
    

# Function to manually input a scambi sequence. 
#-----------------------------------------------------------------
def manual_entry_mono():
    newLine()
    
    print("Manual mode activated!")
    print("Input a Scambi chain:") 
    print("Each sequence must be lower case and seperated by comma.")
    print("For example: 2,3,5r,7")
    
    newLine()
    sequenceInput = input()
    sequenceInput = sequenceInput.lower()
    sequenceInputList = sequenceInput.split(",")
    
    validEntry = True
    
    for element in sequenceInputList:
        if element not in list(Globals.sequenceDict.keys()):
            validEntry = False    
    
    if validEntry == False:
        newLine()
        print("Invalid chain entered.")
        print("Returning to main menu...")
        return
    else:
        Globals.lastGeneratedSequence = sequenceInputList
        newLine()
        print("Chain accepted and saved.")
        print("Chain can be built into a Scambi sound file using the build function.")
        newLine()
    
    


# This is the build system to actually create a full scambi sound file. 
# It uses pydub and a previously generated build sequence.
#----------------------------------------------------------------------

def build_mono():
    
    
    sequenceToBuild = Globals.lastGeneratedSequence[:]
    
    
    
    if sequenceToBuild == []:
        print("[No chain found: use the mono scambi generator to create a chain to build.]")
        return
    
    # We need to add the .wav to get pyDub to detect the file. 
    
    for index in range(len(sequenceToBuild)):
        
        sequenceToBuild[index] = sequenceToBuild[index] + ".wav"
        
        
    buildList  = []
    
        
    for element in sequenceToBuild:
        
        currentSequence = AudioSegment.from_wav(element)
        buildList.append(currentSequence)
    
    
        
    finalComposition = AudioSegment.empty()
    
    for element in buildList:
        
        finalComposition = finalComposition + element
    

    exportMode()
    finalComposition.export("Exported Scambi Composition.wav",format="wav")
    normalMode()
    

def build_from_alignment(leftChannelList,rightChannelList):
    
    #normalMode()
    
    if leftChannelList == [] or rightChannelList == []:
        print("No alignment found, run alignment sequence to generate an alignment to build")
        return
    
    leftChannelSequences = convert_family_to_sequence(leftChannelList)
    rightChannelSequences = convert_family_to_sequence(rightChannelList)
    
    for index in range(len(leftChannelSequences)):
        
        if leftChannelSequences[index] == "-":
            leftChannelSequences[index] = "x.wav" 
        else:
        
            leftChannelSequences[index] = leftChannelSequences[index] + ".wav"    
    
    
    for index in range(len(rightChannelSequences)):
        
        if rightChannelSequences[index] == "-":
            rightChannelSequences[index] = "x.wav"      
        else:
            
            rightChannelSequences[index] = rightChannelSequences[index] + ".wav"        
        
    leftBuildList = [] 
    
    for element in leftChannelSequences:
        
        currentSequence = AudioSegment.from_wav(element)
        leftBuildList.append(currentSequence)    
        
    rightBuildList = [] 
        
    for element in rightChannelSequences:
            
        currentSequence = AudioSegment.from_wav(element)
        rightBuildList.append(currentSequence)     
        
    
    finalCompositionLeft = AudioSegment.empty()
    
    for element in leftBuildList:
        
        finalCompositionLeft = finalCompositionLeft + element    
        
    exportMode()
    finalCompositionLeft.export("Alignment Left Channel.wav",format="wav")
    normalMode() 
    
    finalCompositionRight = AudioSegment.empty()
    
    for element in rightBuildList:
        
        finalCompositionRight = finalCompositionRight + element    
        
    exportMode()
    finalCompositionRight.export("Alignment Right Channel.wav",format="wav")
    normalMode()   




def convert_sequence_to_family():
    
    
    
    if Globals.lastGeneratedSequence == []:
        
        newLine()
        print("[No chain found: use the mono scambi generator to create a chain to convert.]")
        return
    
    
    outputList = []
    
    
    
    for element in Globals.lastGeneratedSequence:
        
        element = element.upper()
        
        outputList.append(Globals.familyDict[element])
        
    
    
    Globals.lastGeneratedFamilyChain = outputList
    
    newLine()
    print("Conversion complete")
    print("-------------------")
    
    
    for element in outputList[:-1]:
        print(element,end=",")
    print(outputList[-1])
    print("-------------------")

def convert_family_to_sequence(familyList):
    
    outputList = []
    
    for family in familyList:
        
        sequence = random.choice(Globals.reverseFamilyDict[family])
        
        outputList.append(sequence)
        
    return outputList
    

def main():
    
    programChoice = None
    
    while programChoice != "11":
        
    
        newLine()
        printASCI()
        print(" By Louis Cochrane: Lancaster University")
        print("--------------------------------------------------")
        print(" [1] Mono Scambi Chain Generator")
        print(" [2] Dual Channel Scambi Chain Generator")
        print(" [3] Manually Enter a Scambi Chain")
        print(" [4] Build Mono Scambi Sound File from Chain")
        print(" [5] Convert Stored Sequence Chain to Family Chain")
        print(" [6] Generate Pairwise Mismatch Table")
        print(" [7] Generate Dynamic Programming Matrix")
        print(" [8] Run Traceback")
        print(" [9] Run Full Alignment Sequence")
        print("[10] Build Sound Files from Alignment")
        print("[11] Quit")
        print("--------------------------------------------------")
        
        newLine()
        programChoice = input()
        
        
        if programChoice == "1":
            
            Globals.lastGeneratedSequence = random_mono_scambi()
            
        elif programChoice == "2":
            random_dual_scambi()
        
        elif programChoice =="3":
            manual_entry_mono()
            
            
    
        elif programChoice == "4":
            
            if Globals.lastGeneratedSequence == []:
                newLine()
                print("No mono chain found: use the mono scambi generator to create a chain to build, or enter a chain manually.")
                
            
            else:
                newLine()
                print("The most recently generated mono chain is...")
                print(Globals.lastGeneratedSequence)
                newLine()
                print("Your sound file will be built to 'Exported Scambi Composition.wav' in the current directory.")
                print("If a previous build exists it will be overwritten.")      
                newLine()
                choice = input("Would you like to build this chain? (Y/N) \n")
                if choice.lower() == "y":
                    newLine()
                    print("Building...")
                    build_mono()
                    newLine()
                    print("*Build complete!*")
                    
        
        elif programChoice == "5":
            
            convert_sequence_to_family()
            
        elif programChoice == "6":
            
            pairwiseMismatchTable = generate_distance_matrix()
            Globals.lastGeneratedPairwiseMismatchTable = pairwiseMismatchTable   
            
            # Resets the other variables to avoid errors.
            Globals.lastGeneratedDynamicProgrammingMatrix = []
            Globals.rawMatrix = []
            Globals.gapScore = None
            
        elif programChoice == "7":
            
            if Globals.lastGeneratedPairwiseMismatchTable == []:
                
                newLine()
                print("Error: A pairwise mismatch table must first be generated.")
                newLine()
            else:
                Globals.lastGeneratedDynamicProgrammingMatrix,Globals.rawMatrix,Globals.gapScore = generate_dyanmic_programming_matrix(Globals.lastGeneratedPairwiseMismatchTable)
                
                
            
        elif programChoice == "8":
            
            if Globals.lastGeneratedPairwiseMismatchTable == [] or Globals.lastGeneratedDynamicProgrammingMatrix == [] or Globals.gapScore == None:
                            
                newLine()
                print("Error: Necessary matrices and gap score missing, try running the full alignment sequence instead.")
                newLine()            
            else:
                
                Globals.leftChannel,Globals.rightChannel = traceback(Globals.lastGeneratedDynamicProgrammingMatrix,Globals.rawMatrix,Globals.gapScore,Globals.lastGeneratedPairwiseMismatchTable)
        
        elif programChoice == "9":
            
            Globals.lastGeneratedPairwiseMismatchTable = generate_distance_matrix()
            time.sleep(0.5)
            Globals.lastGeneratedDynamicProgrammingMatrix,Globals.rawMatrix,Globals.gapScore = generate_dyanmic_programming_matrix(Globals.lastGeneratedPairwiseMismatchTable)
            time.sleep(0.5)
            Globals.leftChannel,Globals.rightChannel = traceback(Globals.lastGeneratedDynamicProgrammingMatrix,Globals.rawMatrix,Globals.gapScore,Globals.lastGeneratedPairwiseMismatchTable)
            #time.sleep(0.5)
        
        
        elif programChoice == "10":
            
            if Globals.leftChannel == [] or Globals.rightChannel == []:
                print("No alignment found, run alignment or traceback function to generate an alignment to build.")
            
            else:
            
                newLine()
                print("Last generated alignment:")
                print(Globals.leftChannel)
                print(Globals.rightChannel)
                newLine()
                choice = input("Do you wish to build this alignment into two sound files? (Y/N) \n")
                
                while choice not in ["y","n","Y","N"]:
                    print("Invalid choice")
                    newLine()
                    choice = input("Do you wish to build this alignment into two sound files? (Y/N) \n")
                
                if choice == "y" or choice == "Y":
                    build_from_alignment(Globals.leftChannel,Globals.rightChannel)
                    newLine()
                    print("Build complete!")
                    print("Sound files exported to Alignment (Left/Right) Channel.wav")
                
                else:
                    pass
        
        
        
        
        elif programChoice == "11":
            newLine()
            print("Enjoy Scambi! Shutting down...")
            newLine()
            time.sleep(0.5)
            return
        
        
        
        else:
            print("Invalid selection: please try again.")
            



main()


