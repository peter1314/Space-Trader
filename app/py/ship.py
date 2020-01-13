"""File for the Ship Class"""
from .inventory import Inventory

class Ship:
    """Ship represents the players ship, ships are created using the ShipType enum"""

    def __init__(self, type):
        """Creates a ship with a type, cargo capacity, fuel capacity, and health capacity using the ShipType enum"""
        self.type = type
        self.cargo_cap = type.cargo_cap
        #Cargo bay starts empty
        self.cargo = round(0.0, 2)
        self.fuel_cap = type.fuel_cap
        #Start fully fueled
        self.fuel = round(self.fuel_cap * 1.0, 2)
        self.health_cap = type.health_cap
        #Start at max health
        self.health = round(self.health_cap * 1.0, 2)
        self.speed = type.speed

    def remaining_space(self):
        """returns the remaining cargo space"""
        return self.cargo_cap - self.cargo

    def load_cargo(self, cargo):
        """Loads cargo if it can fit, returns if it can fit"""
        if self.cargo + cargo <= self.cargo_cap:
            self.cargo = round(self.cargo + cargo, 2)
            return True
        return False

    def use_fuel(self, fuel):
        """Uses fuel if fuel it has enough, returns if it has enough"""
        if self.fuel - fuel >= 0:
            self.fuel = round(self.fuel - fuel, 2)
            return True
        return False

    def has_fuel(self, fuel):
        """Returns if the ship has more fuel than fuel"""
        return fuel <= self.fuel

    def lose_health(self, health):
        """Loses health, returns if remaining health was greater than zero"""
        if self.health - health > 0:
            self.health = round(self.health - health, 2)
            return True
        self.health = 0
        return False

    def unload_cargo(self, cargo):
        """Unloads cargo unless it unloads an impossible amount, returns if added"""
        if self.cargo - cargo >= 0:
            self.cargo = round(self.cargo - cargo, 2)
            return True
        return False

    def refuel(self, fuel):
        """Adds fuel unless it adds an impossible amount, returns if added"""
        if self.fuel + fuel <= self.fuel_cap:
            self.fuel = round(self.fuel + fuel, 2)
            return True
        return False


    def repair(self, health):
        """Adds health unless it adds an impossible amount, returns if added"""
        if self.health + health <= self.health_cap:
            self.health = round(self.health + health, 2)
            return True
        return False

    def refuel_completely(self):
        """Sets fuel to max, returns amount of fuel added"""
        output = self.fuel_cap - self.fuel
        self.fuel = round(self.fuel_cap, 2)
        return output

    def repair_completely(self):
        """Sets health to max, returns amount of health added"""
        output = self.health_cap - self.health
        self.health = round(self.health_cap, 2)
        return output

    def to_dict(self):
        """Creates dictionary of ship"""
        holder = {}
        holder["type"] = self.type.name
        holder["cargo_cap"] = self.cargo_cap
        holder["cargo"] = self.cargo
        holder["fuel_cap"] = self.fuel_cap
        holder["fuel"] = self.fuel
        holder["health_cap"] = self.health_cap
        holder["health"] = self.health
        holder["speed"] = self.speed

        return holder
