#!/usr/bin/env python
from command import *
from random import randint
from landing import PLACES


NAMES = ["Alice", "Bob", "Charlie", "Deno", "Elen", "Ford", "George", "Hill"]

def dice():
  return randint(1, 6), randint(1, 6)


class Player:
  def __init__(self, board, strategy, name, pos=None):
    if pos is None:
      pos = 0
    self.pos = pos
    self.board = board
    board.add(self)
    self.money = 1500
    self.is_free = True
    self.jail_count = 0
    self.strategy = strategy
    self.owns = []
    self.name = name

  def push(self, cmd):
    self.board.send(self, cmd)

  def roll(self):
    return dice()

  def __str__(self):
    return "<Player %s %d %s>"%(self.name, self.money, PLACES[self.pos].name)

  def move(self, n):
    d, self.pos = divmod(self.pos + n, 40)
    if d == 1:
      self.push(GetSallary())
    cmd = self.board.getCommand(self, self.pos, n)
    if cmd:
      self.push(cmd)

  def zapCommand(self):
    self.board.zapCommand()

  def add_property(self, property):
    self.owns.append(property)
    self.board.ownerof[property.pos] = self


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


