import hand_mod
import card_mod
import deck_mod
import human_mod
import dealer_mod
import copy
import common

class Game:
  startingBank = 100000

  def __init__(self, numplayers, decksInShoe):
    '''initializes game with dealer and numplayers of human players'''
    self.players = []
    for i in range(numplayers):
      human = human_mod.Human()
      self.players.append(human)
    self.dealer = dealer_mod.Dealer()
    self.players.append(self.dealer)
    self.playersInRound = []
    self.playersBusted = []
    self.deck = deck_mod.Deck(decksInShoe)

  
  def setBankroll(self, val):
    for player in self.players:
      if(player != self.dealer):
        player.setBankroll(val)

  def takeBets(self):
    for player in self.players:
      bet = 0
      if(type(player) == human_mod.Human):
        bet = player.makeBet()
        while(not common.isInt(bet) or 0 > int(bet) or int(bet) > player.money):
          print('Invalid Bet of %s by %s' % (bet, player.name))
          bet = player.makeBet()
        bet = int(bet)
      elif(player != self.dealer):
        bet = player.makeBet()
        if(not common.isInt(bet) or 0 > int(bet) or int(bet) > player.money):
          print('Invalid Bet of %s by %s' % (bet, player.name))
          player.bet = 0
          continue
      player.bet = bet
      player.money -= player.bet
        
  def startRound(self):
    for player in self.players:
      player.discard()
    self.playersBusted = []
    self.playersInRound = []
    self.takeBets()
    for player in self.players:
      if(player.bet != 0):
        self.playersInRound.append((player, player.hand[0]))
    self.playersInRound.append((self.dealer, self.dealer.hand[0]))

  def endRound(self):
    for player, hand in self.players:
      player.discard()

  def deal(self):
    self.deck.drawCard(True)
    self.deck.drawCard(True)
    for player, hand in self.playersInRound:
      if(type(player) != dealer_mod.Dealer):
        hand.addCard(self.deck.drawCard())
        hand.addCard(self.deck.drawCard())
      else:
        hand.addCard(self.deck.drawCard())
        hand.addCard(self.deck.drawCard(True))
  
  def printBank(self):
    for player in self.players:
      print('%s\'s bankroll: %s' % (player.name, player.money))

  def isLegal(self, move, hand, player):
    if(move == 'quit'):
      return True
    if(hand.busted()):
      print("Busted: Illegal Move")
      print(hand.score)
      return False
    if(move == 'hit'):
      return True
    elif(move == 'stay'):
      return True
    elif(move == 'double down'):
      if(len(hand.cards) == 2):
        return True
    elif(move == 'split'):
      if(len(hand.cards) == 2 and hand.cards[0].card == hand.cards[1].card):
        return True
    elif(move == 'help'):
      return True
    else:
      return False

  def play(self):
    self.setBankroll(self.startingBank) 
    quitFlag = False 
    while(quitFlag == False): # Start game loop
      print("------Starting round-------")
      self.printBank()
      self.startRound()
      self.deal()
      print('Dealer\'s Hand: %s' % self.dealer.hiddenstr())
      while(self.playersInRound and not quitFlag): # Rotate through players 
        player, hand = self.playersInRound[0]
        hand_num = 0
        while(hand_num < len(player.hand) and not quitFlag): # Rotate through hands
          hand = player.hand[hand_num]
          move = player.doMove(hand)
          move = move.strip().lower()
          while(not quitFlag and not self.isLegal(move, hand, player)): # Get legal move
            if(type(player) == human_mod.Human):
              print("Illegal Move. Try Again")
            else:
              print("Illegal Move. Removing bot from round")
              self.playersInRound.remove(player)
              break
            move = player.doMove(hand)
            move = move.strip().lower()
          # We have a legal move -- play it
          if(move == 'hit'):
            card = self.deck.drawCard()
            hand.addCard(card)
            if(hand.busted()):
              print("%s: Hand Busted" % player.name)
              self.playersInRound.remove((player, hand))
              self.playersBusted.append((player, hand))
              hand_num += 1
          elif(move == 'stay'):
            self.playersInRound.remove((player, hand))
            hand_num += 1
          elif(move == 'split'):
            player.splitBet()

            hand1 = hand_mod.Hand()
            hand1.addCard(hand.cards[0])
            card = self.deck.drawCard()
            hand1.addCard(card)
            
            hand2 = hand_mod.Hand()
            hand2.addCard(hand.cards[1])
            card = self.deck.drawCard()
            hand2.addCard(card)
            
            self.playersInRound.remove((player, hand))
            self.playersInRound.append((player, hand1))
            self.playersInRound.append((player, hand2))
            player.hand.remove(hand) 
            player.hand += [hand1, hand2]
            hand = player.hand[hand_num]

          elif(move == 'double down'):
            player.doubleBet()
            card = self.deck.drawCard()
            hand.addCard(card)
            self.playersInRound.remove((player, hand))
            if(hand.busted()):
              print('%s: hand busted' % player.name)
              self.playersBusted.append((player, hand))
            hand_num += 1
          elif(move == 'help'):
            print('cmds: ["hit", "stay", "split", "double down", "quit", "help"]')
          elif(move == 'quit'):
            quitFlag = True
            break

      # Update Winnings
      if((self.dealer, self.dealer.hand[0]) not in self.playersBusted):
        dealerhand = self.dealer.hand[0]
        dealerscore = max(dealerhand.score)
        for player in self.players:
          for hand in player.hand:
            if(not hand.score):
              continue
            if(type(player) != dealer_mod.Dealer):
              playerscore = max(hand.score)
              if(playerscore > dealerscore):
                print('%s \'s %s beat the dealer' % (player.name, hand.handstr()))
                player.money += 2*player.bet
              elif(playerscore < dealerscore):
                print('%s \'s %s lost to the dealer' % (player.name, hand.handstr()))
              else:
                print('%s \'s %s pushed with the dealer' % (player.name, hand.handstr()))
                player.money += player.bet
      else:
        for player in self.players:
          for hand in player.hand:
            if(not hand.score):
              continue
            if(type(player) != dealer_mod.Dealer):
             # for hand in player.hand: 
                print('%s \'s %s beat the dealer' % (player.name, hand.handstr()))
                player.money += 2*player.bet
      #Anyone still have money?
      for player in self.players:
        if player.money <= 0:
          self.players.remove(player)
      if(len(self.players) < 2):
        quit()


def main():
  num_players = 1
  num_decks = 1

  game = Game(num_players, num_decks)
  game.play()

main()
