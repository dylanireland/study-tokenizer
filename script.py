import re
import sys

dict = {}

def rec(fileIndex):
    countedInFile = {}
    with open("texts/" + str(fileIndex) + ".txt", 'r') as text:
        # ^Open Current Study
        document = text.read().replace('\n', '')
        #^ Make study into single long ass string
        for phraseIndex in range(10):
            #^ Iterate for each phrase length for phrases up to 10 words in length
            phraseCount = phraseIndex + 2
            #^ Start at phraseLength of 2 to avoid single words which aren't helpful, this ends up making max phrase count 11 but whatever
            for offset in range(phraseCount):
                #^ Perform lookup on each delimiter iteration.
                #^ Example: "This is a test document" -> ["this is", "a test", "document"], ["this is a", "test document"], ["this is a test", "document"], ["this is a test document"]
                if offset > 0:
                    #^ If offset is 0 no need for below for loop
                    for i in range(offset):
                        document = document[(document.find(" ") + 1):]
                        #^ Shift one word to the right to start tokenizing. Acts as the offsetter

                words = re.findall(" ".join(["[^\s]+"] * phraseCount), document)
                #^ Creates phrase by joining words with a space then splitting on delimiter determined by above regular expression which is
                #^ multiplied by the phraseCount to make strings separated by phraseCount - 1 number of spaces

                for word in words:
                    #^ Word really meaning phrase here, for phrase in list of phrases
                    word = re.sub(r'[^\w\s]','',word).lower().strip()
                    #^ Replace all punctuation with blank string, lower the case, and strip leading and trailing whitespace
                    if len(word.split(" ")) == phraseCount:
                        #^ If word count in phrase is equal to phraseCount, add to dictionary below
                        dict[word] = (dict[word][0] + 1, (dict[word][1] + 1 if not word in countedInFile else dict[word][1])) if word in dict else (1, 1)
                        #^ Creates or increments object stored at location "word" in a dictionary. Given a word, if it exists in the dictionary already, will increment its occurrence count,
                        #^ and will increment its appearance count if countedInFile[word] == False. If word is not in dict, log its file appearances and number of occurrences as 1 and 1
                        countedInFile[word] = True
                        #^ Log that this word has now already been found in this file and don't increment again for this file

            print("{}th phrase length".format(phraseCount))
            #^ So I know it's doing stuff


    print("{}% COMPLETE".format(fileIndex/82*100))
    #^ So I know it's doing stuff
    if fileIndex == 82:
        return
        #^ If we've now searched through all the files, exit back to line 60
    rec(fileIndex + 1)
    #^ If we're not at file 82, dont return and have the function call itself again with an incremented fileIndex



lines = int(sys.argv[1] or 0)
if lines == 0:
    exit("Include lines!")
#^Specify output file line count with command line arguments



rec(0)
#^THIS RUNS THE ALGORITHM; CALLS RECURSIVE FUNCTION AT LINE 6



def makeOutfile(dicti, outname):
    with open(outname, "w+") as outfile:
        #^ Creates File for output
        keys = list(dicti)
        dictLength = len(dicti)
        for i in range(dictLength):
            key = keys[dictLength - 1 - i]
            occurrences = dicti[key][0]
            appearances = dicti[key][1]
            outfile.write("Key: " + str(key) + " ----- Number of occurrences: " + str(occurrences) + " ----- Number of file appearances: " + str(appearances) + "\n")
            if i > lines:
                break



appSort = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1][1])}
occSort = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1][0])}
makeOutfile(appSort, "appearancesSorted.txt")
makeOutfile(occSort, "occurrencesSorted.txt")
