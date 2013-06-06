#!/usr/bin/env python
from command import *
from random import randint

def dice():
  return randint(1, 6), randint(1, 6)


class Player:
  def __init__(self, board, strategy, pos=None):
    if pos is None:
      pos = 0
    self.pos = pos
    self.board = board
    self.queue = []
    self.money = 1500
    self.is_free = True
    self.jail_count = 0
    self.strategy = strategy
    self.owns = []

  def push(self, cmd):
    self.queue.append(cmd)

  def roll(self):
    return dice()

  def move(self, n):
    d, self.pos = divmod(self.pos + n, 40)
    if d == 1:
      self.push(GetSallary())
    return self.board.getCommand(self.pos)

  def pop(self):
    return self.queue.pop(0)

  def hasCommand(self):
    return bool(self.queue)


  def preCommand(self):
    pass

  def postCommand(self):
    pass

  def turn(self):
    if not self.is_free:
      self.strategy.jail_action(self)

    if self.is_free:
      self.push(RollAndMove())
    else:
      self.push(StayInJail())

    while self.hasCommand():
      self.preCommand()
      cmd = self.pop()
      cmd = cmd.action(self)
      self.postCommand()
      if cmd:
        self.push(cmd)

class Strategy:
  '''not yet'''
  def jail_action(self, player):
    raise


class AlwaysOutStrategy(Strategy):
  def jail_action(self, player):
    player.push(PayAndOut())

class AlwaysStayStrategy(Strategy):
  def jail_action(self, player):
    pass



