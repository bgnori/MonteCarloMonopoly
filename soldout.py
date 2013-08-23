#!/usr/bin/env python

import sys

from pypoly import montecarlo
from pypoly import Atlantic2008



deeds = set([p for p in Atlantic2008.myPlace if hasattr(p, 'facevalue')])

Colors = {}
for p in deeds:
    v = Colors.get(p.colorgroups, None)
    if v is None:
        v = []
    v.append(p)
    Colors[p.colorgroups] = v


class Checker(object):
    def __init__(self):
        self.marks = dict.fromkeys(deeds, False)
        self.owners = dict(zip(deeds, deeds))

    def mark(self, prop, owner):
        self.marks[prop] = True
        self.owners[prop] = owner

    def colors(self):
        for c, xs in Colors.iteritems():
            yield c, all([self.marks[x] for x in xs])

    def monopoly(self):
        for c, xs in Colors.iteritems():
            yield c, [self.owners[x] for x in xs]


soldout_count = dict.fromkeys(Colors.keys(), 0)
monopoly_count = dict.fromkeys(Colors.keys(), 0)

class Runner(montecarlo.Runner):
  def report(self, ex, nth):
    checker = Checker()
    for player in ex.game.players:
      d = player.extract()
      for (c, t), prop in d.get('owns', ()):
        checker.mark(prop, player.target)

    for c, status in checker.colors():
        if status:
            soldout_count[c] += 1

    for c, xs in checker.monopoly():
        if len(set(xs)) == 1:
            monopoly_count[c] += 1
            #print >> self.f, xs


#trial = 100*1000


trial = 10 ** int(sys.argv[1])
pnum = int(sys.argv[2])
fname = 'soldout_p%d_t%d.txt'%(pnum, trial)
with file(fname, 'w') as f:
  r = Runner(trial, pnum, f)
  r.run()
  print >> f, 'trial:', trial
  print >> f, 'players:', pnum
  print >> f, soldout_count
  print >> f, monopoly_count

