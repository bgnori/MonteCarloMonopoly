# set of subclass and data


from board import Places
from model import Card, NullCommand
import model
from command import *


myPlace = Places(LandOnProperty)

myPlace.addPlace("Go", NullCommand)

myPlace.addProperty("Mediterranean Avenue", facevalue=60, 
    rent=[2, 10, 30, 90, 160, 250], colorgroups="DarkPurple", cost=50)

class OnCommunityChest(model.Command):
  def __call__(self, game):
    return game.push(DrawCommunityChest(player=self.player, pos=self.pos))

myPlace.addPlace("Community Chest", OnCommunityChest)

myPlace.addProperty("Baltic Avenue", facevalue=60, 
    rent=[4, 20, 60, 180, 320, 450], colorgroups="DarkPurple", cost=50)


class OnIncomeTax(model.Command):
  def __call__(self, game):
    return game.push(PayToBank(player=self.player, amount=200))
myPlace.addPlace("Income TAX", OnIncomeTax)

myPlace.addProperty("RR1", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None)

myPlace.addProperty("Oriental Avenue", facevalue=100,
    rent=[6, 30, 90, 270, 400, 550], colorgroups="LightBlue", cost=50)

class OnChance(model.Command):
  def __call__(self, game):
    return game.push(DrawChance(player=self.player, pos=self.pos))
myPlace.addPlace("Chance", OnChance)


myPlace.addProperty("Vermont Avenue", facevalue=100,
    rent=[6, 30, 90, 270, 400, 550], colorgroups="LightBlue", cost=50)
myPlace.addProperty("Connecticut Avenue", facevalue=120,
    rent=[8, 40, 100, 300, 450, 600], colorgroups="LightBlue", cost=50)

myPlace.addPlace("Jail/Just visiting", NullCommand)

myPlace.addProperty("St. Charles Place", facevalue=140,
    rent=[10, 50, 150, 450, 625, 750], colorgroups="LightPurple", cost=100)
myPlace.addProperty("Electric Company", facevalue=150, colorgroups="Utilities", cost=None)
myPlace.addProperty("States Avenue", facevalue=140,
    rent=[10, 50, 150, 450, 625, 750], colorgroups="LightPurple", cost=100)
myPlace.addProperty("Virginia Avenue", facevalue=160,
    rent=[12, 60, 180, 500, 700, 900], colorgroups="LightPurple", cost=100)
myPlace.addProperty("RR2", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None)
myPlace.addProperty("St. James Place", facevalue=180,
    rent=[14, 70, 200, 500, 750, 950], colorgroups="Orange", cost=100)
myPlace.addPlace("Community Chest", OnCommunityChest)
myPlace.addProperty("Tennessee Avenue", facevalue=180,
    rent=[14, 70, 200, 500, 750, 950], colorgroups="Orange", cost=100)
myPlace.addProperty("New York Avenue", facevalue=200,
    rent=[16, 80, 220, 550, 800, 1000], colorgroups="Orange", cost=100)
myPlace.addPlace("Free Park", NullCommand)
myPlace.addProperty("Kentucky Avenue", facevalue=220,
    rent=[18, 90, 250, 700, 875, 1050], colorgroups="Red", cost=150)
myPlace.addPlace("Chance", OnChance)
myPlace.addProperty("Indiana Avenue", facevalue=220,
    rent=[18, 90, 250, 700, 875, 1050], colorgroups="Red", cost=150)
myPlace.addProperty("Illinois Avenue", facevalue=240,
    rent=[20, 100, 300, 750, 925, 1100], colorgroups="Red", cost=150)
myPlace.addProperty("RR3", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None)
myPlace.addProperty("Atlantic Avenue", facevalue=260,
    rent=[22, 110, 330, 800, 975, 1150], colorgroups="Yellow", cost=150)
myPlace.addProperty("Ventnor Avenue", facevalue=260,
    rent=[22, 110, 330, 800, 975, 1150], colorgroups="Yellow", cost=150)
myPlace.addProperty("Water Works", facevalue=150, colorgroups="Utilities", cost=None)
myPlace.addProperty("Marvin Gardens", facevalue=280,
    rent=[24, 120, 360, 850, 1025, 1200], colorgroups="Yellow", cost=150)


class OnGoToJail(model.Command):
  def __call__(self, game):
    return game.push(GoToJail(player=self.player))
myPlace.addPlace("Go to Jail", OnGoToJail)

myPlace.addProperty("South Carolina Avenue", facevalue=300,
    rent=[26, 130, 390, 900, 1100, 1275], colorgroups="Green", cost=200)
myPlace.addProperty("North Carolina Avenue", facevalue=300,
    rent=[26, 130, 390, 900, 1100, 1275], colorgroups="Green", cost=200)
myPlace.addPlace("Community Chest", OnCommunityChest)
myPlace.addProperty("Pennsylvania Avenue", facevalue=320,
    rent=[28, 150, 450, 1000, 1200, 1400], colorgroups="Green", cost=200)
myPlace.addProperty("RR4", facevalue=200,
    rent=[0, 25, 50, 100, 200], colorgroups="RailRoad", cost=None)
myPlace.addPlace("Chance", OnChance)
myPlace.addProperty("Park Place", facevalue=350,
    rent=[35, 175, 500, 1100, 1300, 1500], colorgroups="DarkBlue", cost=200)

class OnLuxuryTax(model.Command):
  def __call__(self, game):
    return game.push(PayToBank(player=self.player, amount=50))
myPlace.addPlace("Luxury Tax", OnLuxuryTax)
myPlace.addProperty("Boardwalk", facevalue=400,
    rent=[50, 200, 600, 1400, 1700, 2000], colorgroups="DarkBlue", cost=200)




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

COMMUNITY_CHEST_CARDS = [
  Card(AdvanceTo(destination=myPlace.resolve('GO')),
    "Advance to Go (Collect $200) ",
    "Mr. M strides in 7-league boots"),
  Card(GetFromBank(amount=200),
    "Bank error in your favor - Collect $200",
    "Mr. M falls back in astonishment as an arm presents a sheaf of cash out of a bank teller's window,"),
  Card(PayToBank(amount=50),
    "Doctor's fees {fee} - Pay $50",
    "Mr. M angrily brandishes crutches as he stomps with a leg cast"),
  Card(GetFromBank(amount=50), 
    "From sale of stock you get $50", #{$45} 
    "Mr. M, happily entangled in the tape of a stock ticker, waves cash (with no $ sign this time)"),
  Card(GetJailFree(),
    """Get Out of Jail Free {Get out of Jail, Free} 
    - This card may be kept until needed or sold""",
    "A winged Mr. M flutters out of a bird cage>"),
  Card(GoToJail(),
    "Go to Jail - Go directly to jail - Do not pass Go - Do not collect $200",
    "A truncheon-wielding policeman in a light-colored uniform lifts a surprised Mr M by the collar"),

  Card(CollectFromAll(amount=50),
    """Grand Opera Night {Opening}
    - Collect $50 from every player for opening night seats""",
    """A wall sign near steps reads "Opera Tonite - 8 PM Sharp";
    Mr. M leans against it checking his pocket watch in annoyance"""),
  Card(GetFromBank(amount=100),
    "Holiday {Xmas} Fund matures - Receive {Collect} $100",
    "Mr. M carries along a giant Xmas sock containing a sheaf of cash"),
  Card(GetFromBank(amount=20),
    "Income tax refund - Collect $20",
    "Mr M faints back against a man displaying the Refund paper"),
  Card(CollectFromAll(amount=10),
    "It is your birthday - Collect $10 from each player", #{Not in the deck}
    ""),
  Card(GetFromBank(amount=100), 
    "Life insurance matures - Collect $100",
    "Below an I N S sign stands a bent Mr M, his long beard brushing the floor"),
  Card(PayToBank(amount=100),
    "Pay hospital fees of $100", # {Pay hospital $100}
    """A bored nurse holds out her hand for payment
    while Mr. M holds 2 swaddled infants, one in each arm"""),
  Card(PayToBank(amount=150),
    "Pay school fees {tax} of $150",
    "A bespectacled schoolboy unhappily receives a head pat and a dime ((Rockefeller style) from Mr. M."),
  Card(GetFromBank(amount=25),
    "Receive $25 consultancy fee", #{Receive for services $25} 
    """As Justice of the Peace, a stern Mr. M holds out his hand
    for fee from an embarrassed groom whose bride hold a bouquet behind him"""),
  Card(Repair(house=40, hotel=115),
    """You are assessed for street repairs - $40 per house - $115 per hotel""",
    """Mr. M., supported by his near-ubiquitous cane in his left hand, 
    holds a pick and shovel over his right shoulder"""),
  Card(GetFromBank(amount=10),
    """You have won second prize in a beauty contest - Collect $10""",
    """Mr. M preens with a sash and large bouquet"""),
  Card(GetFromBank(amount=100),
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
  Card(AdvanceTo(destionation=myPlace.resolve('GO')),
    "Advance to Go (Collect $200)",
    "Mr. M hops on both feet."),
  Card(AdvanceTo(destination=myPlace.resolve("Illinois Avenue")),
    "Advance to Illinois Ave. - If you pass Go, collect $200", # {Second sentence omitted.}
    """Mr. M has tied a cloth bundle onto his cane to make a bindle, 
    carried over his right shoulder, and is smoking a cigar"""),
  Card(AdvanceTo(destination=myPlace.resolve("St. Charles Place")),
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
  Card(GetFromBank(amount=50),
    "Bank pays you dividend of $50",
    """With his feet up on a telephone-bearing desk, 
    Mr. M leans back in an overstuffed chair, blowing cigar smoke rings"""),
  Card(GetJailFree(),
    """Get out of Jail Free - This card may be kept until needed, or traded/sold""",
    #{This card may be kept until needed or sold - Get Out of Jail Free} 
    #{The first sentence is much smaller than the second}
    "Mr. M, in close-fitting one-piece prison stripes, is literally kicked out"),
  Card(Retreat(amount=3),
    "Go back 3 spaces",
    "Mr. M is hauled back by a cane hooked around his neck"
    # {Presumably an allusion to amateur nights at theaters}
    ),
  Card(GoToJail(),
    "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
    "A truncheon-carrying policeman in a dark-colored uniform hauls a surprised Mr M along by the feet"),
  Card(Repair(house=25, hotel=100),
    """Make general repairs on all your property - For each house pay $25 - For each hotel $100 """,
    """Consulting a "How to Fix It" brochure, a hammer-wielding Mr. M 
    sits astride a house not much larger than he is; it buckles under his weight"""),
  Card(PayToBank(amount=15),
    "Pay poor tax of $15",
    "His trouser pockets pulled out to show them empty, Mr. M spreads his hands"
    #(The video game version replaces this with Speeding fine $15, reportedly also in the UK version.)
    ),
  Card(AdvanceTo(destination=myPlace.resolve('RR1')),
    """Take a trip to Reading Railroad {Take a ride on the Reading} - If you pass Go, collect $200""",
    "Mr. M rides astride the TOOTing engine of a train"),
  Card(AdvanceTo(destination=myPlace.resolve("Boardwalk")),
    """Take a walk on the Boardwalk - Advance token to Boardwalk""", # {Board Walk in both sentences} 
    """Mr. M, a smallish dog hung over one arm, with the other pushes a squalling baby in a small pram;
    behind them, birds fly in the sky above a low fence"""),
  Card(PayToAll(amount=50),
    """You have been elected Chairman of the Board - Pay each player $50""",
    """A newsboy shouts an Extra with Mr. M's headshot on its front page"""),
  Card(GetFromBank(amount=150),
    """Your building {and} loan matures - Collect $150""", # {Up until the 1980s a "building and loan" was a financial institution.} 
    """Mr. M joyfully embraces an apparent wife"""),
  Card(GetFromBank(amount=100),
    """You have won a crossword competition - Collect $100""", #{Not in the deck} 
    ""),
  ]


