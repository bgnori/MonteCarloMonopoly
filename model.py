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



DEFAULT_NAMES = ["Alice", "Bob", "Charlie", "Deno", "Elen", "Ford", "George", "Hill"]


class Executor:
  def __init__(self, *args):
    self.stack= []
    self.players = []
    for i, arg in enumerate(args):
        self.add(Player(self, arg, DEFAULT_NAMES[i]))

  def push(self, p, cmd):
    assert not hasattr(cmd, 'player')
    cmd.player = p #FIXME support for old style
    self.stack.append(cmd)

  def pop(self):
    return self.stack.pop(-1)

  def peek(self):
    return self.stack[-1]

  def zapCommandUpTo(self, klass):
    while not isinstance(self.peek(), klass):
      self.pop()

  def hasCommand(self):
    return bool(self.stack)

  def action(self):
    c = self.pop()
    print c
    name = "handle_" + c.__class__.__name__
    h = getattr(self, name, None)
    if h:
      h(c)
    else:
      #FIXME support for old style
      c.action(self, c.player)

    """WrapUpTurn().action(self, p)"""

  def add(self, p):
    self.players.append(p)

  def nextplayer(self, prev=None):
    if prev is None:
      i = 0
    else:
      i = self.players.index(prev)
    return self.players[(i + 1) % len(self.players)]

  def handle_NullCommand(self, cmd):
    print 'method handle_NullCommand'


class EndTurn(Command):
  def action(self, executor, player):
    executor.zapCommandUpTo(GameLoop)

class GameLoop(Command):
  def action(self, executor, player):
    assert not executor.hasCommand()
    executor.push(executor.nextplayer(player), GameLoop(start=self.start)) #loop
    executor.push(player, self.start())



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
    self.dead = False
    self.turns = 0
    self.go_count = 0

  def asset(self):
    total = 0
    for prop in self.owns:
      total += prop.facevalue
    return total + self.money

  def is_dying(self):
    pass


  def send(self, p, cmd):
    assert not hasattr(cmd, 'player')
    assert isinstance(p, Player)
    assert isinstance(cmd, Command)
    self.game.push(p, cmd)

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


