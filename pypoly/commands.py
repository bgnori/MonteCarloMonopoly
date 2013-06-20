#!/usr/bin/env python

from pypoly import models

class AdvanceTo(models.Command):
  defaults = {"destination":None}
  def __call__(self, game):
    if self.destination is None:
      print self
      assert False
    to_go = (40 + self.destination.pos - self.player.pos) % 40
    assert to_go > 0
    game.push(MoveN(player=self.player, n=to_go, by_dice=False))


class DrawChance(models.Command):
  def __call__(self, game):
    card = game.drawChance()
    cmd = card.fn(self.player, card)
    print card, cmd
    if not isinstance(cmd, GetJailFree):
      game.putBackChance(card)
    game.push(cmd)


class DrawCommunityChest(models.Command):
  def __call__(self, game):
    card = game.drawCommunityChest()
    cmd = card.fn(self.player, card)
    print card.instruction, cmd
    if not isinstance(cmd, GetJailFree):
      game.putBackCommunityChest(card)
    game.push(cmd)


class Retreat(models.Command):
  def __call__(self, game):
    pos = (40 + self.player.pos - self.amount) % 40
    self.player.pos = pos
    game.push(LandOn(player=self.player, n=-self.amount, by_dice=False))


class StartTurn(models.Command):
  def __call__(self, game):
    p = self.player
    if p.dead:
      game.push(EndTurn()) 
      return
    p.turns += 1
    game.push(AfterJailDecision(player=p))
    if not p.is_free:
      p.strategy.jail_action(game, p)


class AfterJailDecision(models.Command):
  def __call__(self, game):
    p = self.player
    if p.is_free:
      game.push(RollAndMove(player=p))
    else:
      game.push(StayInJail(player=p))


class RollAndMove(models.Command):
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


class MoveN(models.Command):
  defaults = dict(n=0, by_dice=True)
  def __call__(self, game):
    p = self.player
    print p, 'moving', self.n
    assert p.pos != 30 # never from "Go To Jail"
    assert isinstance(p.pos, int)
    assert isinstance(self.n, int)
    d, p.pos = divmod(p.pos + self.n, 40)
    if d == 1:
      p.go_count += 1
      game.push(GetFromBank(player=p, amount=200)) #FIXME order!!
    game.push(LandOn(player=p, n=self.n, by_dice=self.by_dice))


class LandOnProperty(models.Command):
  defaults = dict(n=0, by_dice=True)
  def __call__(self, game):
    theBoard = game.board
    player = self.player
    p = theBoard.places[player.pos]
    if theBoard.is_sold(player.pos):
      if theBoard.ownerof[player.pos] == player:
        print 'you have it :)'
      else:
        game.push(XPayToY(
          x=player, 
          y=theBoard.ownerof[player.pos], 
          amount=theBoard.calcRent(player.pos, self.n, self.by_dice)))
    else:
      """ replace this for bidding Strategy """
      assert self.player.pos != 30
      game.push(BuyProperty(prop=p, player=player))


class OnCommunityChest(models.Command):
  def __call__(self, game):
    return game.push(DrawCommunityChest(player=self.player, pos=self.pos))


class OnIncomeTax(models.Command):
  def __call__(self, game):
    return game.push(PayToBank(player=self.player, amount=200))


class OnLuxuryTax(models.Command):
  def __call__(self, game):
    return game.push(PayToBank(player=self.player, amount=50))


class OnChance(models.Command):
  def __call__(self, game):
    return game.push(DrawChance(player=self.player, pos=self.pos))


class OnGoToJail(models.Command):
  def __call__(self, game):
    return game.push(GoToJail(player=self.player))


class LandOn(models.Command):
  defaults = dict(n=0, by_dice=True, player=None)
  def __call__(self, game):
    p = game.board.places[self.player.pos]
    assert self.player.pos == p.pos
    assert self.player.pos != 30 or p.command_class == OnGoToJail
    print "LandOn", p.command_class
    game.push(p.command_class(player=self.player, n=self.n, pos=self.player.pos))


class StayInJail(models.Command):
  def __call__(self, game):
    p = self.player
    n, m = p.roll()
    if n == m:
      game.push(MoveN(player=p, n=n+m))
    else:
      p.jail_count += 1
      if p.jail_count > 2:
        if p.cards:
          game.push(MoveN(player=p, n=n+m))
          card = p.cards.pop()
          game.push(FreeByCard(player=player, card=card))
        elif p.money > 50:
          game.push(MoveN(player=p, n=n+m))
          p.money -= 50 #FIXME forced, but there is an option for Jail Free Card
        else:
          pass
          #CashByDeal
        """
        elif p.estimateLiqudate() > 50:
          game.push(CashByMortgage(player=p))
        """


class GoToJail(models.Command):
  def __call__(self, game):
    p = self.player
    p.pos = 10
    p.is_free = False
    p.jail_count = 0
    game.push(models.EndTurn()); #FIXME may build house, trade etc.


class GetFromBank(models.Command):
  def __call__(self, game):
    self.player.money += self.amount


class GetJailFree(models.Command):
  defaults= dict(is_chance=None)
  def __call__(self, game):
    self.player.cards.add(self.card)


class XPayToY(models.Command):
  def __call__(self, game):
    self.x.money -= self.amount  #FIXME
    self.y.money += self.amount
    print self.x.name, '==(', self.amount, ')=>', self.y.name


class CollectFromAll(models.Command):
  def __call__(self, game):
    cs = []
    p = game.nextplayer(self.player)
    while p != self.player:
      if p.dead:
        continue
      cs.append(XPayToY(amount=self.amount, x=p, y=self.player))
      p = game.nextplayer(p)

    for c in reversed(cs):
      game.push(c)


class Repair(models.Command):
  defaults = dict(houst=0, hotel=0)
  def __call__(self, game):
    cost = sum([p.calcFix(self.house, self.hotel) for p in self.player.owns])
    game.push(PayToBank(player=self.player, amount=cost))


class PayToBank(models.Command):
  def __call__(self, game):
    self.player.money -= self.amount #FIXME


class PayToAll(models.Command):
  def __call__(self, game):
    cs = []
    p = game.nextplayer(self.player)
    while p != self.player:
      if p.dead:
        continue
      cs.append(XPayToY(amount=self.amount, x=self.player, y=p))
      p = game.nextplayer(p)

    for c in reversed(cs):
      game.push(c)


class PayAndOut(models.Command):
  def __call__(self, game):
    self.player.money -= 50 #FIXME
    self.player.is_free = True

class FreeByCard(models.Command):
  def __call__(self, game):
    if isinstance(self.card, models.ChanceCard):
      game.putBackChance(self.card)
    elif isinstance(self.card, models.CommunityChestCard):
      game.putBackCommunityChest(self.card)
    self.player.is_free = True

class BuyProperty(models.Command):
  defaults = dict(player=None, prop=None)
  def __call__(self, game):
    assert isinstance(self.prop, models.Place)
    assert self.prop.pos != 30
    self.player.money -= self.prop.facevalue #FIXME short on cash, to buy. morgage
    self.player.add_property(self.prop)
    game.board.ownerof[self.prop.pos] = self.player


class AdvanceToNearestRailroad(models.Command):
  def __call__(self, game):
    pos = self.player.pos
    while getattr(game.board[pos], "colorgroups", "") != 'RailRoad':
      pos = (pos + 1) % 40
    travel = (40 + pos - self.player.pos) % 40

    game.push(MoveN(player=self.player, n=travel, by_dice=False)) #FIXME double!


class AdvanceToNearestUtility(models.Command):
  def __call__(self, game):
    pos = self.player.pos
    while getattr(game.board[pos], "colorgroups", "") != 'Utilities':
      pos = (pos + 1) % 40
    travel = (40 + pos - self.player.pos) % 40

    game.push(MoveN(player=self.player, n=travel, by_dice=False)) #FIXME fix rate


class CashByMortgage(models.Command):
  def __call__(self, game):
    pass


class CashByDeal(models.Command):
  def __call__(self, game):
    pass


