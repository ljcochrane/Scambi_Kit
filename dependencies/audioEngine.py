# Audio engine. This library deals with all audio generation. 

# This is the build system to actually create a full scambi sound file. 
# It uses pydub and a previously generated build sequence.
#----------------------------------------------------------------------


import random

def convert_family_to_sequence(familyList):
    
    reverseFamilyDict = {'-':['-'],'A': ['1', '2'], 'B': ['2', '3'], 'C': ['3', '4'], 'D': ['4', '5'], 'E': ['5', '6'], 'F': ['6', '7'], 'G': ['7', '8'], 'H': ['8', '9'], 'I': ['9', '10'], 'J': ['10', '11'], 'K': ['11', '12'], 'L': ['12', '13'], 'M': ['13', '14'], 'N': ['14', '15'], 'O': ['15', '16'], 'P': ['16', '17'], 'AR': ['1r', '2r'], 'BR': ['2r', '3r'], 'CR': ['3r', '4r'], 'DR': ['4r', '5r'], 'ER': ['5r', '6r'], 'FR': ['6r', '7r'], 'GR': ['7r', '8r'], 'HR': ['8r', '9r'], 'IR': ['9r', '10r'], 'JR': ['10r', '11r'], 'KR': ['11r', '12r'], 'LR': ['12r', '13r'], 'MR': ['13r', '14r'], 'NR': ['14r', '15r'], 'OR': ['15r', '16r'], 'PR': ['16r', '17r']}
    outputList = []
    
    for family in familyList:
        
        sequence = random.choice(reverseFamilyDict[family])
        
        outputList.append(sequence)
        
    return outputList






def build_mono(sequenceToBuild):
    
    
    
    
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
    
    if leftChannelList == [] or rightChannelList == []:
        print("No alignment found, run alignment sequence to generate an alignment to build")
        return
    
    leftChannelSequences = convert_family_to_sequence(leftChannelList)
    rightChannelSequences = convert_family_to_sequence(rightChannelList)
    
    for index in range(len(leftChannelSequences)):
        
        leftChannelSequences[index] = leftChannelSequences[index] + ".wav"    
    
    
    for index in range(len(rightChannelSequences)):
            
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
    finalCompositionright.export("Alignment Right Channel.wav",format="wav")
    normalMode()   
    
    