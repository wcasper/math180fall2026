#!/usr/bin/python

import random

class card:
  suit = 0  # 0 = d, 1 = c, 2 = h, 3 = s
  rank = 0  # 1 = A, 2 = 2, ...
  face = 0  # 0 = down, 1 = up

  def __init__(self, s, r):
    self.suit = s
    self.rank = r
    self.face = 0

class deck:
  cards = []
  def __init__(self):
    for r in range(1,14):
      for s in range(4):
        c = card(s,r)
        self.cards.append(c)

  def shuffle(self):
    random.shuffle(self.cards)

class board:

  def __init__(self):
    # create and shuffle deck
    self.d = deck()
    self.d.shuffle()

    # create columns
    self.columns = [[0],[1,2],[3,4,5],[6,7,8,9],[10,11,12,13,14],[15,16,17,18,19,20],[21,22,23,24,25,26,27]]

    # flip leading card of each column face up
    for k in range(len(self.columns)):
      self.d.cards[self.columns[k][-1]].face = 1  

    # put remaining cards in draw deck
    self.deck = list(range(28,52))
    for k in self.deck:
      self.d.cards[k].face = 1   # consider all deck cards face up
    self.hand = []

    # create empty scoring area
    self.scoring = [[],[],[],[]]

  def try2scorecard(self,k):
    for i in range(4):
      scorerank = 0
      if(len(self.scoring[i])):
        scorerank = self.d.cards[self.scoring[i][-1]].rank
        scoresuit = self.d.cards[self.scoring[i][-1]].suit
      if(scorerank + 1 == self.d.cards[k].rank):
        if(scorerank == 0 or scoresuit == self.d.cards[k].suit):
          self.scoring[i].append(k)
          return True
    return False


  # try to move any available cards to the score area
  def try2score(self):
    nscore = 0
    # try to score the leading card in the hand
    if(len(self.hand)):
      if(self.try2scorecard(self.hand[-1])):
        # remove placed card
        self.hand.pop()
        scored = True
        return 1
      
    # try to score the leading card in each column
    for i in range(len(self.columns)):
      if(len(self.columns[i])):
        if(self.try2scorecard(self.columns[i][-1])):
          scored = True
          # remove placed card
          self.columns[i].pop()
          # make next card face up
          if(len(self.columns[i])):
            self.d.cards[self.columns[i][-1]].face = 1
          return 1

    return 0

  # try to move any revealed kings to open spaces
  def search4king(self):
    freespot = -1
    kingspot = -1
    kingsdep = -1

    for i in range(len(self.columns)):
      if(len(self.columns[i]) == 0):
        freespot = i
      else:
        for j in range(len(self.columns[i])):
          if(self.d.cards[self.columns[i][j]].face):
            break
        if(j > 0 and self.d.cards[self.columns[i][j]].rank == 13):
          kingspot = i
          kingsdep = j

    if(freespot >= 0):
      if(kingspot >= 0):
        for jj in range(kingsdep,len(self.columns[kingspot])):
          self.columns[freespot].append(self.columns[kingspot][jj])
        self.columns[kingspot] = self.columns[kingspot][:kingsdep]
        self.d.cards[self.columns[kingspot][-1]].face = 1
        return True
      elif(len(self.hand) and self.d.cards[self.hand[-1]].rank == 13):
        self.columns[freespot].append(self.hand[-1])
        self.hand.pop()
        return True

    return False

  # try to move a stack to reveal a card
  def try2reveal(self):
    for i in range(len(self.columns)):
      if len(self.columns[i]):
        for j in range(len(self.columns[i])):
          if(self.d.cards[self.columns[i][j]].face):
            break
        for ii in range(len(self.columns)):
          if len(self.columns[ii]):
            r1 = self.d.cards[self.columns[ii][-1]].rank
            s1 = self.d.cards[self.columns[ii][-1]].suit
            r2 = self.d.cards[self.columns[i][j]].rank
            s2 = self.d.cards[self.columns[i][j]].suit
            if(r1 == r2 + 1 and ((s2+s1)%2 == 1)):
              for jj in range(j,len(self.columns[i])):
                self.columns[ii].append(self.columns[i][jj])
              self.columns[i] = self.columns[i][:j]
              if(len(self.columns[i])):
                self.d.cards[self.columns[i][-1]].face = 1
              return True
    return False

  def draw(self):
    # if deck is empty, make hand into deck
    if(len(self.deck) == 0):
      self.deck = self.hand[::-1]
      self.hand = []
    # draw three cards
    for i in range(5):
      if len(self.deck):
        self.hand.append(self.deck[-1])
        self.deck.pop()


  def taketurn(self):
    while(1):
      if(not self.try2score()):
        break
      else:
        print("scored!")

    while(1):
      if(not self.search4king()):
        break
      else:
        print("kinged!")
    while(1):
      if(not self.try2reveal()):
        break
      else:
        print("revealed!")

  def simulate(self):
    for t in range(10000):
      self.draw()
      self.taketurn()
    nfacedown = 0
    for c in self.d.cards:
      if c.face == 0:
        nfacedown += 1

    print("number of facedown cards:", nfacedown)
    print("number of cards in draw pile:", len(self.deck)+len(self.hand))

sim = board()
sim.simulate()



