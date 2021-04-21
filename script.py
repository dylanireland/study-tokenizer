import re
import sys

dict = {}

extraneousWords = open("extraneous_words.txt", "r").readlines()
#^ Read words in as lists

extraneousWords = [x.strip() for x in extraneousWords]
#^ Remove newline characters from the end of each word

def rec(fileIndex):
    countedInFile = {}
    with open("texts/" + str(fileIndex) + ".txt", 'r') as text:
        #^ Open Current Study
        document = text.read().replace('\n', '')
        #^ Make study into single long ass string
        for phraseIndex in range(10):
            #^ Iterate for each phrase length for phrases up to 10 words in length
            phraseCount = phraseIndex + 2
            #^ Start at phraseLength of 2 to avoid single words which aren't helpful, this ends up making max phrase count 11 but whatever
            for offset in range(phraseCount):
                #^ Perform lookup on each delimiter iteration.
                #^ Example: "This is a test document" -> ["this is", "a test"], ["is a", "test document"]
                if offset > 0:
                    #^ If offset is 0 no need for below for loop
                    for i in range(offset):
                        document = document[(document.find(" ") + 1):]
                        #^ Shift one word to the right to start tokenizing. Acts as the offsetter.

                words = re.findall(" ".join(["[^\s]+"] * phraseCount), document)
                #^ Creates phrase by splitting on each Nth space character. the regular
                #^ expression above will match to a set of words separated by phraseCount - 1 spaces

                for word in words:
                    #^ Word really meaning phrase here, for phrase in list of phrases
                    word = re.sub(r'[^\w\s]','',word).lower().strip()
                    #^ Replace all punctuation with blank string, lower the case, and strip leading and trailing whitespace
                    extraneousWordCount = 0
                    if phraseCount < 4:
                        #^ Only perform extraneous word check on phrases less than 4 words in length
                        for w in word.split(" "):
                            if w in extraneousWords:
                                extraneousWordCount = extraneousWordCount + 1
                        #^ For each word in phrase, see if it is listed as an extraneous word and if it is,
                        #^ increment extraneousWordCount. Then below, if extraneousWordCount == length(wordsInPhrase), we know that
                        #^ all the words in the phrase are extraneous words, making it an extraneous phrase, and we dont include it

                    if len(word.split(" ")) == phraseCount and extraneousWordCount != len(word.split(" ")):
                        #^ If word count in phrase is equal to phraseCount and not all words in phrase are extraneous, add to dictionary below
                        dict[word] = (dict[word][0] + 1, (dict[word][1] + 1 if not word in countedInFile else dict[word][1])) if word in dict else (1, 1)
                        #^ Creates or increments object stored at location "word" in a dictionary. Given a word, if it exists in the dictionary already,
                        #^ will increment its occurrence count, and will increment its appearance count if countedInFile[word] == False. If word is not
                        #^ in dict, log its file appearances and number of occurrences as 1 and 1
                        countedInFile[word] = True
                        #^ Log that this word has now already been found in this file and don't increment again for this file

            print("{}th phrase length".format(phraseCount))
            #^ So you know it's working
            #^ Yes I'm aware it prints 2th 3th etc

    print("{}% COMPLETE".format(fileIndex/82*100))
    #^ So you know it's working
    if fileIndex == 82:
        return
        #^ If we've now searched through all the files, exit back to line 84
    rec(fileIndex + 1)
    #^ If we're not at file 82, dont return and have the function call itself again with an incremented fileIndex


if len(sys.argv) < 2:
    print("Please include line count of outfile. Example: python3 script.py 5000")
    exit()
lines = int(sys.argv[1] or 0)
#^ Specify output file line count with command line arguments



rec(0)
#^ THIS RUNS THE ALGORITHM; CALLS RECURSIVE FUNCTION rec(fileIndex) AT LINE 16



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
            if i == lines - 1:
                break



appSort = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1][1])}
occSort = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1][0])}
makeOutfile(appSort, "appearances_sorted.txt")
makeOutfile(occSort, "occurrences_sorted.txt")
