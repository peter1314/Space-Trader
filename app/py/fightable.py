"""file for storing the Fightable ABC"""
from abc import abstractmethod
from .npc import NPC

class Fightable(NPC):
    """Describes a fightable NPC"""

    @abstractmethod
    def give_fight_reward(self, player):
        """Gives a reward to the player if they win the fight"""

    @abstractmethod
    def give_fight_punishment(self, player):
        """Determines what happens if the player fails to flee"""

    @abstractmethod
    def fight(self, player):
        """Determines if the player wins or loses the fight."""
