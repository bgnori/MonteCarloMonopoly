#!/usr/bin/env python


class Command:
  def action(self, player):
    raise
  def __str__(self):
    return "<Command %s>"%(self.__class__.__name__,)


class NullCommand(Command):
  def action(self, player):
    pass

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

class WrapUpTurn(Command):
  def action(self, player):
    pass

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
        player.money -= 50 #forced, but there is an option for Jail Free Card
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

class PayToBank(Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, player):
    player.money -= self.amount

class PayAndOut(Command):
  def action(self, player):
    player.money -= 50
    player.is_free = True

class PayRent(Command):
  def __init__(self, owner, amount):
    self.owner = owner
    self.amount = amount
  def action(self, player):
    player.money -= self.amount
    self.owner.money += self.amount
    print player.name, '==(', self.amount, ')=>', self.owner.name

class BuyProperty(Command):
  def __init__(self, property):
    self.property = property

  def action(self, player):
    player.money -= self.property.facevalue
    player.add_property(self.property)


