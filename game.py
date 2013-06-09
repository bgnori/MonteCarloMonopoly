#!/usr/bin/env python


#modeling 
import command
import player

import board
import card

# set of subclass and data
import Atlantic2008

DEFAULT_NAMES = ["Alice", "Bob", "Charlie", "Deno", "Elen", "Ford", "George", "Hill"]


class Game(command.Executor, command.Chance, command.CommunityChest):
  def __init__(self, args):
    command.Executor.__init__(self)
    self.chance = card.Pile(*Atlantic2008.CHANCE_CARDS)
    self.chance.shuffle()
    self.chest = card.Pile(*Atlantic2008.COMMUNITY_CHEST_CARDS)
    self.chest.shuffle()
    self.board = board.Board(Atlantic2008.myPlace)
    self.players = []
    [player.Player(self, arg, DEFAULT_NAMES[i]) for i, arg in enumerate(args)]

  def add(self, player):
    self.players.append(player)

  def remove(self, player):
    i = self.players.index(player)
    self.players = self.players[:i] + self.players[i+1:]

  def nextplayer(self, player=None):
    if player is None:
      return self.players[0]
    n = len(self.players)
    i = self.players.index(player)
    return self.players[(i + 1) % n]

  def ready(self):
    p = self.players[0]
    self.send(p, command.StartTurn())

  def progress(self):
    if len(self.players) < 2:
      return False
    if not self.hasCommand():
      self.send(self.nextplayer(), command.StartTurn())
    self.action()
    return True

  def move(self, player, n):
    print player, 'moving', n
    d, player.pos = divmod(player.pos + n, 40)
    if d == 1:
      self.send(player, GetFromBank(200))
    cmd = self.board.getCommand(player, player.pos, n)
    if cmd:
      self.send(player, cmd)

