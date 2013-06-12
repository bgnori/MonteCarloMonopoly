#!/usr/bin/env python

import model

class AdvanceTo(model.Command):
  def action(self, executor, player):
    to_go = self.destination - player.pos 

class Chance(model.Command):
  def handle_Chance(executor, cmd):
    print 'evoked', cmd

class CommunityChest(model.Command):
  def handle_CommunityChest(executor, cmd):
    print 'evoked', cmd

class Retreat(model.Command):
  def __init__(self, amount):
    self.amount = amount

  def action(self, executor, player):
    pass
    to_go = self.dst - player.pos 

class StartTurn(model.Command):
  def action(self, executor, player):
    if player.dead:
      player.send(player, model.EndTurn())
      return

    player.turns += 1
    if not player.is_free:
      player.strategy.jail_action(player)
    player.send(player, AfterJailDecision())

class AfterJailDecision(model.Command):
  def action(self, executor, player):
    if player.is_free:
      player.send(player, RollAndMove())
    else:
      player.send(player, StayInJail())

class WrapUpTurn(model.Command):
  def action(self, executor, player):
    pass

class RollAndMove(model.Command):
  def __init__(self, count=None):
    if count is None:
      count = 0
    self.count = count

  def action(self, executor, player):
    game = executor
    n, m = player.roll()
    if n == m:
      if self.count == 2:
        player.send(player,GoToJail())
      else:
        game.move(player, n+m)
        player.send(player, RollAndMove(self.count+1))
    else:
      game.move(player, n+m)

class StayInJail(model.Command):
  def action(self, executor, player):
    n, m = player.roll()
    if n == m:
      executor.move(player, n+m) #FIXME
    else:
      player.jail_count += 1
      if player.jail_count > 2:
        player.money -= 50 #forced, but there is an option for Jail Free Card
        executor.move(player, n+m) #FIXME


class GoToJail(model.Command):
  def action(self, executor, player):
    player.pos = 10
    player.is_free = False
    player.jail_count = 0
    executor.push(player, model.EndTurn());

class GetFromBank(model.Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money += self.amount

class GetJailFree(model.Command):
  def __init__(self, is_chance=None):
    pass
  def action(self, executor, player):
    pass

class CollectFromAll(model.Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money += self.amount

class Repair(model.Command):
  def __init__(self, house, hotel):
    self.house = house
    self.hotel = hotel
  def action(self, executor, player):
    pass


class PayToBank(model.Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money -= self.amount


class PayToAll(model.Command):
  def __init__(self, amount):
    self.amount = amount
  def action(self, executor, player):
    player.money -= self.amount


class PayAndOut(model.Command):
  def action(self, executor, player):
    player.money -= 50
    player.is_free = True


class PayRent(model.Command):
  def __init__(self, owner, amount):
    self.owner = owner
    self.amount = amount
  def action(self, executor, player):
    player.money -= self.amount
    self.owner.money += self.amount
    print player.name, '==(', self.amount, ')=>', self.owner.name

class BuyProperty(model.Command):
  def __init__(self, prop):
    self.prop = prop 

  def action(self, executor, player):
    prop = self.prop
    player.money -= prop.facevalue
    player.add_property(prop)
    executor.board.ownerof[prop.pos] = player


class AdvanceToNearestRailroad(model.Command):
  pass

class AdvanceToNearestUtility(model.Command):
  pass



