# AUTHOR - ZAK FORSTER
# DATE - 29/03/2018
# PURPOSE - TO SIMULATE A CACHE THAT USES LRU REPLACEMENT, OUTPUTTING A TXT FILE CONTAINING AN ARRAY OF C OR M
# C IF THE ADDRESS WAS ACCESSED FROM THE CACHE, M IF ACCESSED FROM MEMORY
import os

# OPENS THE PASSED FILE
# READS EACH LINE OF THE FILE INTO AN ARRAY AND RETURNS THAT ARRAY
def openFile(fileName):
    with open(fileName) as file:
        linesList = file.readlines()
        linesList = [x.strip() for x in linesList]
    return linesList

# CALCULATES INFORMATION ABOUT THE CACHE USING THE FIRST LINE OF THE FILE, STORING THE INFO IN A DICTIONARY 
# A DICTIONARY OPERATES IN A SIMILAR WAY TO A JAVA HASHMAP
def extractInfo(linesList):
    firstLine = linesList[0].split()
    d = {}
    d.update({"Word / Address Bits":int(firstLine[0])})
    d.update({"Cache Bytes":int(firstLine[1])})
    d.update({"Blocks Bytes":int(firstLine[2])})
    d.update({"No Blocks":int(firstLine[1])/int(firstLine[2])})
    d.update({"Index":binaryToIndexLines(bin(int(d["No Blocks"])))})
    d.update({"Block Contains Lines":int(firstLine[3])})
    d.update({"Bytes in a Line":int(d["Blocks Bytes"])/int(d["Block Contains Lines"])})
    d.update({"Offset":binaryToIndexLines(bin(int(d["Bytes in a Line"])))})
    print d
    return d

# RETURNS LENGTH OF THE INDEX OF A BINARY LINE
def binaryToIndexLines(binary):
    num = -1
    for x in range(2,len(binary)):
        num = num + 1
    return num

# TAKES A LINE FROM THE FILE, AND THE CACHE INFORMATION AS PARAMETERS
# CONVERTS THE LINE TO BINARY AND REMOVES EXTRA CHARACTERS THAT PYTHON PUTS IN FRONT (0B)
# ADDS THE NECESSARY BITS TO THE LINE TO ENSURE THE ADDRESS MEETS THE WORD SIZE
# RETURNS THE FILLED BINARY NUMBER WITH THE CORRECT NUMBER OF BITS
def convertToBinary(line,cacheInfo):
    unModifiedbinaryLine = bin(int(line))
    strippedBinary = ""
    for x in range(2,len(unModifiedbinaryLine)):
        strippedBinary = strippedBinary + unModifiedbinaryLine[x]
    neededZeros = int(cacheInfo["Word / Address Bits"]) - len(strippedBinary)
    correctBinary = strippedBinary
    for x in range(0,neededZeros):
        correctBinary = "0" + correctBinary
    return correctBinary 

# TAKES A BINARY LINE, AND THE CACHE INFO AS PARAMETERS
# CALCULATES THE TAG SIZE AND TAG
# CALCULATES THE INDEX AND OFFSET
# STORES THIS INFO IN A DICTIONARY AND RETURNS IT 
def splitTagIndexOffset(binaryVal,cacheInfo):
    split = {}
    tagSize = cacheInfo["Word / Address Bits"] - (cacheInfo["Index"] + cacheInfo["Offset"])
    tag = ""
    index = ""
    offset = ""
    for i in range(0,len(binaryVal)):
        if(i < tagSize):
            tag = tag + binaryVal[i]
        elif(i >= tagSize and i < (tagSize + cacheInfo["Index"])):
            index = index + binaryVal[i]
        elif(i >= (tagSize + cacheInfo["Index"]) and i < (tagSize + cacheInfo["Index"] + cacheInfo["Offset"])):
            offset = offset + binaryVal[i]
    split.update({"Tag":tag})
    split.update({"Index":index})
    split.update({"Offset":offset})
    return split

# RETURNS THE NUMBER OF UNIQUE INDEXES (NEEDED AS IF YOU HAVE 4 BLOCK, BUT ONLY USE 2 INDEXES, YOU ONLY NEED 2 BLOCKS)
def getUniqueIndexes(memory):
    unique = -1
    last = []
    for addr in memory:
        if(not(addr["Index"] in last)):
            last.append(addr["Index"])
    return last
        
# THE LOGIC OF THE PROGRAM
def program(fileName):
    linesList = openFile(fileName)
    cacheInfo = extractInfo(linesList)
    # INITALISES ALL NECESSARY ARRAYS
    memory = []
    blocks = []
    operations = []
    blockLines = cacheInfo["Block Contains Lines"]
    # LOOPS THROUGH ALL OF LINES IN MEMORY, ADDS EACH ADDRESS WITH INDEX, OFFSET AND TAG CALCULATED INTO THE MEMORY ARRAY
    for i in range(1,len(linesList)):
        memory.append(splitTagIndexOffset(convertToBinary(linesList[i],cacheInfo),cacheInfo))
    #for i in memory:
    #    print str(i)
    allIndexes = getUniqueIndexes(memory)
    uniqueIndexes = len(allIndexes)
    # INITALISES ALL BLOCKS BY ASSOCIATING EACH WITH A UNIQUE INDEX
    for index in allIndexes:
        blocks.append([{"Index":index}])
    print "Unique Indexes: " + str(uniqueIndexes)
    print "Initalised Blocks: " + str(blocks)
    print "Number of Lines in Block " + str(blockLines)
    # LOOP THROUGH EACH ADDRESS IN MEMORY
    for addr in memory:
        #print "address is " + str(addr["Tag"])
        # LOOP THROUGH EACH BLOCK IN THE BLOCK ARRAY
        for block in blocks:
            # IF THE ADDRESS INDEX IS EQUAL TO THE INDEX OF THE CURRENT BLOCK
            if(addr["Index"] == block[0]["Index"]):
                # IF THE BLOCK CONTAINS LESS ELEMENTS THAT ITS NUMBER OF LINES PERMITS
                if(len(block)-1 < blockLines):
                    #print str(blockLines) + " " + str(len(block) - 1)
                    # IF THE BLOCK HAS NO TAGS IN IT
                    if(len(block) - 1 == 0):
                        # ADD A TAG TO THE BLOCK AND ADD M TO THE LIST OF OPERATIONS
                     #   print "BEFORE " + str(block)
                        block.append(addr["Tag"])
                        operations.append("M")
                     #   print "AFTER " + str(block) + " OPERATION M \n"
                     # IF THE BLOCK IS NOT FULL, BUT HAS MORE THAN 1 ELEMENT IN IT
                    else:
                        # Loop through each element in the block (ignoring the dictionary which is at pos 0)
                        for i in range(1,len(block)):
                            # if the tag is found
                            if(block[i] == addr["Tag"]):
                                #push the found element to the front and shift everything else back 1 place
                              #  print "BEFORE " + str(block)
                                block.append(addr["Tag"])
                                block.remove(block[i])
                                operations.append("C")
                               # print "AFTER " + str(block) + " OPERATION C \n"
                                break # break because you added a new element thus it will loop over the same element and append c again as it hits the same tag
                            else:
                                # if you hit the last element and still havent found the tag in the cache
                                if(i == len(block) - 1):
                                   # print "BEFORE " + str(block)
                                    block.append(addr["Tag"])
                                    #print "AFTER " + str(block) + " OPERATION M \n"
                                    operations.append("M")
                                     # exit the loop as a new element has been added 
                                    #Dont remove the first element as the cache isn't full yet
                # if the cache is full                    
                else:
                    # Loop through each element in the block (ignoring the dictionary which is at pos 0)
                    for i in range(1,len(block)):
                        # if the tag is found
                        if(block[i] == addr["Tag"]):
                            #push the found element to the front and shift everything else back 1 place
                           # print "BEFORE " + str(block)
                            block.append(addr["Tag"])
                            block.remove(block[i])
                            operations.append("C")
                            #print "AFTER " + str(block) + " OPERATION C \n"
                            break # break because you added a new element thus it will loop over the same element and append c again as it hits the same tag
                        else:
                            # if you hit the last element and still havent found the tag in the cache
                            if(i == len(block) - 1):
                                #print "BEFORE " + str(block)
                                block.append(addr["Tag"])
                                #print "AFTER " + str(block) + " OPERATION M \n"
                                operations.append("M")
                    
    #print blocks
    #print operations
    return operations

def getAllFiles():
    files = []
    for file in os.listdir("PUT FILE DIRECTORY HERE"):
        if file.endswith(".in"):
            files.append(file)
    return files

def saveToFile(fileName,array):
    f = open(fileName+".result.txt","w+")
    f.write(str(array))
    f.close()
        
def main(): 
    allFiles = getAllFiles()
    for file in allFiles:
        print "Operating on: " + file
        print "Starting To Calculate Answer"        
        saveToFile(file,program(file))
        print "Solution Found!"
    print "Calculated Solution For All Files !"

main()