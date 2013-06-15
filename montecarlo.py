#!/usr/bin/env python

import model
import command
import board

import Atlantic2008

class AlwaysOutStrategy(model.Strategy):
  def jail_action(self, game, player):
    assert isinstance(player, model.Player)
    if player.cards:
      card = player.cards.pop()
      game.push(command.FreeByCard(player=player, card=card))
    elif player.money > 50:
      game.push(command.PayAndOut(player=player))
      return
    else:
      pass
    ''' no money to get out '''


class AlwaysStayStrategy(model.Strategy):
  def jail_action(self, game, player):
    pass



class Experiment:
  def __init__(self, count, strategies):
    self.game = model.Game(
        start_command=command.StartTurn,
        board=board.Board(Atlantic2008.myPlace),
        chance=Atlantic2008.CHANCE_CARDS,
        chest=Atlantic2008.COMMUNITY_CHEST_CARDS,
        strategies=strategies)
    self.count = count
    assert Atlantic2008.myPlace[30].name == 'Go to Jail'

  def report(self):
    for p in self.game.players:
      print '='*20
      print p.name
      print "played", p.turns
      print "passed go", p.go_count, 'time(s)'
      print 'get jailed', p.jailed_count
      plus = sum(p.profit)
      minus = sum(p.loss)
      print "P/L:", plus, minus, plus - minus
      print 'cash:', p.money
      print 'asset', p.asset()
      print "has ", sum([o.facevalue for o in p.owns]),
      print " as property"
      for i, prop in enumerate(p.owns):
        print i, prop
      for c in p.cards:
        print c.instruction
      print


  def run(self):
    self.game.ready()
    #self.game.players[2].dead = True
    for i in xrange(self.count):
      self.game.progress()


ao = AlwaysOutStrategy()
ex = Experiment(8000, [ao, ao, ao, ao])

ex.run()

ex.report()

