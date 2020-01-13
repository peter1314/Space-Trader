"""File for storing the Bandit class"""
# import random
from random import randint
from .fightable import Fightable
from .fleable import Fleable
from .forfeitable import Forfeitable

class Bandit(Fightable, Fleable, Forfeitable):
    """The bandit npc"""

    def __init__(self, target_region, target_fuel_cost):
        self.name = "Bandit"
        self.id = 1
        self.demand = None
        self.credit_demand = None
        self.demand_code = None
        self.target_region = target_region
        self.target_fuel_cost = target_fuel_cost
        self.over = False
        self.outcome = ""

    def set_demand(self, player):
        #karma now influences how much a bandit asks for
        self.credit_demand = randint(50, 300) * (.5 + player.get_karma())

    def can_encounter(self, player):
        """decides if a player can encounter this npc, sets demand"""
        self.set_demand(player)
        if player.get_credits() >= self.credit_demand:
            self.demand = "Give me " + str(self.credit_demand) + " credits and nobody gets hurt!"
            self.demand_code = 0
        elif player.ship.cargo > 0:
            self.demand = "Give me your items and noboy gets hurt!"
            self.demand_code = 1
        else:
            self.demand = "You're hiding something, I'll blast you to bits to find it!"
            self.demand_code = 2

        return True

    def give_flea_reward(self, player):
        """handles the flee reward"""
        player.ship.use_fuel(self.target_fuel_cost)
        self.outcome = "You escaped the bandit!"

    def give_fight_reward(self, player):
        """handles the fight reward"""
        player.move_to_region(self.target_region, self.target_fuel_cost)
        player.add_credits(self.credit_demand / 2)
        self.outcome = "You outgunned the bandit, and took his credits!"

    def give_forfeit_punishment(self, player):
        """hurts the player"""
        player.move_to_region(self.target_region, self.target_fuel_cost)
        if self.demand_code == 0:
            player.spend_credits(self.credit_demand)
            self.outcome = "You gave the bandit " + str(self.credit_demand) + " credits!"
        elif self.demand_code == 1:
            player.clear_inventory()
            self.outcome = "The bandit took all your items!"
        else:
            player.ship.lose_health(10)
            self.outcome = "The bandit damaged your ship!"

    def give_flea_punishment(self, player):
        """Determines what happens if the player fails to flee"""
        player.ship.use_fuel(self.target_fuel_cost)
        player.ship.lose_health(2.5)
        player.spend_credits(player.get_credits())
        self.outcome = "The Bandit caught you and took your credits!"

    def give_fight_punishment(self, player):
        """Determines what happens if the player fails to fight"""
        player.ship.use_fuel(self.target_fuel_cost)
        player.ship.lose_health(5)
        player.spend_credits(player.get_credits())
        self.outcome = "The Bandit outgunned you and took your credits!"


    def fight(self, player):
        """Determines how fight goes"""
        self.over = True
        roll = player.fighter_skill + randint(0, 17)
        #Lowering the karma if you fight
        player.lower_karma();
        if roll >= 17:
            self.give_fight_reward(player)
            return True
        self.give_fight_punishment(player)
        return False

    def flee(self, player):
        """Determines how fleeing goes"""
        self.over = True
        roll = player.pilot_skill + randint(0, 17) * (.5 + player.get_karma())
        if roll >= 17:
            self.give_flea_reward(player)
            return True
        self.give_flea_punishment(player)
        return False

    def forfeit(self, player):
        """Handles what happens when the player forfeits"""
        self.over = True
        self.give_forfeit_punishment(player)
        return True

    def to_dict(self):
        """Returns a dictionary representation of this object"""
        holder = {}
        holder["name"] = self.name
        holder["id"] = self.id
        holder["over"] = self.over
        holder["outcome"] = self.outcome
        holder["demand"] = self.demand
        return holder
