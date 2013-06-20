#!/usr/bin/env python

import sys

from pypoly import montecarlo
from pypoly import Atlantic2008



deeds = dict([(p, False) for p in Atlantic2008.myPlace if hasattr(p, 'facevalue')])

Colors = {}
for p in deeds:
    v = Colors.get(p.colorgroups, None)
    if v is None:
        v = []
    v.append(p)
    Colors[p.colorgroups] = v


class Checker(object):
    def __init__(self):
        self.marks = dict(deeds)

    def mark(self, prop):
        self.marks[prop] = True

    def colors(self):
        for c, xs in Colors.iteritems():
            yield c, all([self.marks[x] for x in xs])

count = dict.fromkeys(Colors.keys(), 0)

class Runner(montecarlo.Runner):
  def report(self, ex, nth):
    checker = Checker()
    for player in ex.game.players:
      d = player.extract()
      for (c, t), prop in d.get('owns', ()):
        checker.mark(prop)
    for c, status in checker.colors():
        if status:
            count[c] += 1


trial = 100*1000
with file('soldout_p4.txt', 'w') as f:
  r = Runner(trial, 4, f)
  r.run()
  print >> f, count

