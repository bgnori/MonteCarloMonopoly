#!/usr/bin/env python

from landing import Board
from player import *

def experiment(n):
  b = Board()
  s = AlwaysOutStrategy()
  #s = AlwaysStayStrategy()
  ps = [Player(b, s) for i in range(n)]

  i = 0
  while 1:
    for p in ps:
      p.turn()
    yield sum([p.money for p in ps])


def kmean(n):
  total = [0 for i in range(40)]
  for i in range(n):
    for i, s in enumerate(experiment(4)):
      if i >= 40:
        break
      total[i] += s
  return [1.0*t/n for t in total]

print kmean(100)








