#!/usr/bin/env python





places = [
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


class Eventlog:
  def __init__(self):
    self.log = []
  def report(self, message):
    self.log.append(message)


class Board:
  def __init__(self):
    self.ownerof = [-1 for i in range(40)]

  def getCommand(self, n):
    if places[n] == "Go to Jail":
      return GoToJail()
    return None

  def is_sold(self, n):
    return self.ownerof[n] != -1


from player import *

def experiment(n):
  b = Board()
  s = AlwaysOutStrategy()
  #s = AlwaysStayStrategy()
  ps = [Player(b, s) for i in range(n)]

  i = 0
  while 1:
    for p in ps:
      p.turn()
    yield sum([p.money for p in ps])


def kmean(n):
  total = [0 for i in range(40)]
  for i in range(n):
    for i, s in enumerate(experiment(4)):
      if i >= 40:
        break
      total[i] += s
  return [1.0*t/n for t in total]

print kmean(100)




