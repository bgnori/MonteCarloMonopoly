#!/usr/bin/env python

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


