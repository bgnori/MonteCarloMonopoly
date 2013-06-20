

#!/usr/bin/env python

import sys

from pypoly import montecarlo
from pypoly import Atlantic2008



stat = dict([(p, []) for p in Atlantic2008.myPlace if hasattr(p, 'facevalue')])




class Runner(montecarlo.Runner):
  def report(self, ex, nth):
    for player in ex.game.players:
      d = player.extract()
      for (c, t), prop in d.get('owns', ()):
        stat[prop].append((nth, c, t))
      #self.f.write("%d %d %d %d\n"%(p.turns, p.go_count, d['owns']))


trial = 10
with file('soldout_p4.txt', 'w') as f:
  r = Runner(trial, 4, f)
  r.run()
  for k, v in stat.iteritems():
    print >> f, k.name, 1.0*len(v) / trial
