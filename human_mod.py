import player_mod
import common

class Human(player_mod.Player):
  def doMove(self, hand):
    print('Hand to consider: ')
    hand.print()
    return input('Enter your move: ')
  def setup(self):
    self.name = 'Human'
  def makeBet(self):
    return input('Enter bet amount: ')
