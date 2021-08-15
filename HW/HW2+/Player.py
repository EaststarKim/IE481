class Player:
    def __init__(self):
        self.Hand = []
        self.score = 0
        self.actionLast = 'Hit'

    def action(self,observedCards,valueCards,actionLastOpp,scoreOpp):
        print("(H)it or (P)ass ??? Type!")
        action = input()
        if action == 'H' or action == 'h':
            self.Hand.append(observedCards[0])
            self.score = self.score + valueCards[observedCards[0]]
            self.actionLast = 'Hit'
        else:
            self.actionLast = 'Pass'
        return self.actionLast
