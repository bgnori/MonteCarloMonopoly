#!/usr/bin/env python



class Place:
  def __init__(self, name):
    self.name = name
    self.pos = None
    

class Property(Place):
  def __init__(self, name, **kw):
    Place.__init__(self, name)
    for k, v in kw.items():
      setattr(self, k, v)



PLACES = [
  Place("Go"),
  Property("Mediterranean Avenue", facevalue=60, 
    rent=[2, 10, 30, 90, 160, 250], colorgroups="DarkPurple", cost=50),
  Place("Community Chest"),
  Property("Baltic Avenue", facevalue=60, 
    rent=[4, 20, 60, 180, 320, 450], colorgroups="DarkPurple", cost=50),
  Place("Income TAX"),
  Property("RR1", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None),
  Property("Oriental Avenue", facevalue=100,
    rent=[6, 30, 90, 270, 400, 550], colorgroups="LightBlue", cost=50),
  Place("Chance"),
  Property("Vermont Avenue", facevalue=100,
    rent=[6, 30, 90, 270, 400, 550], colorgroups="LightBlue", cost=50),
  Property("Connecticut Avenue", facevalue=120,
    rent=[8, 40, 100, 300, 450, 600], colorgroups="LightBlue", cost=50),
  Place("Jail/Just visiting"),
  Property("St. Charles Place", facevalue=140,
    rent=[10, 50, 150, 450, 625, 750], colorgroups="LightPurple", cost=100),
  Property("Electric Company", facevalue=150, colorgroups="Utilities", cost=None),
  Property("States Avenue", facevalue=140,
    rent=[10, 50, 150, 450, 625, 750], colorgroups="LightPurple", cost=100),
  Property("Virginia Avenue", facevalue=160,
    rent=[12, 60, 180, 500, 700, 900], colorgroups="LightPurple", cost=100),
  Property("RR2", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None),
  Property("St. James Place", facevalue=180,
    rent=[14, 70, 200, 500, 750, 950], colorgroups="Orange", cost=100),
  Place("Community Chest"),
  Property("Tennessee Avenue", facevalue=180,
    rent=[14, 70, 200, 500, 750, 950], colorgroups="Orange", cost=100),
  Property("New York Avenue", facevalue=200,
    rent=[16, 80, 220, 550, 800, 1000], colorgroups="Orange", cost=100),
  Place("Free Park"),
  Property("Kentucky Avenue", facevalue=220,
    rent=[18, 90, 250, 700, 875, 1050], colorgroups="Red", cost=150),
  Place("Chance"),
  Property("Indiana Avenue", facevalue=220,
    rent=[18, 90, 250, 700, 875, 1050], colorgroups="Red", cost=150),
  Property("Illinois Avenue", facevalue=240,
    rent=[20, 100, 300, 750, 925, 1100], colorgroups="Red", cost=150),
  Property("RR3", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None),
  Property("Atlantic Avenue", facevalue=260,
    rent=[22, 110, 330, 800, 975, 1150], colorgroups="Yellow", cost=150),
  Property("Ventnor Avenue", facevalue=260,
    rent=[22, 110, 330, 800, 975, 1150], colorgroups="Yellow", cost=150),
  Property("Water Works", facevalue=150, colorgroups="Utilities", cost=None),
  Property("Marvin Gardens", facevalue=280,
    rent=[24, 120, 360, 850, 1025, 1200], colorgroups="Yellow", cost=150),
  Place("Go to Jail"),
  Property("South Carolina Avenue", facevalue=300,
    rent=[26, 130, 390, 900, 1100, 1275], colorgroups="Green", cost=200),
  Property("North Carolina Avenue", facevalue=300,
    rent=[26, 130, 390, 900, 1100, 1275], colorgroups="Green", cost=200),
  Place("Community Chest"),
  Property("Pennsylvania Avenue", facevalue=320,
    rent=[28, 150, 450, 1000, 1200, 1400], colorgroups="Green", cost=200),
  Property("RR4", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None),
  Place("Chance"),
  Property("Park Place", facevalue=350,
    rent=[35, 175, 500, 1100, 1300, 1500], colorgroups="DarkBlue", cost=200),
  Place("Luxury Tax"),
  Property("Boardwalk", facevalue=400,
    rent=[50, 200, 600, 1400, 1700, 2000], colorgroups="DarkBlue", cost=200),
]

for i, p in enumerate(PLACES):
  p.pos = i


CHANCES = set([i for i in range(40) if PLACES[i].name == "Chance"])
CHESTS = set([i for i in range(40) if PLACES[i].name == "Community Chest"])
NOACTIONS = set([0, 10, 20])
GO = 0
GOTOJAIL = 30
INCOMETAX = 4
LUXURYTAX = 38

class Eventlog:
  def __init__(self):
    self.log = []
  def report(self, message):
    self.log.append(message)

from command import *

class Board:
  def __init__(self):
    self.ownerof = [None for i in range(40)]
    self.queue = []
    self.players = []

  def add(self, player):
    self.players.append(player)

  def remove(self, player):
    i = self.players.index(player)
    self.players = self.players[:i] + self.players[i+1:]

  def send(self, player, cmd):
    self.queue.append((player, cmd))

  def getCommand(self, player, n, rolled):
    if n in NOACTIONS:
      return NullCommand()
    if n == GOTOJAIL:
      return GoToJail()
    if n == INCOMETAX:
      return PayTax(200)
    if n == LUXURYTAX:
      return PayTax(75)
    if n in CHESTS:
      return CommunityChest(n)
    if n in CHANCES:
      return Chance(n)

    """ pay or buy """
    if self.is_sold(n):
      if self.ownerof[n] == player:
        return None
      else:
        return PayRent(self.ownerof[n], self.calcRent(n, rolled))
    else:
      """ replace this for bidding Strategy """
      return BuyProperty(PLACES[n])
    return None
  
  def zapCommand(self):
    self.queue = []

  def is_sold(self, n):
    return self.ownerof[n] is not None

  def ready(self):
    p = self.players[0]
    self.send(p, StartTurn())

  def nextplayer(self, player):
    n = len(self.players)
    i = self.players.index(player)
    return self.players[(i + 1) % n]

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

  def progress(self):
    if len(self.players) < 2:
      return False
    p, c = self.queue.pop(0)
    print p, c
    c.action(p)
    if not self.queue:
      WrapUpTurn().action(p)
      print p
      self.send(self.nextplayer(p), StartTurn())
    return True


