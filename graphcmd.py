#!/usr/bin/env python

import model
import command
import board
import Atlantic2008


class CallGraphMaker(object):
  def __init__(self):
    self.knowns = {}
    self.scanned = []

  def scan_module(self, m):
    self.scanned.append(m)
    for k, v in m.__dict__.iteritems():
      if isinstance(v, type) and issubclass(v, model.Command):
        self.knowns[k] = (v, set())

  def scan_object(self, xs):
    v, ys = self.knowns['LandOn']
    for x in xs:
      ys.add(x.command_class.__name__)
     
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

cgm.scan_module(model)
cgm.scan_module(command)
cgm.scan_module(board)
cgm.scan_module(Atlantic2008)
cgm.scan_object(Atlantic2008.myPlace.xs)

cgm.build()
cgm.report()

