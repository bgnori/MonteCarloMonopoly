#!/usr/bin/env python

import model

class AdvanceTo(model.Command):
  def __call__(self, game):
    to_go = self.destination - self.player.pos 


class Chance(model.Command):
  def __call__(self, game):
    print 'evoked', self


class CommunityChest(model.Command):
  def __call__(self, game):
    print 'evoked', self


class Retreat(model.Command):
  def __call__(self, game):
    pass #to_go = self.dst - player.pos 


class StartTurn(model.Command):
  def __call__(self, game):
    p = self.player
    if p.dead:
      game.push(EndTurn()) 
      return

    p.turns += 1
    if not p.is_free:
      p.strategy.jail_action(game, p)
    game.push(AfterJailDecision(player=p))


class AfterJailDecision(model.Command):
  def __call__(self, game):
    p = self.player
    if p.is_free:
      game.push(RollAndMove(player=p))
    else:
      game.push(StayInJail(player=p))


class RollAndMove(model.Command):
  defaults = {"count":0}
  def __call__(self, game):
    p = self.player
    n, m = p.roll()
    if n == m:
      if self.count == 2:
        game.push(GoToJail(player=p))
      else:
        game.push(RollAndMove(player=p, count=self.count+1))
        game.push(MoveN(player=p, n=n+m))
    else:
      game.push(MoveN(player=p, n=n+m))


class MoveN(model.Command):
  def __call__(self, game):
    p = self.player
    print p, 'moving', self.n
    assert p.pos != 30 # never from "Go To Jail"
    d, p.pos = divmod(p.pos + self.n, 40)
    if d == 1:
      p.go_count += 1
      game.push(GetFromBank(player=p, amount=200)) #FIXME order!!
    game.push(LandOn(player=p, rolled=self.n))

GOTOJAIL = 30
INCOMETAX = 4
LUXURYTAX = 38

class LandOn(model.Command):
  def __call__(self, game):
    theBoard = game.board
    player = self.player
    rolled = self.rolled
    n = player.pos
    p = theBoard.places[n]
    if isinstance(p, model.Property):
      """ Property is SubClass of Place, must be this order """
      """ pay or buy """
      if theBoard.is_sold(n):
        if theBoard.ownerof[n] == player:
          print 'you have it :)'
          return None
        else:
          return game.push(PayRent(player=player, owner=theBoard.ownerof[n], amount=theBoard.calcRent(n, rolled)))
      else:
        """ replace this for bidding Strategy """
        return game.push(BuyProperty(prop=p, player=player))
    elif isinstance(p, model.Place):
      if p in theBoard.noactions:
        return model.NullCommand()
      if n == GOTOJAIL:
        return game.push(GoToJail(player=player))
      if n == INCOMETAX:
        return game.push(PayToBank(player=player, amount=200))
      if n == LUXURYTAX:
        return game.push(PayToBank(player=player, amount=75))
      if p in theBoard.chests:
        return game.push(CommunityChest(player=player, at=n))
      if p in theBoard.chances:
        return game.push(Chance(player=player, at=n))
      assert False
    else:
      assert False
    return None



class StayInJail(model.Command):
  def __call__(self, game):
    p = self.player
    n, m = p.roll()
    if n == m:
      game.push(MoveN(player=p, n=n+m))
    else:
      p.jail_count += 1
      if p.jail_count > 2:
        p.money -= 50 #FIXME forced, but there is an option for Jail Free Card
        game.push(MoveN(player=p, n=n+m))


class GoToJail(model.Command):
  def __call__(self, game):
    p = self.player
    p.pos = 10
    p.is_free = False
    p.jail_count = 0
    game.push(model.EndTurn()); #FIXME may build house, trade etc.


class GetFromBank(model.Command):
  def __call__(self, game):
    self.player.money += self.amount

class GetJailFree(model.Command):
  defaults= dict(is_chance=None)
  def __call__(self, game):
    pass

class CollectFromAll(model.Command):
  def __call__(self, game):
    self.player.money += self.amount 

class Repair(model.Command):
  defaults = dict(houst=0, hotel=0)
  def __call__(self, game):
    pass


class PayToBank(model.Command):
  def __call__(self, game):
    self.player.money -= self.amount


class PayToAll(model.Command):
  def __call__(self, game):
    self.player.money -= self.amount


class PayAndOut(model.Command):
  def __call__(self, game):
    self.player.money -= 50
    self.player.is_free = True


class PayRent(model.Command):
  defaults = dict(owner=None, amount=0)
  def __call__(self, game):
    player = self.player
    player.money -= self.amount
    self.owner.money += self.amount
    print player.name, '==(', self.amount, ')=>', self.owner.name

class BuyProperty(model.Command):
  defaults = dict(prop=None)
  def __call__(self, game):
    prop = self.prop
    player = self.player
    player.money -= prop.facevalue
    player.add_property(prop)
    game.board.ownerof[prop.pos] = player


class AdvanceToNearestRailroad(model.Command):
  pass

class AdvanceToNearestUtility(model.Command):
  pass



