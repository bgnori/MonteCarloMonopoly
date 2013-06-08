#!/usr/bin/env python


class Command:
  def action(self, executor, player):
    raise
  def __str__(self):
    return "<Command %s>"%(self.__class__.__name__,)


class Executor:
  def __init__(self):
    self.queue = []

  def send(self, player, cmd):
    self.queue.append((player, cmd))

  def zapCommand(self):
    self.queue = []

  def action(self):
    p, c = self.queue.pop(0)
    c.action(self, p)
    if not self.queue:
      WrapUpTurn().action(self, p)


class NullCommand(Command):
  def action(self, executor, player):
    pass


class AdvanceTo(Command):
  def __init__(self, dst):
    self.dst = dst 

  def action(self, executor, player):
    to_go = self.dst - player.pos 


class Retreat(Command):
  def __init__(self, amount):
    self.amount = amount

  def action(self, executor, player):
    pass
    to_go = self.dst - player.pos 



class StartTurn(Command):
  def action(self, executor, player):
    if not player.is_free:
      player.strategy.jail_action(player)
    player.push(AfterJailDecision())

class AfterJailDecision(Command):
  def action(self, executor, player):
    if player.is_free:
      player.push(RollAndMove())
    else:
      player.push(StayInJail())

class WrapUpTurn(Command):
  def action(self, executor, player):
    pass

class RollAndMove(Command):
  def __init__(self, count=None):
    if count is None:
      count = 0
    self.count = count

  def action(self, executor, player):
    game = executor
    n, m = player.roll()
    if n == m:
      if self.count == 2:
        player.push(GoToJail())
      else:
        game.move(player, n+m)
        player.push(RollAndMove(self.count+1))
    else:
      game.move(player, n+m)

class StayInJail(Command):
  def action(self, executor, player):
    n, m = player.roll()
    if n == m:
      game.move(player, n+m)
    else:
      player.jail_count += 1
      if player.jail_count > 2:
        player.money -= 50 #forced, but there is an option for Jail Free Card
        game.move(player, n+m)


class GoToJail(Command):
  def action(self, executor, player):
    player.pos = 10
    player.is_free = False
    player.jail_count = 0
    player.zapCommand()

class GetFromBank(Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money += self.amount

class GetJailFree(Command):
  def __init__(self, is_chance=None):
    pass
  def action(self, executor, player):
    pass

class CollectFromAll(Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money += self.amount

class Repair(Command):
  def __init__(self, house, hotel):
    self.house = house
    self.hotel = hotel
  def action(self, executor, player):
    pass


class GetSallary(Command):
  def action(self, executor, player):
    player.money += 200

class PayToBank(Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money -= self.amount

class PayToAll(Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money -= self.amount


class PayAndOut(Command):
  def action(self, executor, player):
    player.money -= 50
    player.is_free = True

class PayRent(Command):
  def __init__(self, owner, amount):
    self.owner = owner
    self.amount = amount
  def action(self, executor, player):
    player.money -= self.amount
    self.owner.money += self.amount
    print player.name, '==(', self.amount, ')=>', self.owner.name

class BuyProperty(Command):
  def __init__(self, property):
    self.property = property

  def action(self, executor, player):
    player.money -= self.property.facevalue
    player.add_property(self.property)


class AdvanceToNearestRailroad(Command):
  pass

class AdvanceToNearestUtility(Command):
  pass






