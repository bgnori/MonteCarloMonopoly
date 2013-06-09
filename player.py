#!/usr/bin/env python
from command import *
from random import randint



def dice():
  return randint(1, 6), randint(1, 6)


class Player:
  def __init__(self, game, strategy, name, pos=None):
    if pos is None:
      pos = 0
    self.pos = pos
    self.game = game 
    game.add(self)
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

class AlwaysOutStrategy(Strategy):
  def jail_action(self, player):
    player.send(self, PayAndOut())

class AlwaysStayStrategy(Strategy):
  def jail_action(self, player):
    pass


