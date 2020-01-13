"""File for storing the haggleable ABC"""
from abc import abstractmethod
from .npc import NPC

class Haggleable(NPC):

    @abstractmethod
    def haggle(self, player):
        """Haggling with trader"""

    @abstractmethod
    def haggle_punishment(self, player):
        """Punishment for haggling with trader"""

    @abstractmethod
    def haggle_reward(self, player):
        """Reward for successfullying haggling with trader"""
