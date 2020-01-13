"""File for storing the Ship class"""
import random
import math
from .ship import Ship
from .enums import ShipTypes
from .enums import ItemTypes
from .enums import Difficulty
from .inventory import Inventory
from .police import Police
from .bandit import Bandit
from .trader import Trader
from random import randint

class Player:
    """The player class represents the player and stores a name, the players skills, credits, and their ship"""

    def __init__(self, name, pilot, fighter, merchant, engineer, difficultyNum):
        """Creates a player given a name, skills, and difficulty"""
        self.name = name
        self.pilot_skill = int(pilot)
        self.fighter_skill = int(fighter)
        self.merchant_skill = int(merchant)
        self.engineer_skill = int(engineer)

        #Sets difficulty
        if int(difficultyNum) == 1:
            self.difficulty = Difficulty.EASY
        elif int(difficultyNum) == 2:
            self.difficulty = Difficulty.MEDIUM
        else:
            self.difficulty = Difficulty.HARD

        self.credits = self.difficulty.starting_credits

        #Defaults the players region to none, their ship to the Wren,
        #and gives them a new empty inventory
        self.region = None
        self.ship = Ship(ShipTypes.Wren)
        self.inventory = Inventory()

        #NPC starts at 0, which is no npc, 1 is bandit, 2 police, 3 trader
        self.currentNPC = None
        # Players start off with .5 karma by default. This is nuetral
        self.karma = .50

    @classmethod
    def create_player_from_form(cls, form):
        """Creates a player from a form"""
        return cls(form["name"],
                   form["pilotSkills"],
                   form["fighterSkills"],
                   form["merchantSkills"],
                   form["engSkills"],
                   form["difficultyNum"])

    def set_region(self, region):
        """Sets the players region to a specified region"""
        self.region = region

    def lower_karma(self):
        """Lowers karma by 10%"""
        self.karma *= .9

    def raise_karma(self):
        """Raises karma by 10%"""
        self.karma *= 1.1

    def get_karma(self):
        return self.karma

    def move_to_region(self, region, fuel_cost):
        """Moves the player to a specified region using a specified amount of fuel"""
        if self.ship.has_fuel(fuel_cost):
            self.ship.use_fuel(fuel_cost)
            self.region = region

    def check_encounter(self, region, fuel_cost):
        """Where encounter logic happens and determines if player should travel"""

        #rolls a number 1 through 100
        roll = randint(1, 100)

        #if roll is less than 10, 20, or 30 depending on difficulty, causes a bad encounter
        #the roll also takes into account karma. Worse karma means you are more likely to have
        #a bad encounter
        if roll <= (self.difficulty.number * 10) * (.5 + self.karma):
            #negative npc have equal odds
            randNPC = randint(1, 2)
            if randNPC == 1:
                self.currentNPC = Bandit(region, fuel_cost)

                if not self.currentNPC.can_encounter(self):
                    self.currentNPC = None
            else:
                self.currentNPC = Police(region, fuel_cost)
                #player is spared from police if they have no items
                if not self.currentNPC.can_encounter(self):
                    self.currentNPC = None
        #if roll is higher than 80, causes good encounter
        elif roll * (.5 + self.karma) >= 80:
            self.currentNPC = Trader(region, fuel_cost)
            #
            if not self.currentNPC.can_encounter(self):
                    self.currentNPC = None
        #otherwise there is no encounter
        else:
            self.currentNPC = None

        #return if there is an npc
        return self.currentNPC is not None

    def refuel(self):
        """Refuels player's the ship"""
        #TEMPORARY
        fuel_rate = 1

        fuel_amount = self.ship.fuel_cap - self.ship.fuel
        fuel_cost = fuel_amount * fuel_rate

        #If the player cannot afford a full refuel, refuel as much as possible
        if fuel_cost > self.credits:
            fuel_cost = self.credits
            fuel_amount = fuel_cost / fuel_rate

        self.ship.refuel(fuel_amount)
        self.spend_credits(fuel_cost)

    def repair(self):
        """Repairs the player's ship"""
        #TEMPORARY
        repair_rate = 5

        repair_amount = self.ship.health_cap - self.ship.health
        repair_cost = repair_amount * repair_rate * 17 / (self.engineer_skill +  1)

        #If the player cannot affod a full repair, repair as much as possible
        if repair_cost > self.credits:
            repair_cost = self.credits
            repair_amount = repair_cost / repair_rate

        self.ship.repair(repair_amount)
        self.spend_credits(repair_cost)

    def spend_credits(self, credits):
        """Reduces player's credits buy a specified amount, returns if the player was able to pay"""
        if(self.credits >= credits):
            self.credits = round((self.credits - credits))
            return True
        self.credits = 0
        return False

    def add_credits(self, credits):
        """Increases player's credits buy a specified amount"""
        self.credits = round((self.credits + credits))

    def get_credits(self):
        """Returns players credits"""
        return self.credits

    def add_item(self, item, count):
        """Adds a specified number of a specified item to the player's inventory"""
        if self.ship.load_cargo(item.size * count):
            self.inventory.add_item(item, count)

    def add_item_max(self, item, count):
        """Adds a specified number or as many as can fit of a specified item to the player's inventory"""
        fitCount = math.floor(self.ship.remaining_space() / item.size)
        newCount = min(count, fitCount)

        if self.ship.load_cargo(item.size * newCount):
            self.inventory.add_item(item, newCount)

    def remove_item(self, item, count):
        """Removes a specified number of a specified item from the player's inventory"""
        if self.inventory.remove_item(item, count):
            self.ship.unload_cargo(item.size * count)

    def get_item_count(self, item):
        """Returns the count of a specified item in the player's inventory"""
        return self.inventory.get_item_count(item)

    def get_slot_count(self, slot):
        """Returns the count of a specified item in the player's inventory based on the item's slot, useful for iteration"""
        return self.inventory.get_slot_count(slot)

    def get_random_item(self):
        """Returns a random item type that the player has at least one of"""
        if(self.ship.cargo > 0):

            rand_type = random.choice(list(ItemTypes))
            while (self.get_item_count(rand_type) == 0):
                rand_type = random.choice(list(ItemTypes))

            return rand_type
        return None

    def has_items(self):
        if (self.ship.cargo > 0):
            return True
        return False

    def clear_inventory(self):
        self.inventory.clear()
        self.ship.cargo = 0

    def to_dict(self):
        """Creates dictionary of player"""
        holder = {}
        holder["name"] = self.name
        holder["pilot_skill"] = self.pilot_skill
        holder["fighter_skill"] = self.fighter_skill
        holder["merchant_skill"] = self.merchant_skill
        holder["engineer_skill"] = self.engineer_skill
        holder["difficulty"] = self.difficulty.name
        holder["credits"] = self.credits
        holder["ship"] = self.ship.to_dict()
        holder["inventory"] = self.inventory.to_dict()

        return holder
