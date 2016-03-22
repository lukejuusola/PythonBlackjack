import player_mod

class Dealer(player_mod.Player):
  '''Player bot playing standard house dealer rules. Hits on soft 17
     Will only have one hand and will always have one hand'''
  def doMove(self, hand):
    print('Dealer hand: %s' % hand.handstr())
    soft = 'hard'
    hand = self.hand[0]
    handscores = hand.score
    score = max(handscores)
    for card in self.hand[0].cards:
      if card.card == 'A':
        soft = 'soft'
    if(score < 17):
      print('Dealer hits on:%s %s' % (soft, score))
      return 'hit'
    if(score > 17 or (score == 17 and soft == 'hard')):
      print('Dealer stays on:%s %s' % (soft, score))
      return 'stay'
    if(score == 17 and soft == 'soft'):
      print('Dealer hits on:%s %s' % (soft, score))
      return 'hit'

  def setup(self):
    self.name = 'Dealer'
    self.money = float('inf')

  def hiddenstr(self):
    return '* ' + self.hand[0].cards[0].card
