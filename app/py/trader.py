"""File for storing the Trader class"""

from random import randint
import random
from .fightable import Fightable
from .forfeitable import Forfeitable
from .tradeable import Tradeable
from .haggleable import Haggleable
from .enums import ItemTypes

class Trader(Fightable, Forfeitable, Tradeable, Haggleable):
    """The trader npc"""

    def __init__(self, target_region, target_fuel_cost):
        self.name = "Trader"
        self.id = 3
        self.selling_item = None
        self.selling_item_price = 0
        self.selling_item_count = 0
        self.target_region = target_region
        self.target_fuel_cost = target_fuel_cost
        self.over = False
        self.has_haggled = False
        self.outcome = ""

    def can_encounter(self, player):
        self.selling_item = random.choice(list(ItemTypes))
        while self.selling_item.slot == 10:
            self.selling_item = random.choice(list(ItemTypes))
        self.selling_item_price = round(self.selling_item.price * randint(60, 140) / 100) + 1
        self.selling_item_count = round(self.selling_item.count * randint(1, 5) / 100) + 1
        self.selling_item_price *= (.5 + player.get_karma())
        return True

    def give_forfeit_punishment(self, player):
        """Determines what happens if player ignores the trader"""
        player.move_to_region(self.target_region, self.target_fuel_cost)
        self.outcome = "You have ignored the trader."

    # robbing
    def give_fight_reward(self, player):
        """handles the fight reward"""
        player.move_to_region(self.target_region, self.target_fuel_cost)
        player.add_item_max(self.selling_item, self.selling_item_count)
        self.outcome = "You outgunned the trader, and took his items!"

    def give_fight_punishment(self, player):
        """Determines what happens if the player fails to fight"""
        player.ship.use_fuel(self.target_fuel_cost)
        player.ship.lose_health(5)
        self.outcome = "The Trader outgunned you and damaged your ship!"

    def forfeit(self, player):
        """Handles what happens when the player ignores the trader"""
        self.over = True
        self.give_forfeit_punishment(player)
        return True

    def trade(self, player):
        """Handles what happens when the player trades with the trader"""
        self.over = True
        player.move_to_region(self.target_region, self.target_fuel_cost)
        #buying things from trader raises karma becaues it helps economy
        player.raise_karma();
        if player.credits >= self.selling_item_price * self.selling_item_count:
            player.spend_credits(self.selling_item_price * self.selling_item_count)
            player.add_item(self.selling_item, self.selling_item_count)
            self.outcome = ("You have bought "
                            + str(self.selling_item_count) + " "
                            + str(self.selling_item.name.lower()))
            return True
        return False

    def fight(self, player):
        """Determines how fight goes"""
        self.over = True
        player.lower_karma();
        roll = player.fighter_skill + randint(0, 17)
        if roll >= 17:
            self.give_fight_reward(player)
            return True
        self.give_fight_punishment(player)
        return False

    # haggling
    def haggle(self, player):
        """Haggling with trader"""
        if not self.has_haggled:
            self.has_haggled = True
            roll = player.merchant_skill + randint(0, 17)
            if roll >= 17:
                self.haggle_reward(player)
                return True
            self.haggle_punishment(player)
            return False
        return False

    def haggle_punishment(self, player):
        """Reward for successfullying haggling with trader"""
        #being bad at haggling lowers your karma b/c you were probably rude
        player.lower_karma();
        self.selling_item_price = round(self.selling_item_price * randint(110, 135) / 100)

    def haggle_reward(self, player):
        """Reward for successfullying haggling with trader"""
        self.selling_item_price = round(self.selling_item_price * randint(65, 90) / 100)

    def to_dict(self):
        """Creates a dictionary representation of this object"""
        holder = {}
        holder["name"] = self.name
        holder["id"] = self.id
        holder["over"] = self.over
        holder["outcome"] = self.outcome
        holder["selling_item"] = self.selling_item.name
        holder["selling_item_price"] = (self.selling_item_price * self.selling_item_count)
        holder["selling_item_count"] = self.selling_item_count
        holder["selling_item_cargo"] = (self.selling_item.size * self.selling_item_count)

        return holder
