import SortingAlgorithm
import BagOfWordCreator
from HashTable import HashTable
from PriorityLinkedList import PriorityNode, PriorityLinkedList

class VerySimpleSearchEngine:

    def __init__(self,folder,maxFileNumber,hashSize):
        dataset = BagOfWordCreator.BagOfWord(folder,maxFileNumber,hashSize,hash=True)
        self.words = dataset.words
        self.bows = dataset.bows
        self.files = dataset.files
        self.numDocuments = len(self.bows)
        self.hashWordDocument = HashTable(100)
        self.createWordDocumentTable()

    def createWordDocumentTable(self):
        for itrWord in range(len(self.words)):
            strWord = self.words[itrWord]
            lstWordFrequency = PriorityLinkedList()
            for itrDoc in range(self.numDocuments):
                if itrWord in self.bows[itrDoc].keys():
                    lstWordFrequency.insertWithPriority(PriorityNode(self.bows[itrDoc][itrWord],self.files[itrDoc]))
            self.hashWordDocument.put(strWord,lstWordFrequency)

    def query(self,strQuery):
        lstQueryWords = strQuery.split()
        hashResult = HashTable(100)
        for strQueryWord in lstQueryWords:
            for char in ' ?.!/;:()-<>_\\[]{}':
                strQueryWord = strQueryWord.replace(char,'')
            strQueryWord = strQueryWord.lower()
            lstPriorityDocs = self.hashWordDocument.get(strQueryWord)
            if lstPriorityDocs == None:
                continue
            nodePriorityDoc = lstPriorityDocs.getHead().getNext()
            while(nodePriorityDoc!=lstPriorityDocs.getTail()):
                intNewPriority = nodePriorityDoc.getPriority()
                if hashResult.get(nodePriorityDoc.getValue()) != None:
                    intNewPriority = intNewPriority + hashResult.get(nodePriorityDoc.getValue())
                hashResult.put(nodePriorityDoc.getValue(),intNewPriority)
                nodePriorityDoc = nodePriorityDoc.getNext()

        lstFrequency = []
        lstDocument = []

        lstKeysInResult = hashResult.keys
        for key in lstKeysInResult:
            lstFrequency.append(hashResult.get(key))
            lstDocument.append(key)

        sorting = SortingAlgorithm.QuickSort()
        lstDocument, lstFrequency = sorting.performSorting(lstFrequency,lstDocument)

        cnt = 0
        for itr in range(len(lstDocument)):
            self.printItem(lstDocument[itr],lstFrequency[itr])
            cnt = cnt + 1
            if cnt > 4:
                break

    def printItem(self,strDocument,intFrequency):
        print(str(intFrequency) + " : " + strDocument)
        file = open(strDocument, "r")
        cntLine = 0
        strFirstLines = ''
        while (True):
            line = file.readline()
            if not line:
                break
            if cntLine > 10:
                strFirstLines = strFirstLines + " " + line
            if cntLine > 25:
                break
            cntLine = cntLine + 1
        for char in '\n\t':
            strFirstLines = strFirstLines.replace(char,' ')
        print(strFirstLines)
        file.close()


if __name__ == "__main__":

    engine = VerySimpleSearchEngine('./20_newsgroups', 3000,20)

    print("Initialized................................")
    print("Num of Document : "+str(engine.numDocuments))
    print("Num of Word : " + str(len(engine.words)))

    while(True):
        print()
        strQuery = input("Search Phrase : ")
        #strQuery = 'people dead ashes victory'
        if strQuery == 'quit':
            break
        tree = engine.query(strQuery)
        #Wbreak
