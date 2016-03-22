import card_mod
import copy
import random

class Deck:
  def __init__(self, decksInShoe):
    standardDeck = []
    for cardT in ['2', '3','4','5','6','7','8','9','10','J','Q','K','A']:
      for suiteT in ['H', 'S', 'D', 'C']:
        standardDeck.append(card_mod.Card(cardT, suiteT))
    self.cards = []
    for i in range(decksInShoe):
      self.cards += copy.deepcopy(standardDeck)
    self.discarded = []

    self.shuffle()
 

  def drawCard(self, quiet = False):
    if(len(self.cards) <= 0):
      self.shuffle()
    card = self.cards[0]
    self.cards.remove(card)
    self.discarded.append(card)
    if(not quiet):
      print('Drawn Card: %s' % card.card)
    return card

  def shuffle(self):
    self.cards += self.discarded
    random.shuffle(self.cards)
