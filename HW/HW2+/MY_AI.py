class MY_AI:
    def __init__(self):
        self.Hand = []
        self.score = 0
        self.actionLast = 'Hit'
    # score1(AI's score), score2(Opponent's turn), turn=0(AI's turn) or 1, last=0(last action==Pass) or 1
    def comp(self,score1,score2):
        if score1==score2:
            return 1.5
        return (score1<score2)+1
    def Recursion(self,score1,score2,turn,last,cards):
        if score1>21:
            self.table[score1][score2][turn][last]=2
        elif score2>21:
            self.table[score1][score2][turn][last]=1
        elif score1==21:
            self.table[score1][score2][turn][last]=1
        elif score2==21:
            self.table[score1][score2][turn][last]=2
        elif len(cards)==0:
            self.table[score1][score2][turn][last]=1.5
        if self.table[score1][score2][turn][last]>0:
            return self.table[score1][score2][turn][last]
        if turn==0:
            if last==0:
                self.table[score1][score2][turn][last]=min(self.Recursion(score1+cards[0],score2,1,1,cards[1:]),self.comp(score1,score2))
            else:
                self.table[score1][score2][turn][last]=min(self.Recursion(score1+cards[0],score2,1,1,cards[1:]),self.Recursion(score1,score2,1,0,cards))
        else:
            if last==0:
                self.table[score1][score2][turn][last]=max(self.Recursion(score1,score2+cards[0],0,1,cards[1:]),self.comp(score1,score2))
            else:
                self.table[score1][score2][turn][last]=max(self.Recursion(score1,score2+cards[0],0,1,cards[1:]),self.Recursion(score1,score2,0,0,cards))
        return self.table[score1][score2][turn][last]
    def createMemoizationTable(self,observedCards,valueCards,actionLastOpp,scoreOpp):
        self.table=[[[[0,0],[0,0]] for i in range(40)] for i in range(40)]
        cards=[]
        for i in observedCards:
            cards.append(valueCards[i])
        self.Recursion(self.score,scoreOpp,0,int(actionLastOpp=='Hit'),cards)
        if actionLastOpp=='Pass':
            self.table[self.score][scoreOpp][1][0]=self.comp(self.score,scoreOpp)
        return self.table[self.score+cards[0]][scoreOpp][1][1]<=self.table[self.score][scoreOpp][1][0]
    def action(self,observedCards,valueCards,actionLastOpp,scoreOpp):
        #print("Observed Cards : " + str(observedCards))
        select=self.createMemoizationTable(observedCards,valueCards,actionLastOpp,scoreOpp)
        if select:
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
