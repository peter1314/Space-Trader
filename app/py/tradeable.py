"""fiel for storing the Tradeable ABC"""
from abc import abstractmethod
from .npc import NPC

class Tradeable(NPC):

    @abstractmethod
    def trade(self, player):
        '''Trades items'''
