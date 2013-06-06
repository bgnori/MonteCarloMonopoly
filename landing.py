#!/usr/bin/env python



PLACES = [
  "Go",
  "Mediterranean Avenue",
  "Community Chest",
  "Baltic Avenue",
  "Income TAX",
  "RR1",
  "Oriental Avenue",
  "Chance",
  "Vermont Avenue",
  "Connecticut Avenue",
  "Jail/Just visiting",
  "St. Charles Place",
  "Electric Company",
  "States Avenue",
  "Virginia Avenue",
  "RR2",
  "St. James Place",
  "Community Chest",
  "Tennessee Avenue",
  "New York Avenue",
  "Free Park",
  "Kentucky Avenue",
  "Chance",
  "Indiana Avenue",
  "Illinois Avenue",
  "RR3",
  "Atlantic Avenue",
  "Ventnor Avenue",
  "Water Works",
  "Marvin Gardens",
  "Go to Jail",
  "South Carolina Avenue",
  "North Carolina Avenue",
  "Community Chest",
  "Pennsylvania Avenue",
  "RR4",
  "Chance",
  "Park Place",
  "Luxury Tax",
  "Boardwalk",
]


CHANCES = set([i for i in range(40) if PLACES[i] == "Chance"])
CHESTS = set([i for i in range(40) if PLACES[i] == "Community Chest"])
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
    self.ownerof = [-1 for i in range(40)]
    self.queue = []
    self.players = []

  def add(self, player):
    self.players.append(player)

  def remove(self, player):
    i = self.players.index(player)
    self.players = self.players[:i] + self.players[i+1:]

  def send(self, player, cmd):
    self.queue.append((player, cmd))

  def getCommand(self, n):
    if n == GOTOJAIL:
      return GoToJail()
    if n == INCOMETAX:
      return PayTax(200)
    if n == LUXURYTAX:
      return PayTax(75)

    return None
  
  def zapCommand(self):
    self.queue = []

  def is_sold(self, n):
    return self.ownerof[n] != -1

  def ready(self):
    p = self.players[0]
    self.send(p, StartTurn())

  def nextplayer(self, player):
    n = len(self.players)
    i = self.players.index(player)
    return self.players[(i + 1) % n]


  def progress(self):
    if len(self.players) < 2:
      return False
    p, c = self.queue.pop(0)
    print p, c
    c.action(p)
    if not self.queue:
      self.send(self.nextplayer(p), StartTurn())
    return True



