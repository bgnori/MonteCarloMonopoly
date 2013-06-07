#!/usr/bin/env python
# -*- coding utf-8 -*-

"""
source  http://monopoly.wikia.com/wiki/Community_Chest

The text on each card in the current (as of Sept. 2008) U.S. Standard Edition 
(the "Atlantic City Edition") is as follows, Differences in one or more 
previous US editions appear in {scrolled brackets} (where actual texts 
were in various sizes of ALL CAPS, though this peculiarity is ignored below). 
Art in one or more of those editions is described in <angle brackets>. 
(Parentheses) are in the originals.

Difference in the UK standard edition should appear in [square brackets] 
"""

from command import *

class Card:
  def __init__(self, command, instruction, art):
    self.instruction = instruction
    self.art = art
    self.command = command



COMMUNITY_CHEST_CARDS = [
  Card(AdvanceTo(GO),
    "Advance to Go (Collect $200) ",
    "Mr. M strides in 7-league boots"),
  Card(GetFromBank(200),
    "Bank error in your favor - Collect $200",
    "Mr. M falls back in astonishment as an arm presents a sheaf of cash out of a bank teller's window,"),
  Card(PayToBank(50),
    "Doctor's fees {fee} - Pay $50",
    "Mr. M angrily brandishes crutches as he stomps with a leg cast"),
  Card(GetFromBank(50), 
    "From sale of stock you get $50", #{$45} 
    "Mr. M, happily entangled in the tape of a stock ticker, waves cash (with no $ sign this time)"),
  Card(GetJailFree(),
    """Get Out of Jail Free {Get out of Jail, Free} 
    - This card may be kept until needed or sold""",
    "A winged Mr. M flutters out of a bird cage>"),
  Card(GoToJail(),
    "Go to Jail - Go directly to jail - Do not pass Go - Do not collect $200",
    "A truncheon-wielding policeman in a light-colored uniform lifts a surprised Mr M by the collar"),

  Card(CollectFromAll(50),
    """Grand Opera Night {Opening}
    - Collect $50 from every player for opening night seats""",
    """A wall sign near steps reads "Opera Tonite - 8 PM Sharp";
    Mr. M leans against it checking his pocket watch in annoyance"""),
  Card(GetFromBank(100),
    "Holiday {Xmas} Fund matures - Receive {Collect} $100",
    "Mr. M carries along a giant Xmas sock containing a sheaf of cash"),
  Card(GetFromBank(20),
    "Income tax refund - Collect $20",
    "Mr M faints back against a man displaying the Refund paper"),
  Card(CollectFromAll(10),
    "It is your birthday - Collect $10 from each player", #{Not in the deck}
    "",)
  Card(GetFromBank(100), 
    "Life insurance matures - Collect $100",
    "Below an I N S sign stands a bent Mr M, his long beard brushing the floor"),
  Card(PayToBank(100),
    "Pay hospital fees of $100", # {Pay hospital $100}
    """A bored nurse holds out her hand for payment
    while Mr. M holds 2 swaddled infants, one in each arm"""),
  Card(PayToBank(150),
    "Pay school fees {tax} of $150",
    "A bespectacled schoolboy unhappily receives a head pat and a dime ((Rockefeller style) from Mr. M."),
  Card(GetFromBank(25),
    "Receive $25 consultancy fee", #{Receive for services $25} 
    """As Justice of the Peace, a stern Mr. M holds out his hand
    for fee from an embarrassed groom whose bride hold a bouquet behind him"""),
  Card(Repair(40, 115),
    """You are assessed for street repairs - $40 per house - $115 per hotel""",
    """Mr. M., supported by his near-ubiquitous cane in his left hand, 
    holds a pick and shovel over his right shoulder"""
  Card(GetFromBank(10),
    """You have won second prize in a beauty contest - Collect $10""",
    """Mr. M preens with a sash and large bouquet"""),
  Card(GetFromBank(100),
    """You inherit $100""",
    """Mr M. holds his head as unseen people's hands offer brochures titled
    "Buy Yacht", "World Tour", and "Rolls Royce""")
  ]



