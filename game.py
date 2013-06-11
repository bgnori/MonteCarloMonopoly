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


class Game(model.Executor, command.Chance, command.CommunityChest):
  def __init__(self, *args):
    model.Executor.__init__(self, *args)
    self.chance = card.Pile(*Atlantic2008.CHANCE_CARDS)
    self.chance.shuffle()
    self.chest = card.Pile(*Atlantic2008.COMMUNITY_CHEST_CARDS)
    self.chest.shuffle()
    self.board = board.Board(Atlantic2008.myPlace)

  def ready(self):
    self.push(self.nextplayer(), model.GameLoop(commandclass=command.StartTurn))

  def progress(self):
    if len(self.players) < 2:
      return False
    self.action()
    return True

  def move(self, p, n):
    print p, 'moving', n
    d, p.pos = divmod(p.pos + n, 40)
    if d == 1:
      p.go_count += 1
      self.push(p, command.GetFromBank(200))
    cmd = self.board.getCommand(p, p.pos, n)
    if cmd:
      self.push(p, cmd)

