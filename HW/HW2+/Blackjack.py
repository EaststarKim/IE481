import random
import Player as pl
import HW_AI as hw
import MY_AI as my

class Blackjack:
    def __init__(self,numObserved,ptype1,ptype2):
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
        self.round = 0

        self.p1 = self.generatePlayer(ptype1)
        self.p2 = self.generatePlayer(ptype2)
    def generatePlayer(self,type):
        if type==1:
            return hw.HW_AI()
        if type==2:
            return my.MY_AI()
        return pl.Player()
    def iterate(self):
        stop=0
        while stop == 0:
            #self.showCurrentObservedCards()
            self.p1.action(self.cards[:self.numObserved],self.valueCards,'Hit',self.p2.score)
            #print("P1 " + self.p1.actionLast)
            if self.p1.actionLast=='Hit':
                self.cards.remove(self.cards[0])
            self.p2.action(self.cards[:self.numObserved],self.valueCards,self.p1.actionLast,self.p1.score)
            #print("P2 " + self.p2.actionLast)
            if self.p2.actionLast=='Hit':
                self.cards.remove(self.cards[0])
            #print("P1 Current Score : " + str(self.p1.score))
            #print("P2 Current Score : " + str(self.p2.score))
            stop = self.checkWinning()
        # self.Winner(stop)
        return stop
    def showCurrentObservedCards(self):
        print ("-------------------------------------------------")
        print ("Round : "+str(self.round))
        print(self.cards[:self.numObserved])
        print("P1's Hand : "+str(self.p1.Hand))
        print("P2's Hand : "+str(self.p2.Hand))
        self.round = self.round + 1
    def checkWinning(self):
        if self.p1.score > 21:
            return 2
        if self.p2.score > 21:
            return 1
        if self.p1.score == 21:
            return 1
        if self.p2.score == 21:
            return 2
        if self.p1.actionLast == 'Pass' and self.p2.actionLast == 'Pass':
            if self.p1.score > self.p2.score:
                return 1
            elif self.p1.score < self.p2.score:
                return 2
            else:
                return 3
        return 0
    def Winner(self,type):
        if type==1:
            print("P1 Win!")
        if type==2:
            print("P2 Win!")
        if type==3:
            print("Tie")

if __name__ == "__main__":

    #----------------AI Battle!!!!----------------#
    tot=200
    win=0
    tie=0
    coin=random.randrange(0,2)
    if coin==0:
        print("HW_AI goes first")
    else:
        print("MY_AI goes first")
    for i in range(tot):
        b=Blackjack(5,coin+1,2-coin)
        result=b.iterate()
        print("Match :",i+1)
        if coin==0:
            print("HW_AI Score :",b.p1.score)
            print("MY_AI Score :",b.p2.score)
        else:
            print("MY_AI Score :", b.p1.score)
            print("HW_AI Score :", b.p2.score)
        if result==2-coin:
            win+=1
        elif result==3:
            tie+=1
        print("Match Record (",win,"/",tie,"/",i-win-tie+1,")")
        print("-------------------------------------------------")
    print("For",tot,"matches,")
    print("MY_AI won",win,"matches and halved",tie,"matches")