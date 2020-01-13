"""file for storing the forfeitable ABC"""
from abc import abstractmethod
from .npc import NPC

class Forfeitable(NPC):
    """Describes a forfeitable NPC"""

    @abstractmethod
    def forfeit(self, player):
        """Handles what happens when the player forfeits"""

    @abstractmethod
    def give_forfeit_punishment(self, player):
        """Hurts the player if they lose the fight"""
