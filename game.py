#!/usr/bin/env python


import model
import command

import board
import card

# set of subclass and data
import Atlantic2008



class AlwaysOutStrategy(model.Strategy):
  def jail_action(self, player):
    assert isinstance(player, model.Player)
    player.send(player, command.PayAndOut())

class AlwaysStayStrategy(model.Strategy):
  def jail_action(self, player):
    pass


DEFAULT_NAMES = ["Alice", "Bob", "Charlie", "Deno", "Elen", "Ford", "George", "Hill"]

class Game(model.Executor, command.Chance, command.CommunityChest):
  def __init__(self, args):
    model.Executor.__init__(self)
    self.chance = card.Pile(*Atlantic2008.CHANCE_CARDS)
    self.chance.shuffle()
    self.chest = card.Pile(*Atlantic2008.COMMUNITY_CHEST_CARDS)
    self.chest.shuffle()
    self.board = board.Board(Atlantic2008.myPlace)
    self.players = []
    for i, arg in enumerate(args):
        self.add(model.Player(self, arg, DEFAULT_NAMES[i]))

  def add(self, p):
    self.players.append(p)

  def remove(self, p):
    i = self.players.index(p)
    self.players = self.players[:i] + self.players[i+1:]

  def nextplayer(self, prev=None):
    if prev is None:
      return self.players[0]
    n = len(self.players)
    i = self.players.index(prev)
    n = self.players[(i + 1) % n]
    assert isinstance(n, model.Player)
    return n

  def ready(self):
    p = self.players[0]
    self.send(p, command.StartTurn())

  def progress(self):
    if len(self.players) < 2:
      return False
    if not self.hasCommand():
      self.send(self.nextplayer(), command.StartTurn())
    if not isinstance(getattr(self.queue[0], "player", None), (model.Player,)):
        print self.queue[0]
        print dir(self.queue[0])
        assert False

    self.action()
    return True

  def move(self, p, n):
    print p, 'moving', n
    d, p.pos = divmod(p.pos + n, 40)
    if d == 1:
      self.send(p, command.GetFromBank(200))
    cmd = self.board.getCommand(p, p.pos, n)
    if cmd:
      self.send(p, cmd)

