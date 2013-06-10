#!/usr/bin/env python

from random import randint



def dice():
  return randint(1, 6), randint(1, 6)

class Command:
  def __init__(self, **kwargs):
    
    for k, v in kwargs.iteritems():
      self.__dict__[k] = v

  def action(self, executor, player):
    raise

  def __str__(self):
    return "<Command %s>"%(self.__class__.__name__,)

class NullCommand(Command):
  pass


class Executor:
  def __init__(self):
    self.queue = []

  def send(self, p, cmd):
    assert not hasattr(cmd, 'player')
    cmd.player = p #FIXME support for old style
    self.queue.append(cmd)

  def zapCommand(self):
    self.queue = []

  def hasCommand(self):
    return bool(self.queue)

  def action(self):
    c = self.queue.pop(0)
    print c
    name = "handle_" + c.__class__.__name__
    h = getattr(self, name, None)
    if h:
      h(c)
    else:
      #FIXME support for old style
      c.action(self, c.player)

    """WrapUpTurn().action(self, p)"""
  def handle_NullCommand(self, cmd):
    pass



class Player:
  def __init__(self, game, strategy, name, pos=None):
    if pos is None:
      pos = 0
    self.pos = pos
    self.game = game 
    self.money = 1500
    self.is_free = True
    self.jail_count = 0
    self.strategy = strategy
    self.owns = []
    self.houses = {}
    self.hotels = {}
    self.name = name

  def asset(self):
    total = 0
    for prop in self.owns:
      total += prop.facevalue
    return total

  def send(self, p, cmd):
    assert not hasattr(cmd, 'player')
    assert isinstance(p, Player)
    assert isinstance(cmd, Command)
    self.game.send(p, cmd)

  def roll(self):
    return dice()

  def __str__(self):
    return "<Player %s %d %s>"%(self.name, self.money, self.game.board[self.pos].name)

  def zapCommand(self):
    self.game.zapCommand()

  def add_property(self, property):
    self.owns.append(property)
    self.game.board.ownerof[property.pos] = self #FIXME


class Strategy:
  '''not yet'''
  def jail_action(self, player):
    raise


