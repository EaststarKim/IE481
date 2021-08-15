import random

class Blackjack:
    def __init__(self,numObserved):
        self.numObserved = numObserved
        self.cards = []
        self.valueCards = {}
        types = ['Clover', 'Spade', 'Heart', 'Diamond']
        numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        for type in types:
            for j in range(len(numbers)):
                card = numbers[j] + '-' + type
                self.cards.append(card)
                self.valueCards[card] = j+1

        random.shuffle(self.cards)
        self.tblSelect = [None]*1000
        self.tblBestSelect = [None]
        self.tblRemaining = [None]*1000
        self.lstAIHand = []
        self.lstPlayerHand = []
        self.scoreAI = 0
        self.scorePlayer = 0
        self.round = 0
        self.idxCard = 0
        self.actionLastPlayer = 'Hit'
        self.actionLastAI = 'Hit'

    def iterate(self):
        stop = False
        while stop == False:
            self.showCurrentObservedCards()
            self.actionPlayer()
            self.actionAI()
            stop = self.checkWinning()

    def showCurrentObservedCards(self):
        print ("-------------------------------------------------")
        self.observedCards = self.cards[self.idxCard:min(len(self.cards),self.idxCard+self.numObserved)]
        print ("Round : "+str(self.round))
        print(self.observedCards)
        print("AI Current Score : "+str(self.scoreAI))
        print("AI's Hand : "+str(self.lstAIHand))
        print("Player Current Score : " + str(self.scorePlayer))
        print("Player's Hand : " + str(self.lstPlayerHand))
        self.round = self.round + 1

    def checkWinning(self):
        print("AI Current Score : "+str(self.scoreAI))
        print("Player Current Score : " + str(self.scorePlayer))
        if self.scorePlayer > 21:
            print ("Player Lose!")
            return True
        if self.scoreAI > 21:
            print("AI Lose!")
            return True
        if self.scorePlayer == 21:
            print("Player Win!")
            return True
        if self.scoreAI == 21:
            print("AI Win!")
            return True
        if self.actionLastAI == 'Pass' and self.actionLastPlayer == 'Pass':
            if self.scorePlayer > self.scoreAI:
                print ("Player Win!")
                return True
            elif self.scoreAI > self.scorePlayer:
                print ("AI Win!")
                return True
            else:
                print ("Tie, Both Wins!")
                return True
        return False

    def actionPlayer(self):
        print("Player Cards to Play : " + self.observedCards[0])
        print("(H)it or (P)ass ??? Type!")
        action = input()
        if action == 'H' or action == 'h':
            self.idxCard = self.idxCard + 1
            self.lstPlayerHand.append(self.observedCards[0])
            self.scorePlayer = self.scorePlayer + self.valueCards[self.observedCards[0]]
            self.observedCards.remove(self.observedCards[0])
            self.actionLastPlayer = 'Hit'
        else:
            self.actionLastPlayer = 'Pass'

	# Homework task
	# self.tblSelect[index = self.scoreAI] : selected cards from the observed cards + current hand(self.lstAIHand)
	# self.tblRemaining[index = self.scoreAI] : cards for selection (initially at the method beginning : self.observedCards), each element is a list
	# self.tblBestSelect : the selection set closest to 21	
    def createMemoizationTable(self):
        self.tblSelect = [None]*1000
        self.tblBestSelect = [None]
        self.tblRemaining = [None]*1000

        self.tblSelect[self.scoreAI] = self.lstAIHand.copy()
        self.tblRemaining[self.scoreAI] = self.observedCards.copy()
        print("AI Observed Cards : "+str(self.observedCards))

        for i in range(self.scoreAI,21):
            if self.tblRemaining[i]==None:
                continue
            while len(self.tblRemaining[i])>0:
                j=i+self.valueCards[self.tblRemaining[i][0]]
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
                print("INSIDE AI : AI Expected Total Score : "+str(i))
                print("INSIDE AI : AI Selected Cards : "+str(self.tblSelect[i]))
                self.tblBestSelect = self.tblSelect[i]
                break


    def actionAI(self):
        self.createMemoizationTable()
        print("AI Cards to Play : "+self.observedCards[0])
        if self.observedCards[0] in self.tblBestSelect:
            self.actionLastAI = 'Hit'
        else:
            if self.actionLastPlayer == 'Hit':
                self.actionLastAI = 'Pass'
            else:
                if self.scoreAI < self.scorePlayer:
                    print("INSIDE AI : AI cannot pass because Player will win if AI pass")
                    self.actionLastAI = 'Hit'
                else:
                    self.actionLastAI = 'Pass'
        print("AI "+self.actionLastAI)
        if self.actionLastAI == 'Hit':
            self.idxCard = self.idxCard + 1
            self.lstAIHand.append(self.observedCards[0])
            self.scoreAI = self.scoreAI + self.valueCards[self.observedCards[0]]
            self.observedCards.remove(self.observedCards[0])

if __name__ == "__main__":

    b = Blackjack(5)
    b.iterate()