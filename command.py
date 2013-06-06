#!/usr/bin/env python


class Command:
  def action(self, player):
    pass
  def __str__(self):
    return "<Command %s>"%(self.__class__.__name__,)

class StartTurn(Command):
  def action(self, player):
    if not player.is_free:
      player.strategy.jail_action(player)
    player.push(AfterJailDecision())

class AfterJailDecision(Command):
  def action(self, player):
    if player.is_free:
      player.push(RollAndMove())
    else:
      player.push(StayInJail())

class RollAndMove(Command):
  def __init__(self, count=None):
    if count is None:
      count = 0
    self.count = count

  def action(self, player):
    n, m = player.roll()
    if n == m:
      if self.count == 2:
        player.push(GoToJail())
      else:
        player.move(n+m)
        player.push(RollAndMove(self.count+1))
    else:
      player.move(n+m)

class StayInJail(Command):
  def action(self, player):
    n, m = player.roll()
    if n == m:
      player.move(n+m)
    else:
      player.jail_count += 1
      if player.jail_count > 2:
        player.money -= 50 #forced
        player.move(n+m)

class GoToJail(Command):
  def action(self, player):
    player.pos = 10
    player.is_free = False
    player.jail_count = 0
    player.zapCommand()

class GetSallary(Command):
  def action(self, player):
    player.money += 200


class PayTax(Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, player):
    player.money -= self.amount

class PayAndOut(Command):
  def action(self, player):
    player.money -= 50
    player.is_free = True


class PayRent(Command):
  def __init__(self, src, dst):
    pass
  def action(self, player):
    player.money -= 50
    player.is_free = True


class DrainMoney(Command):
  def __init__(self, amount, src, dst):
    self.amount = amount
    self.src = src
    self.dst = dst

  def action(self, player):
    pass

class TapMoney(Command):
  def action(self, player):
    pass


