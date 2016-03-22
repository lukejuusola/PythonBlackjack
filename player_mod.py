import hand_mod

class Player:
  def __init__(self):
    '''Constructor for player object'''
    self.money = 0
    self.bet = 0
    self.hand = []
    self.hand.append(hand_mod.Hand())
    self.name = 'Player'
    self.setup()

  def bet(self, num):
    '''Constructor make bet'''
    self.bet = num
    self.money -= num

  def addCard(self, card):
    '''adds card to player's hand'''
    assert type(card) == card_mod.Card
    self.hand.add(card)

  def score(self, hand):
    assert type(hand) == hand_mod.Hand
    return hand.score()
  
  def discard(self):
    self.hand = []
    self.hand.append(hand_mod.Hand())

  def doubleBet(self):
    self.money -= self.bet
    self.bet *= 2
  
  def splitBet(self):
    self.money -= self.bet
  
  def setBankroll(self, val):
    self.money = val

  def makeBet(self):
    '''Makes whatever bet you deem necessary'''
  def doMove(self, hand):
    '''chooses move, based on hand and blackjack rules'''
  def setup(self):
    '''Does setup to keep track of whatever bot dependent variables you have'''
