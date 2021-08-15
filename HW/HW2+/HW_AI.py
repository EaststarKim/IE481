class HW_AI:
    def __init__(self):
        self.Hand = []
        self.score = 0
        self.actionLast = 'Hit'

    def createMemoizationTable(self,observedCards,valueCards):
        self.tblSelect = [None]*1000
        self.tblBestSelect = [None]
        self.tblRemaining = [None]*1000

        self.tblSelect[self.score] = self.Hand.copy()
        self.tblRemaining[self.score] = observedCards.copy()
        #print("Observed Cards : "+str(observedCards))

        for i in range(self.score,21):
            if self.tblRemaining[i]==None:
                continue
            while len(self.tblRemaining[i])>0:
                j=i+valueCards[self.tblRemaining[i][0]]
                if j>21:
                    self.tblRemaining[i].remove(self.tblRemaining[i][0])
                    continue
                if self.tblSelect[j]!=None:
                    self.tblRemaining[i].remove(self.tblRemaining[i][0])
                    continue
                self.tblSelect[j]=self.tblSelect[i].copy()
                self.tblSelect[j].append(self.tblRemaining[i][0])
                self.tblRemaining[i].remove(self.tblRemaining[i][0])
                self.tblRemaining[j]=self.tblRemaining[i].copy()

        for i in range(21,-1,-1):
            if self.tblSelect[i]!=None:
                self.tblBestSelect = self.tblSelect[i]
                break

    def action(self,observedCards,valueCards,actionLastOpp,scoreOpp):
        self.createMemoizationTable(observedCards,valueCards)
        if observedCards[0] in self.tblBestSelect:
            self.actionLast = 'Hit'
        else:
            if actionLastOpp == 'Hit':
                self.actionLast = 'Pass'
            else:
                if self.score < scoreOpp:
                    self.actionLast = 'Hit'
                else:
                    self.actionLast = 'Pass'
        if self.actionLast == 'Hit':
            self.Hand.append(observedCards[0])
            self.score = self.score + valueCards[observedCards[0]]
        return self.actionLast
