import card_mod
import copy

def el_add(ls, el):
  assert type(ls) == list
  for i in range(len(ls)):
    ls[i] += el  
  return ls

class Hand:
  '''A Hand of Cards'''
  def __init__(self):
    '''constructs empty hand'''
    self.cards = []
    self.score = [0]

  def addCard(self, card):
    assert type(card) == card_mod.Card
    self.cards.append(card)
    if(card.score() == 'A'):
      scores_lista = copy.deepcopy(self.score)
      scores_listb = copy.deepcopy(self.score)
      self.score = el_add(scores_lista, 1) + el_add(scores_listb, 11)
    else:
      self.score = el_add(self.score, card.score()) 
    for i in self.score:
      if(i > 21):
        self.score.remove(i)

  def busted(self):
    if(not self.score):
      return True
    return False
  
  def print(self):
    print(self.handstr())

  def handstr(self):
    printstr = ''
    for card in self.cards:
      printstr += card.card + ' '
    return printstr
