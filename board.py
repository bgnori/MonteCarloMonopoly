#!/usr/bin/env python

class Place(object):
  def __init__(self, name, pos):
    self.name = name
    self.pos = pos
  def __str__(self):
    return "<" + self.name + ">"

class Property(Place):
  def __init__(self, name, pos, **kw):
    Place.__init__(self, name, pos)
    for k, v in kw.items():
      assert k not in ('name', 'pos')
      setattr(self, k, v)

class Places:
  def __init__(self):
    self.xs = []
    self.count = 0

  def __len__(self):
    return len(self.xs)

  def __getitem__(self, n):
    return self.xs[n]

  def resolve(self, name):
    for i, p in enumerate(self.xs):
      if p.name == name:
        return i, p
    return -1, None

  def addPlace(self, name):
    self.xs.append(Place(name, self.count))
    self.count += 1

  def addProperty(self, name, **kw):
    self.xs.append(Property(name, self.count, **kw))
    self.count += 1

  @property
  def chances(self):
    return set([x for x in self.xs if x.name == "Chance"])

  @property
  def chests(self):
    return set([x for x in self.xs if x.name == "Community Chest"])

  @property
  def noactions(self):
    return set([x for x in self.xs if x.name in ("Go", "Jail/Just visiting", "Free Park")])

  @property
  def prefixactions(self):
    pass
    ("Go to Jail")
GOTOJAIL = 30
INCOMETAX = 4
LUXURYTAX = 38

import model

from command import *

class Board:
  def __init__(self, places):
    self.places = places
    c = len(places)
    self.ownerof = [None for i in range(c)]
    self.chests = places.chests
    self.chances = places.chances
    print self.chances
    self.noactions = places.noactions
    print self.noactions

  def __getitem__(self, n):
    return self.places[n]

  def getCommand(self, player, n, rolled):
    p = self.places[n]
    print 'getCommand', n, p
    if isinstance(p, Property):
      """ Property is SubClass of Place, must be this order """
      """ pay or buy """
      if self.is_sold(n):
        if self.ownerof[n] == player:
          print 'you have it :)'
          return None
        else:
          return PayRent(self.ownerof[n], self.calcRent(n, rolled))
      else:
        """ replace this for bidding Strategy """
        return BuyProperty(p)
    elif isinstance(p, Place):
      if p in self.noactions:
        return model.NullCommand()
      if n == GOTOJAIL:
        return GoToJail()
      if n == INCOMETAX:
        return PayToBank(200)
      if n == LUXURYTAX:
        return PayToBank(75)
      if p in self.chests:
        return CommunityChest(at=n)
      if p in self.chances:
        return Chance(at=n)
      assert False
    else:
      assert False
    return None

  def is_sold(self, n):
    return self.ownerof[n] is not None

  def getColorGroups(self, color):
    return [p for p in self.places if getattr(p, "colorgroups", '') == color]

  def calcRent(self, n, rolled):
    theproperty = self.places[n]
    housing = theproperty.cost 
    color = theproperty.colorgroups
    owner = self.ownerof[n]
    if housing:
      """ usual color group """
      if all([ p in owner.owns for p in self.getColorGroups(color)]):
        ''' monopoly '''
        return theproperty.rent[0] * 2
      else:
        return theproperty.rent[0]
    else:
      """RailRoad or Utilities"""
      count = 0
      for p in self.getColorGroups(color):
        if p in owner.owns:
          count+=1
      if theproperty.colorgroups == "RailRoad":
        assert count < 5
        assert count > 0
        return theproperty.rent[count]
      elif theproperty.colorgroups == "Utilities":
        if count == 1:
          return rolled * 4
        elif count == 2:
          return rolled * 10
        else:
          assert False
      else:
        assert False



