#!/usr/bin/env python

from pypoly import models
from pypoly import commands
from pypoly import board

from pypoly import Atlantic2008

import sys

class AlwaysOutStrategy(models.Strategy):
  def jail_action(self, game, player):
    assert isinstance(player, (models.Player, models.StatWrapper))
    if player.cards:
      card = player.cards.pop()
      game.push(commands.FreeByCard(player=player, card=card))
    elif player.money > 50:
      game.push(commands.PayAndOut(player=player))
      return
    else:
      pass
    ''' no money to get out '''


class AlwaysStayStrategy(models.Strategy):
  def jail_action(self, game, player):
    pass



ao = AlwaysOutStrategy()

def track_turns(wrapper, old, new, data):
  if data is None:
    data = []
  data.append((wrapper.stamp(), new))
  return data

def track_pos(wrapper, old, new, data):
  if data is None:
    data = []
  data.append((wrapper.stamp(), (old, new)))
  return data

def track_jail(wrapper, old, new, data):
  if data is None:
    data = []
  if old and not new:
    data.append(wrapper.stamp())
  return  data


def track_money(wrapper, old, new, data):
  if data is None:
    data = ([], [])
  chg = new - old 
  if chg > 0:
    data[0].append((wrapper.stamp(), chg))
  if chg < 0:
    data[1].append((wrapper.stamp(), -chg))
  return data

def track_owns(wrapper, method):
  def foo(*args, **kw):
    print 'track_owns', method
    print args, kw
    d = wrapper.__dict__['values']
    v = d.get('owns', None)
    if v is None:
      v = []
    v.append((wrapper.stamp(), args[0]))
    d['owns'] = v
    return method(*args, **kw)
  return foo


peekers = {
    #"turns":track_turns,
    "pos": track_pos,
    "is_free" : track_jail,
    "money" : track_money,
}


class Experiment(object):
  def __init__(self, count, *players):
    self.game = models.Game(
        start_command=commands.StartTurn,
        board=board.Board(Atlantic2008.myPlace),
        chance=Atlantic2008.CHANCE_CARDS,
        chest=Atlantic2008.COMMUNITY_CHEST_CARDS,
        players=players)
    self.count = count
    assert Atlantic2008.myPlace[30].name == 'Go to Jail'

  def report(self):
    for p in self.game.players:
      print '='*20
      print p.name
      print "played", p.turns
      print "passed go", p.go_count, 'time(s)'
      print 'by tracker'
      d = p.extract()
      print d
      print 'get jailed', len(d.get('is_free', []))
      print d.get('is_free', None)
      plus = sum(map(lambda x: x[0][1], d['money']))
      minus = sum(map(lambda x: x[1][1], d['money']))
      print "P/L:", plus, minus, plus - minus
      print 'cash:', p.money
      print 'asset', p.asset()
      print "has ", sum([o.facevalue for o in p.owns]),
      print " as property"
      for i, prop in enumerate(p.owns):
        x = d.get('owns', None)
        if x is not None:
          for found in x:
            if found[1] == prop:
              break
          print i, prop, found[0]
        else:
          print i, prop, '???'
      for c in p.cards:
        print c.instruction
      print

  def run(self):
    self.game.ready()
    #self.game.players[2].dead = True
    for i in xrange(self.count):
      self.game.progress()


class Runner(object):
  def __init__(self, n, f):
    self.n = n
    self.done = 0
    self.bar_drawn = 0
    self.bar = 40
    self.f = f

  def run(self):
    sys.stderr.write('>')
    for i in range(self.n):
      self.one()
      self.draw()
    sys.stderr.write('!')

  def one(self):
    
    ex = Experiment(1000, 
            *[models.StatWrapper(models.Player(ao, models.DEFAULT_NAMES[i], pos=0),
                on_method={'add_property':track_owns},
                on_setter=peekers) for i in range(4)])
    ex.run()
    for p in ex.game.players:
      d = p.extract()
      self.f.write("%d %d %d %d\n"%(p.turns, p.go_count, d['is_free']))
    self.done += 1

  def draw(self):
    if (self.bar * self.done / self.n) > self.bar_drawn:
      self.bar_drawn += 1
      sys.stderr.write('\b')
      sys.stderr.write('=')
      sys.stderr.write('>')
      sys.stderr.flush()

if __name__ == '__main__':
  import sys
  ex = Experiment(1000, 
    *[models.StatWrapper(models.Player(ao, models.DEFAULT_NAMES[i], pos=0),
        on_method={'add_property':track_owns},
        on_setter=peekers) 
        for i in range(4)])
  ex.run()
  ex.report()
  #for p in ex.game.players:
  #  print p.extract()




