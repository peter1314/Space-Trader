"""File for the Universe Class"""
from random import randint
from .region import Region
from .enums import ItemTypes

class Universe:
    """The Universe class generates and stores all of the games regions"""
    shared = None

    def __init__(self, region_names):
        """Given region names, creates a universe where each region is randomly generated"""
        if Universe.shared is None:
            Universe.shared = self
        else:
            raise Exception("The Universe class is a singleton!")
        self.region_names = region_names
        self.regions = {}
        self.region_count = 0

        for name in region_names:
            region = Region.random(name)
            #Region must be valid, otherwise it will regenerate
            while not self.valid_region(region):
                region = Region.random(name)
            self.regions[name] = region
            self.region_count += 1


    def get_random_region(self):
        """Returns a random region"""
        rand = randint(0, self.region_count - 1)
        return self.regions[self.region_names[rand]]

    def valid_region(self, new_region):
        """Checks if a region is valid"""
        for _, region in self.regions.items():
            #Region cannot be closer than 10 units to any other region
            if new_region.calc_distance(region) < 25:
                return False
        return True

    def to_dict(self, curr_reg, pilot_skill, merchant_skill):
        """Creates dictionary of this universe"""
        holder = {}
        for reg_name, reg in self.regions.items():
            holder[reg_name] = reg.to_dict(curr_reg, pilot_skill, merchant_skill)
        return holder
