import numpy as np

class Game(object):
    
    def __init__(self):
        self.symbols = ["c", "d", "h", "s"]
        self.cards  = [ 
            ["A", self.symbols], 
            [2,   self.symbols], 
            [3,   self.symbols],
            [4,   self.symbols],
            [5,   self.symbols],
            [6,   self.symbols],
            [7,   self.symbols],
            [8,   self.symbols],
            [9,   self.symbols],
            [10,  self.symbols],
            ["J", self.symbols],
            ["Q", self.symbols],
            ["K", self.symbols],
        ]
        self.playedCards = []
        self.totalCards  = 52
        self.countCards  = 0
        self.cardsInHand = 0

    def initGame(self, number, symbol):
        playedCard = number+symbol
        self.playedCards.append(playedCard)
        if  self.isAlreadyEvaluated(playedCard) == False:
            self.deleteCardInArray(number, symbol)
            self.cardsInHand += 1
            return True
        return False

    #cards [ A , 10 ]
    def evaluateHand(self, cards):
        #see later for case if 2 Aces in hand
        aceInHand = False
        totalPoints = 0
        for card in cards:
            if card.isnumeric() == False:
                if(card == "A"):
                    totalPoints += 11
                    aceInHand = True
                    self.countCards += -1
                else:
                    totalPoints += 10
                    self.countCards += -1
            else:
                if(card == 10):
                    self.countCards += -1
                elif(card >= 7 <= 9):
                    self.countCards += 1
                totalPoints += card
        return self.decideIfPlayQuitOrAnotherCard(totalPoints, aceInHand)
        

    def decideIfPlayQuitOrAnotherCard(self, totalPoints, aceInHand):
        if totalPoints > 21:
            if aceInHand:
                totalPoints -= 10
                aceInHand = False
                return self.decideIfPlayQuitOrAnotherCard(totalPoints, aceInHand)
            else:
                #Here I loss so i can not play 
                return False
        elif totalPoints > 17:
            #Here I probably in the next turn i go to loss so i not play 
            return False
        elif totalPoints <= 13:
            #Here I play
            return True

    def seeProbabilityOfGetNeededCard(self, totalPoints):
        needValue = 21 - totalPoints
        count = 0
        for x in self.cards: 
            for y in x:
                if y[0].isnumeric() == False:
                    if(y[0] == "A"):
                        if needValue <= 1 or needValue <= 11 :
                            count+= 1
                    else:
                        if needValue <= 10 :
                            count+= 1
                else:
                    for u in range(len(y[1]) ):
                        if(y[1][u] <= needValue):
                            count+= 1
        probability = (count/self.totalCards)*100
        return probability 

    def deleteCardInArray(self,number, symbol):
        for x in self.cards: 
            for y in x:
                if y[0] == number:
                    for u in range(len(y[1]) ):
                        if( y[1][u]  == symbol):
                            y[1].pop(u)
                            self.totalCards -= 1
                            return True

    def isAlreadyEvaluated(self, card):
        for i in self.playedCards:
            if i == card:
                return True
        return False