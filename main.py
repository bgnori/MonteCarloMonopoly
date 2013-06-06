#!/usr/bin/env python

from landing import Board
from player import *




class Experiment:
  def __init__(self, count, *args):
    self.board = Board()
    self.count = count
    ps = [Player(self.board, arg, NAMES[i]) for i, arg in enumerate(args)]

    self.setUp()
  def setUp(self):
    pass

  def run(self):
    self.board.ready()
    for i in range(self.count):
      self.board.progress()
      self.hooks()

  def hooks(self):
    self.hook_moneycount()


class MoneyCount(Experiment):
  def setUp(self):
    self.log = []

  def hook_moneycount(self):
    self.log.append(sum([p.money for p in self.board.players]))

ao = AlwaysOutStrategy()
ex = MoneyCount(400, ao, ao, ao, ao)

ex.run()

print ex.log
