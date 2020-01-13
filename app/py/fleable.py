"""file for storing the Fleable ABC"""
from abc import abstractmethod
from .npc import NPC

class Fleable(NPC):
    """Defines an NPC that can flea"""

    @abstractmethod
    def give_flea_reward(self, player):
        """Gives a reward to a player if the escape"""

    @abstractmethod
    def give_flea_punishment(self, player):
        """Hurts the player if they don't flee successfully"""

    @abstractmethod
    def flee(self, player):
        """Allows the player to try and flea. This method should return true if player is"""
