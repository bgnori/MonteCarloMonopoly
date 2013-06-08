#!/usr/bin/env python



class Places:
  class Place:
    def __init__(self, name):
      self.name = name

  class Property(Place):
    def __init__(self, name, **kw):
      Places.Place.__init__(self, name)
      for k, v in kw.items():
        setattr(self, k, v)


  def __init__(self):
    self.xs = []

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
    self.xs.append(self.Place(name))

  def addProperty(self, name, **kw):
    self.xs.append(self.Property(name, **kw))

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


from command import *

class Board:
  def __init__(self, places):
    self.places = places
    c = len(places)
    self.ownerof = [None for i in range(c)]
    self.chests = places.chests
    self.chances = places.chances
    self.noactions = places.noactions

  def getCommand(self, player, n, rolled):
    if isinstance(self.places[n], Places.Place):
      if n in self.noactions:
        return NullCommand()
      if n == GOTOJAIL:
        return GoToJail()
      if n == INCOMETAX:
        return PayToBank(200)
      if n == LUXURYTAX:
        return PayToBank(75)
      if n in self.chests:
        return CommunityChest(n)
      if n in self.chances:
        return Chance(n)

    elif isinstance(self.places[n], Places.Property):
      """ pay or buy """
      if self.is_sold(n):
        if self.ownerof[n] == player:
          return None
        else:
          return PayRent(self.ownerof[n], self.calcRent(n, rolled))
      else:
        """ replace this for bidding Strategy """
        return BuyProperty(PLACES[n])
    else:
      assert False
    return None

  def is_sold(self, n):
    return self.ownerof[n] is not None

  def getColorGroups(self, color):
    return [p for p in PLACES if getattr(p, "colorgroups", '') == color]

  def calcRent(self, n, rolled):
    property = PLACES[n]
    housing = property.cost 
    color = property.colorgroups
    owner = self.ownerof[n]
    if housing:
      """ usual color group """
      if all([ p in owner.owns for p in self.getColorGroups(color)]):
        ''' monopoly '''
        return property.rent[0] * 2
      else:
        return property.rent[0]
    else:
      """RailRoad or Utilities"""
      count = 0
      for p in self.getColorGroups(color):
        if p in owner.owns:
          count+=1
      if property.colorgroups == "RailRoad":
        assert count < 5
        assert count > 0
        return property.rent[count]
      elif property.colorgroups == "Utilities":
        if count == 1:
          return rolled * 4
        elif count == 2:
          return rolled * 10
        else:
          assert False
      else:
        assert False



