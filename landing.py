#!/usr/bin/env python

from random import randint
 


def dice():
  return randint(1, 6), randint(1, 6)


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
  def getCommand(self, n):
    if places[n] == "Go to Jail":
      return GoToJail()
    return None


class Player:
  def __init__(self, board, strategy, pos=None):
    if pos is None:
      pos = 0
    self.pos = pos
    self.board = board
    self.queue = []
    self.money = 1500
    self.is_free = True
    self.jail_count = 0
    self.strategy = strategy

  def push(self, cmd):
    self.queue.append(cmd)

  def roll(self):
    return dice()

  def move(self, n):
    d, self.pos = divmod(self.pos + n, 40)
    if d == 1:
      self.push(GetSallary())
    return self.board.getCommand(self.pos)

  def pop(self):
    return self.queue.pop(0)

  def hasCommand(self):
    return bool(self.queue)


  def preCommand(self):
    pass

  def postCommand(self):
    pass

  def turn(self):
    if not self.is_free:
      self.strategy.jail_action(self)

    if self.is_free:
      self.push(RollAndMove())
    else:
      self.push(StayInJail())

    while self.hasCommand():
      self.preCommand()
      cmd = self.pop()
      cmd = cmd.action(self)
      self.postCommand()
      if cmd:
        self.push(cmd)

class Strategy:
  '''not yet'''
  def jail_action(self, player):
    raise


class AlwaysOutStrategy(Strategy):
  def jail_action(self, player):
    player.push(PayAndOut())

class AlwaysStayStrategy(Strategy):
  def jail_action(self, player):
    pass



class Command:
  def action(self, player):
    pass


class RollAndMove(Command):
  def __init__(self, count=None):
    if count is None:
      count = 0
    self.count = count

  def action(self, player):
    n, m = player.roll()
    cmd = player.move(n+m)
    if cmd:
      ''' go to jail''' #FIXME how about payment?
      return cmd

    if n == m:
      if self.count == 2:
        return GoToJail()
      else:
        return RollAndMove(self.count+1)
    return None

class StayInJail(Command):
  def action(self, player):
    n, m = player.roll()
    if n == m:
      cmd = player.move(n+m)
      return cmd
    else:
      player.jail_count += 1
      if player.jail_count > 2:
        player.money -= 50 #forced
        cmd = player.move(n+m)
        return cmd
      return None
    assert False

class GoToJail(Command):
  def action(self, player):
    player.pos = 10
    player.is_free = False
    player.jail_count = 0

class GetSallary(Command):
  def action(self, player):
    player.money += 200

class PayAndOut(Command):
  def action(self, player):
    player.money -= 50
    player.is_free = True


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


