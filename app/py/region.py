"""File for the Region class"""
import math
from random import randint
from .coordinate import Coordinate
from .enums import TechLevel
from .inventory import Inventory
from .market import Market

class Region:
    """Region represents a planet, it has a name, location, tech level, and market"""
    
    def __init__(self, name, tech_level, xray, yankee):
        """Creates a region with specified attributes"""
        self.name = name
        self.coordinate = Coordinate(xray, yankee)
        self.tech_level = TechLevel(tech_level)
        self.market = Market(TechLevel(tech_level))

    @classmethod
    def random(cls, name):
        """Creates a region with a specified name but random attributes"""
        xray = randint(-400, 400)
        yankee = randint(-200, 200)
        tech_level = TechLevel(randint(1, 7))
        return cls(name, tech_level, xray, yankee)

    def calc_distance(self, other):
        """Calculates the distance between this region and another"""
        return self.coordinate.distance_to(other.coordinate)

    def calc_fuel_cost(self, other, pilot_skill):
        """Calculates the cost to travel between this region and another"""
        #Discounts fuel cost based on pilot skill
        pilot_discount = (16.0 / (16 + pilot_skill)) / 7
        return self.calc_distance(other) * pilot_discount

    def to_dict(self, curr_reg, pilot_skill, merchant_skill):
        """Creates dictionary of region"""
        holder = {}
        holder["name"] = self.name
        holder["coordinate"] = self.coordinate.__dict__
        holder["techLevel"] = {"value":self.tech_level.value, "name":self.tech_level.name}
        holder["distance"] = self.calc_distance(curr_reg)
        holder["fuel_cost"] = self.calc_fuel_cost(curr_reg, pilot_skill)
        holder["market"] = self.market.to_dict(merchant_skill)

        return holder
