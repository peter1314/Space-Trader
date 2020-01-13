"""file contaning the NPC ABC"""
from abc import ABC, abstractmethod

class NPC(ABC):
    """Describes an NPC"""

    @abstractmethod
    def can_encounter(self, player):
        """decides if a player can encounter this npc"""
