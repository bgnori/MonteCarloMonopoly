#!/usr/bin/env python


import game

class Experiment:
  def __init__(self, count, *args):
    self.game = game.Game(*args)
    self.count = count

  def report(self):
    for p in self.game.players:
      print '='*20
      print p.name
      print "played", p.turns
      print "passed go", p.go_count, 'time(s)'
      plus = sum(p.profit)
      minus = sum(p.loss)
      print "P/L:", plus, minus, plus - minus
      print 'cash:', p.money
      print 'asset', p.asset()
      print "has ", sum([o.facevalue for o in p.owns]),
      print " as property"
      for i, prop in enumerate(p.owns):
        print i, prop
      print


  def run(self):
    self.game.ready()
    #self.game.players[2].dead = True
    for i in xrange(self.count):
      self.game.progress()


ao = game.AlwaysOutStrategy()
ex = Experiment(800, ao, ao, ao, ao)

ex.run()

ex.report()

