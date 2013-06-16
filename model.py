#!/usr/bin/env python

from random import randint
from random import shuffle


DEFAULT_NAMES = ["Alice", "Bob", "Charlie", "Deno", "Elen", "Ford", "George", "Hill"]

def dice():
  return randint(1, 6), randint(1, 6)


class StatWrapper(object):
  def __init__(self, target, **args):
    d = self.__dict__
    d['target'] = target
    d['procs'] = dict(**args)
    d['values'] = dict()

  def __getattr__(self, k):
    return getattr(self.__dict__['target'], k)

  def __setattr__(self, k, new):
    proc = self.__dict__['procs'].get(k, None)
    old = getattr(self.__dict__['target'], k)
    data = self.__dict__['values'].get(k, None)
    if proc is not None:
      self.__dict__['values'][k] = proc(self, old, new, data)
    setattr(self.__dict__['target'], k, new)

  def extract(self):
    return self.__dict__['values']
  
  def __str__(self):
    return str(self.target)


class Command(object):
  defaults = {}
  def __new__(klass, **kwargs): #def __init__(self, **kwargs):
    self = super(Command, klass).__new__(klass)
    self.param = dict(**klass.defaults)
    for k, v in kwargs.iteritems():
      self.param[k] = v
    return self

  def __getattr__(self, k):
    try:
      return self.__dict__["param"][k]
    except:
      raise AttributeError('no such atribute %s'%(k,))

  def __call__(self, game):
    ''' 
      param == self.param,  for shorthand
    '''
    raise

  def __str__(self):
    return "<Command %s %s>"%(self.__class__.__name__, self.param)


class NullCommand(Command):
  def __call__(self, game):
    pass


class Card(object):
  def __init__(self, fn, instruction, art):
    self.instruction = instruction
    self.art = art
    self.fn = fn # player => Command proc


class ChanceCard(Card):pass
class CommunityChestCard(Card):pass

class Pile(object):
  def __init__(self, t, *cards):
    self.t = t
    self.cards = cards
    self.pile = list(self.cards)

  def shuffle(self):
    shuffle(self.pile)

  def draw(self):
    return self.pile.pop(0)

  def putBack(self, card):
    assert isinstance(card, self.t)
    self.pile.append(card)


class Game(object):
  def __init__(self, start_command, board, chance, chest, players):
    self.stack= []
    self.players = players
    for p in self.players:
      p.bind(self)
    self.chance = Pile(ChanceCard, *chance)
    self.chance.shuffle()
    self.chest = Pile(CommunityChestCard, *chest)
    self.chest.shuffle()
    self.board = board

    self.start_command = start_command

  def ready(self):
    self.push(GameLoop(start_command=self.start_command, player=self.nextplayer()))

  def progress(self):
    if len(self.players) < 2:
      return False
    c = self.pop()
    print c, getattr(c, 'player', 'N/A')
    c(self)

  def push(self, cmd):
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

  def nextplayer(self, prev=None):
    if prev is None:
      i = -1
    else:
      i = self.players.index(prev)
    return self.players[(i + 1) % len(self.players)]

  def drawChance(self):
    return self.chance.draw()
    
  def putBackChance(self, card):
    self.chance.putBack(card)

  def drawCommunityChest(self):
    return self.chest.draw()

  def putBackCommunityChest(self, card):
    self.chest.putBack(card)


class EndTurn(Command):
  def __call__(self, game):
    game.zapCommandUpTo(GameLoop)


class GameLoop(Command):
  def __call__(self, game):
    assert not game.hasCommand()
    game.push(GameLoop(start_command=self.start_command, player=game.nextplayer(self.player))) #loop
    game.push(self.start_command(player=self.player))


class Player(object):
  def __init__(self, strategy, name, pos=None):
    if pos is None:
      pos = 0
    self.pos = pos
    self.game = None
    self.money = 1500
    self.is_free = True
    self.jail_count = 0
    self.strategy = strategy
    self.owns = set([])
    self.houses = {}
    self.hotels = {}
    self.cards = set()
    self.name = name
    self.dead = False

    ''' these must be highly useful for strategy impl.'''
    self.turns = 0 
    self.go_count = 0 

  def bind(self, game):
    self.game = game


  def asset(self):
    total = 0
    for prop in self.owns:
      total += prop.facevalue
    return total + self.money

  def estimateLiqudate(self):
    total = 0
    for prop in self.owns:
      if prop.is_morgaged:
        continue
      total += (prop.facevalue/2 + prop.buildings * prop.cost/2)
    return total + self.money

  def is_dying(self):
    pass

  def send(self, p, cmd):
    raise

  def roll(self):
    return dice()

  def __str__(self):
    return "<Player %s %d %s>"%(self.name, self.money, self.game.board[self.pos].name)

  def zapCommand(self):
    self.game.zapCommand()

  def add_property(self, prop):
    self.owns.add(prop)

  def remove(self, prop):
    self.owns.remove(prop)


class Place(object):
  def __init__(self, name, commadclass, pos, **kw):
    self.name = name
    self.pos = pos
    self.buildings = 0
    self.command_class = commadclass
    for k, v in kw.iteritems():
      assert k not in ('name', 'pos', 'command_class', 'buildings')
      setattr(self, k, v)
  def __str__(self):
    return "<" + self.name + ">"
 
  def calcFix(self, house, hotel):
    if self.buildings == 0:
      return 0
    elif 0 < self.buildings and self.buildings < 5:
      return self.buildings * house
    elif self.buildings == 5:
      return hotel
    else:
      assert False


class Strategy(object):
  '''not yet'''
  def jail_action(self, game, player):
    raise


