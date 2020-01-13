"""File for storing the Game class"""
from .universe import Universe
from .enums import Difficulty
from .enums import ItemTypes

class Game:
    """The Game class holds the main elements of the game"""
    def __init__(self, player):
        """Creates a game based on a player"""
        self.difficulty = Difficulty(player.difficulty)
        self.player = player
        self.universe = None

    def start_game(self):
        """Initializes a game"""
        #Add or remove regions from the game here
        region_names = ["Lintford Harbor",
                        "New Opland",
                        "Nixa",
                        "Port Vi",
                        "Kernium",
                        "Chromland",
                        "Remroot",
                        "Termica",
                        "Port Macs",
                        "Vetto",
                        "Wultway",
                        "Lati",
                        "Rookram",
                        "Bontuk",
                        "Threnica",
                        "Artunum",
                        "Ximai",
                        "Celtor",
                        "Suri",
                        "Hulfast"]
        Universe.shared = None
        self.universe = Universe(region_names)
        self.player.set_region(self.universe.get_random_region())
        self.player.region.market.add_item(ItemTypes.Special, 1)

    def get_game(self):
        """Returns self"""
        return self
