#!/usr/bin/env python

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




"""
source http://monopoly.wikia.com/wiki/Chance


The text on each card in the current (as of Sept. 2008) U.S. Standard Edition
(the "Atlantic City Edition") is as follows. Differences in one or 
more previous US editions appear in {scrolled brackets} (where actual texts 
were mostly in various sizes of ALL CAPS, and when in upper and lower case 
might be strangely capitalized--e.g., "pay owner Twice the Rental"--though 
none of these peculiarities is noted below). Art in one or more of those 
editions is described in <angle brackets>. 

Differences in the UK standard edition should appear in [square brackets]. 
"""


CHANCE_CARDS = [
  Card(AdvanceTo(GO),
    "Advance to Go (Collect $200)",
    "Mr. M hops on both feet."),
  Card(AdvanceTo(IllinoisAve),
    "Advance to Illinois Ave. - If you pass Go, collect $200", # {Second sentence omitted.}
    """Mr. M has tied a cloth bundle onto his cane to make a bindle, 
    carried over his right shoulder, and is smoking a cigar"""),
  Card(AdvanceTo(StCharlesPlace),
    "Advance to St. Charles Place - If you pass Go, collect $200",
    "Mr. M hurries along, hauling a little boy by the hand"),
  Card(AdvanceToNearestUtility(),
    """Advance token to nearest Utility. If unowned, you may buy it from the Bank. 
    If owned, throw dice and pay owner a total ten times the amount thrown.""",
    "Mr. M trudges along with a huge battleship token on his back"),
  Card(AdvanceToNearestRailroad(),
    """Advance token to the nearest Railroad 
    and pay owner twice the rental to which he/she {he} is otherwise entitled. 
    If Railroad is unowned, you may buy it from the Bank.""", # (There are two of these.) 
    """At lower left, Mr. M carries a large flatiron token with two hands;
    at upper right a railroad crossing is seen"""),
  Card(AdvanceToNearestRailroad(),
    """Advance token to the nearest Railroad 
    and pay owner twice the rental to which he/she {he} is otherwise entitled. 
    If Railroad is unowned, you may buy it from the Bank.""", # (There are two of these.) 
    """At lower left, Mr. M carries a large flatiron token with two hands;
    at upper right a railroad crossing is seen"""),
  Card(GetFromBank(50),
    "Bank pays you dividend of $50",
    """With his feet up on a telephone-bearing desk, 
    Mr. M leans back in an overstuffed chair, blowing cigar smoke rings"""),
  Card(GetJailFree(),
    """Get out of Jail Free - This card may be kept until needed, or traded/sold""",
    #{This card may be kept until needed or sold - Get Out of Jail Free} 
    #{The first sentence is much smaller than the second}
    "Mr. M, in close-fitting one-piece prison stripes, is literally kicked out"),
  Card(Retreit(3),
    "Go back 3 spaces",
    "Mr. M is hauled back by a cane hooked around his neck"
    # {Presumably an allusion to amateur nights at theaters}
    ),
  Card(GoToJail(),
    "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
    "A truncheon-carrying policeman in a dark-colored uniform hauls a surprised Mr M along by the feet"),
  Card(Repair(25, 100),
    """Make general repairs on all your property - For each house pay $25 - For each hotel $100 """,
    """Consulting a "How to Fix It" brochure, a hammer-wielding Mr. M 
    sits astride a house not much larger than he is; it buckles under his weight"""),
  Card(PayToBank(15),
    "Pay poor tax of $15",
    "His trouser pockets pulled out to show them empty, Mr. M spreads his hands"
    #(The video game version replaces this with Speeding fine $15, reportedly also in the UK version.)
    ),
  Card(AdvanceTo(ReadingRailroad),
    """Take a trip to Reading Railroad {Take a ride on the Reading} - If you pass Go, collect $200""",
    "Mr. M rides astride the TOOTing engine of a train"),
  Card(AdvanceTo(Boardwalk),
    """Take a walk on the Boardwalk - Advance token to Boardwalk""", # {Board Walk in both sentences} 
    """Mr. M, a smallish dog hung over one arm, with the other pushes a squalling baby in a small pram;
    behind them, birds fly in the sky above a low fence"""),
  Card(PayToAll(50),
    """You have been elected Chairman of the Board - Pay each player $50""",
    """A newsboy shouts an Extra with Mr. M's headshot on its front page"""),
  Card(GetFromBank(150),
    """Your building {and} loan matures - Collect $150""", # {Up until the 1980s a "building and loan" was a financial institution.} 
    """Mr. M joyfully embraces an apparent wife"""),
  Card(GetFromBank(100),
    """You have won a crossword competition - Collect $100""", #{Not in the deck} 
    ""),
  ]







