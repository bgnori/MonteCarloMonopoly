#!/usr/bin/env python


import game

class Experiment:
  def __init__(self, count, *args):
    self.game = game.Game(args)
    self.count = count


  def run(self):
    self.game.ready()
    for i in range(self.count):
      self.game.progress()


ao = game.AlwaysOutStrategy()
ex = Experiment(400, ao, ao, ao, ao)

ex.run()

print ex.log

