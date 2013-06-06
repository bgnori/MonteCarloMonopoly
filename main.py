#!/usr/bin/env python

from landing import Board
from player import *




def experiment(n):
  b = Board()
  s = AlwaysOutStrategy()
  #s = AlwaysStayStrategy()
  ps = [Player(b, s, NAMES[i]) for i in range(n)]

  b.ready()
  while b.progress():
    yield sum([p.money for p in ps])


COUNT = 400

def kmean(n):
  total = [0 for i in range(COUNT)]
  for i in range(n):
    for i, s in enumerate(experiment(4)):
      if i >= COUNT:
        break
      total[i] += s
  return [1.0*t/n for t in total]

kmean(1)



