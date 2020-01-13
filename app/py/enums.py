"""File containing enums"""
from enum import Enum
from collections import namedtuple

DifficultyLevel = namedtuple('DifficultyLevel', ['name', 'starting_credits', 'number'])

class Difficulty(Enum):
    """Enum for storing the difficulty of the game"""

    @property
    def nanme(self):
        """Returns the name of a difficulty"""
        return self.value.name

    @property
    def starting_credits(self):
        """Returns the starting credits of a difficulty"""
        return self.value.starting_credits

    @property
    def number(self):
        """Returns the number of a difficulty"""
        return self.value.number

    EASY = DifficultyLevel("Easy", 10000, 1)
    MEDIUM = DifficultyLevel("Medium", 500, 2)
    HARD = DifficultyLevel("Hard", 250, 3)

class TechLevel(Enum):
    """Enum for storing the techlevel of a region, market, or item"""
    Primitive = 1
    Agricultural = 2
    Industrial = 3
    Modern = 4
    Planetary = 5
    Interstellar = 6
    Galactic = 7

ShipType = namedtuple('ShipType', ['cargo_cap', 'fuel_cap', 'health_cap', 'speed'])

class ShipTypes(Enum):
    """Enum for storing different types of ships"""

    @property
    def cargo_cap(self):
        """Returns the capacity of a ship type"""
        return self.value.cargo_cap

    @property
    def fuel_cap(self):
        """Returns the fuel capacity of a ship type"""
        return self.value.fuel_cap

    @property
    def health_cap(self):
        """Returns the health capacity of a ship type"""
        return self.value.health_cap

    @property
    def speed(self):
        """Returns the speed of a ship type"""
        return self.value.speed

    Wren = ShipType(500, 20, 8, 20)
    Sparrow = ShipType(150, 30, 10, 20)
    Robin = ShipType(200, 30, 15, 25)
    Crow = ShipType(200, 40, 25, 25)
    Hawk = ShipType(250, 35, 50, 40)
    Falcon = ShipType(300, 45, 60, 45)
    Eagle = ShipType(400, 50, 70, 50)
    Albatross = ShipType(1000, 100, 60, 30)

ItemType = namedtuple('ItemType', ['name', 'slot', 'size', 'base_price',
                                   'base_count', 'tech_level'])

class ItemTypes(Enum):
    """Enum for storing different types of items"""

    @property
    def name(self):
        """Returns the name of an item type"""
        return self.value.name

    @property
    def slot(self):
        """Returns the slot number of an item type, items are numbered by their slot"""
        return self.value.slot

    @property
    def size(self):
        """Returns the size of an item type"""
        return self.value.size

    @property
    def price(self):
        """Returns the base price of an item type"""
        return self.value.base_price

    @property
    def count(self):
        """Returns the base count of an item type"""
        return self.value.base_count

    @property
    def tech_level(self):
        """Returns the tech level of an item type"""
        return self.value.tech_level

    Food = ItemType("Food", 0, 10, 10, 500, TechLevel.Primitive)
    Wood = ItemType("Wood", 1, 30, 25, 200, TechLevel.Primitive)
    Spices = ItemType("Spices", 2, 5, 50, 150, TechLevel.Agricultural)
    Gold = ItemType("Gold", 3, 5, 100, 50, TechLevel.Agricultural)
    Medicine = ItemType("Medicine", 4, 10, 100, 100, TechLevel.Industrial)
    Phone = ItemType("Phones", 5, 5, 200, 100, TechLevel.Industrial)
    Computer = ItemType("Computers", 6, 10, 500, 80, TechLevel.Modern)
    Ray_Gun = ItemType("Ray Guns", 7, 25, 1500, 50, TechLevel.Planetary)
    Nanobots = ItemType("Nanobots", 8, 10, 5000, 30, TechLevel.Interstellar)
    Dark_Matter = ItemType("Dark Matter", 9, 10, 10000, 20, TechLevel.Galactic)
    Special = ItemType("Special", 10, 100, 5, 0, TechLevel.Primitive)
