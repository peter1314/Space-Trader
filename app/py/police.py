"""File for storing the Police class"""
from random import randint
from .fightable import Fightable
from .fleable import Fleable
from .forfeitable import Forfeitable

class Police(Fightable, Fleable, Forfeitable):
    """The police npc"""

    def __init__(self, target_region, target_fuel_cost):
        self.name = "Police"
        self.id = 2
        self.stolen_item = None
        self.target_region = target_region
        self.target_fuel_cost = target_fuel_cost
        self.over = False
        self.outcome = ""

    def can_encounter(self, player):
        """decides if a player can encounter this npc"""
        self.stolen_item = player.get_random_item()
        return self.stolen_item is not None

    def give_flea_reward(self, player):
        """handles the flee reward"""
        player.ship.use_fuel(self.target_fuel_cost)
        self.outcome = "You escaped the Police!"

    def give_fight_reward(self, player):
        """handles the rewards"""
        player.move_to_region(self.target_region, self.target_fuel_cost)
        self.outcome = "You outgunned the Police!"

    def give_forfeit_punishment(self, player):
        """Determines what happens if player forfeits"""
        player.move_to_region(self.target_region, self.target_fuel_cost)
        player.remove_item(self.stolen_item, player.get_item_count(self.stolen_item))
        self.outcome = "You have turned over your " + self.stolen_item.name.lower()

    def give_flea_punishment(self, player):
        """Determines what happens if the player fails to flee"""
        player.ship.use_fuel(self.target_fuel_cost)
        player.remove_item(self.stolen_item, player.get_item_count(self.stolen_item))
        player.ship.lose_health(2.5)
        player.spend_credits(250)
        self.outcome = "The Police caught you!"


    def give_fight_punishment(self, player):
        """Determines what happens if the player fails to fight"""
        player.ship.use_fuel(self.target_fuel_cost)
        player.remove_item(self.stolen_item, player.get_item_count(self.stolen_item))
        player.ship.lose_health(5)
        player.spend_credits(250)
        self.outcome = "The Police outgunned you!"


    def fight(self, player):
        """Determines how fight goes"""
        self.over = True
        roll = player.fighter_skill + randint(0, 17)
        player.lower_karma()
        if roll >= 17:
            self.give_fight_reward(player)
            return True
        self.give_fight_punishment(player)
        return False

    def flee(self, player):
        """Determines how fleeing goes"""
        player.lower_karma()
        self.over = True
        roll = player.pilot_skill + randint(0, 17)
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
        """Creates a dictionary representation of this object"""
        holder = {}
        holder["name"] = self.name
        holder["id"] = self.id
        holder["over"] = self.over
        holder["outcome"] = self.outcome
        holder["stolen_item"] = self.stolen_item.name.lower()
        return holder
