#!/usr/bin/env python


class Command:
  def action(self, player):
    pass

class RollAndMove(Command):
  def __init__(self, count=None):
    if count is None:
      count = 0
    self.count = count

  def action(self, player):
    n, m = player.roll()
    cmd = player.move(n+m)
    if cmd:
      ''' go to jail''' #FIXME how about payment?
      return cmd

    if n == m:
      if self.count == 2:
        return GoToJail()
      else:
        return RollAndMove(self.count+1)
    return None

class StayInJail(Command):
  def action(self, player):
    n, m = player.roll()
    if n == m:
      cmd = player.move(n+m)
      return cmd
    else:
      player.jail_count += 1
      if player.jail_count > 2:
        player.money -= 50 #forced
        cmd = player.move(n+m)
        return cmd
      return None
    assert False

class GoToJail(Command):
  def action(self, player):
    player.pos = 10
    player.is_free = False
    player.jail_count = 0

class GetSallary(Command):
  def action(self, player):
    player.money += 200

class PayAndOut(Command):
  def action(self, player):
    player.money -= 50
    player.is_free = True


