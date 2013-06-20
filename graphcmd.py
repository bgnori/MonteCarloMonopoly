#!/usr/bin/env python

from pypoly import models
from pypoly import commands
from pypoly import board
from pypoly import Atlantic2008


class CallGraphMaker(object):
  def __init__(self):
    self.knowns = {}
    self.scanned = []

  def scan_module(self, m):
    self.scanned.append(m)
    for k, v in m.__dict__.iteritems():
      if isinstance(v, type) and issubclass(v, models.Command):
        self.knowns[k] = (v, set())

  def scan_place(self, xs):
    v, ys = self.knowns['LandOn']
    for x in xs:
      ys.add(x.command_class.__name__)

  def scan_card(self, name, xs):
    v, ys = self.knowns[name]
    for x in xs:
      for k in x.fn.func_code.co_names:
        if k in self.knowns:
          ys.add(k)

     
  def build(self):
    for m in self.scanned:
      for k, (v, xs) in self.knowns.iteritems():
        for name in v.__call__.__func__.func_code.co_names:
          if name in self.knowns:
            xs.add(name)

  def report(self):
    print "digraph evoke {"
    for k, (v, xs) in self.knowns.iteritems():
      for x in xs:
        print k, '->', x
    print "}"


cgm = CallGraphMaker()

cgm.scan_module(models)
cgm.scan_module(commands)
cgm.scan_module(board)
cgm.scan_module(Atlantic2008)
cgm.scan_place(Atlantic2008.myPlace.xs)
cgm.scan_card('DrawChance', Atlantic2008.CHANCE_CARDS)
cgm.scan_card('DrawCommunityChest', Atlantic2008.COMMUNITY_CHEST_CARDS)

cgm.build()
cgm.report()

