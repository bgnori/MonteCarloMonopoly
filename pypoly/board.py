#!/usr/bin/env python

from pypoly import models

class Places:
  def __init__(self, landon_command):
    self.xs = []
    self.count = 0
    self.landon_command = landon_command

  def __len__(self):
    return len(self.xs)

  def __getitem__(self, n):
    return self.xs[n]

  def resolve(self, name):
    for p in self.xs:
      if p.name == name:
        return p
    return None

  def addPlace(self, name, landon_command):
    self.xs.append(models.Place(name, landon_command, self.count))
    self.count += 1

  def addProperty(self, name, **kw):
    self.xs.append(models.Place(name, self.landon_command, self.count, **kw))
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

  def calcRent(self, pos, n, by_dice):
    theproperty = self.places[pos]
    housing = theproperty.cost 
    color = theproperty.colorgroups
    owner = self.ownerof[pos]
    if housing:
      """ usual color group """
      if all([ p in owner.owns for p in self.getColorGroups(color)]):
        ''' monopoly '''
        ''' FIXME need to handle house/hotel '''
        return theproperty.rent[0] * 2
      else:
        return theproperty.rent[0]
    else:
      """RailRoad or Utilities"""
      assert by_dice
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
          return n * 4
        elif count == 2:
          return n * 10
        else:
          assert False
      else:
        assert False



