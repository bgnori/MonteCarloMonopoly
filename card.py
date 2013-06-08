#!/usr/bin/env python

from random import shuffle

class Card:
  def __init__(self, command, instruction, art):
    self.instruction = instruction
    self.art = art
    self.command = command

class Pile:
  def __init__(self, *cards):
    self.cards = cards
    self.pile = list(self.cards)

  def shuffle(self):
    shuffle(self.pile)

  def draw(self):
    self.pop(0)

  def under(self, card):
    self.pile.append(card)


