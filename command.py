#!/usr/bin/env python

import model

class AdvanceTo(model.Command):
  defaults = {"destination":None}
  def __call__(self, game):
    if self.destination is None:
      print self
      assert False
    to_go = (40 + self.destination.pos - self.player.pos) % 40
    assert to_go > 0
    game.push(MoveN(player=self.player, n=to_go, by_dice=False))


class DrawChance(model.Command):
  def __call__(self, game):
    card = game.drawChance()
    cmd = card.fn(self.player, card)
    print card, cmd
    game.push(cmd)


class DrawCommunityChest(model.Command):
  def __call__(self, game):
    card = game.drawCommunityChest()
    cmd = card.fn(self.player, card)
    print card.instruction, cmd
    game.push(cmd)


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
  defaults = dict(n=0, by_dice=True)
  def __call__(self, game):
    p = self.player
    print p, 'moving', self.n
    assert p.pos != 30 # never from "Go To Jail"
    d, p.pos = divmod(p.pos + self.n, 40)
    if d == 1:
      p.go_count += 1
      game.push(GetFromBank(player=p, amount=200)) #FIXME order!!
    game.push(LandOn(player=p, n=self.n, by_dice=self.by_dice))

GOTOJAIL = 30
INCOMETAX = 4
LUXURYTAX = 38

class LandOnProperty(model.Command):
  defaults = dict(n=0, by_dice=True)
  def __call__(self, game):
    theBoard = game.board
    player = self.player
    p = theBoard.places[player.pos]
    if theBoard.is_sold(player.pos):
      if theBoard.ownerof[player.pos] == player:
        print 'you have it :)'
      else:
        game.push(PayRent(
          player=player, 
          owner=theBoard.ownerof[player.pos], 
          amount=theBoard.calcRent(player.pos, self.n, self.by_dice)))
    else:
      """ replace this for bidding Strategy """
      assert self.player.pos != 30
      game.push(BuyProperty(prop=p, player=player))

class OnCommunityChest(model.Command):
  def __call__(self, game):
    return game.push(DrawCommunityChest(player=self.player, pos=self.pos))

class OnIncomeTax(model.Command):
  def __call__(self, game):
    return game.push(PayToBank(player=self.player, amount=200))

class OnChance(model.Command):
  def __call__(self, game):
    return game.push(DrawChance(player=self.player, pos=self.pos))

class OnGoToJail(model.Command):
  def __call__(self, game):
    return game.push(GoToJail(player=self.player))

class LandOn(model.Command):
  defaults = dict(n=0, by_dice=True, player=None)
  def __call__(self, game):
    p = game.board.places[self.player.pos]
    assert self.player.pos == p.pos
    assert self.player.pos != 30 or p.command_class == OnGoToJail
    print "LandOn", p.command_class
    game.push(p.command_class(player=self.player, n=self.n, pos=self.player.pos))


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
  defaults = dict(player=None, prop=None)
  def __call__(self, game):
    assert isinstance(self.prop, model.Place)
    assert self.prop.pos != 30
    self.player.money -= self.prop.facevalue
    self.player.add_property(self.prop)
    game.board.ownerof[self.prop.pos] = self.player


class AdvanceToNearestRailroad(model.Command):
  def __call__(self, game):
    pass

class AdvanceToNearestUtility(model.Command):
  def __call__(self, game):
    pass



