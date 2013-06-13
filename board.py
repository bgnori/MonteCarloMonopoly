#!/usr/bin/env python

import model

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
    self.xs.append(model.Place(name, self.count))
    self.count += 1

  def addProperty(self, name, **kw):
    self.xs.append(model.Property(name, self.count, **kw))
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



