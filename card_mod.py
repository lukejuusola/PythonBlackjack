class Card:
  valid_cards = ('2','3', '4', '5', '6', '7', '8', '9', '10', 'K', 'Q', 'J', 'A')
  valid_suites = ('D', 'S', 'C', 'H')
  def __init__(self, card, suite):
    '''Contructs Card object'''
    assert card in self.valid_cards
    assert suite in self.valid_suites
    self.card = card
    self.suite = suite
    self.scorenum = -1

  def score(self):
    '''Determines score of card'''
    if(self.scorenum != -1):
      return self.scorenum
    if(self.card in ('2','3','4','5','6','7','8','9','10')):
      self.scorenum = int(self.card)
    elif(self.card in ('K','Q','J')):
      self.scorenum = 10
    else: #card == 'A'
      self.scorenum = 'A'
    return self.scorenum


