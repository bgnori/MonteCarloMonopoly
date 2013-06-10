#!/usr/bin/env python


import game

class Experiment:
  def __init__(self, count, *args):
    self.game = game.Game(args)
    self.count = count

  def report(self):
    for p in self.game.players:
      print '='*20
      print p.name, "has", p.asset()
      for i, prop in enumerate(p.owns):
        print i, prop
      print


  def run(self):
    self.game.ready()
    for i in xrange(self.count):
      self.game.progress()


ao = game.AlwaysOutStrategy()
ex = Experiment(1000, ao, ao, ao, ao)

ex.run()

ex.report()

