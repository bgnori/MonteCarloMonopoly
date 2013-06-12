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


class Game(model.Executor):
  def __init__(self, *args):
    model.Executor.__init__(self, *args)
    self.chance = card.Pile(*Atlantic2008.CHANCE_CARDS)
    self.chance.shuffle()
    self.chest = card.Pile(*Atlantic2008.COMMUNITY_CHEST_CARDS)
    self.chest.shuffle()
    self.board = board.Board(Atlantic2008.myPlace)

  def ready(self):
    self.push(self.nextplayer(), model.GameLoop(start=command.StartTurn))

  def progress(self):
    if len(self.players) < 2:
      return False
    self.action()
    return True

