"""File for the Market Class"""
# import random
from random import randint
from .inventory import Inventory
from .enums import ItemTypes
from .enums import TechLevel

class Market:
    """The market class has inventory, rates for those items, and controls and changes in either"""

    def __init__(self, tech_level):
        """Creates a market with a specified tech level"""
        self.inventory = Inventory()
        self.tech_level = TechLevel(tech_level)
        self.price_list = [None] * 11

        #Initializes items and prices
        self.generate_items()
        self.generate_prices()

    def update(self):
        """Updates items and prices"""
        self.drift_items()
        self.drift_prices()

    def generate_prices(self):
        """Sets intial prices"""
        for i in range(11):
            #Prices are stored as a percentage of base price
            self.price_list[i] = randint(70, 130)


    def generate_items(self):
        """Sets intialial item counts"""
        for data in ItemTypes:
            #Sets items if they are within tech level of market, otherwise stay at default of 0
            if data.tech_level.value <= self.tech_level.value:
                #Sets counts to random percentage of base count, unlike prices stores actual values
                count = round(randint(70, 130) * self.inventory.get_item_base_count(data) / 100)
                self.inventory.set_item(data, count)

    def drift_prices(self):
        """Causes prices to drift a percentage, however they will drift on average towards 100%"""
        for i in range(10):
            adjust = (self.price_list[i] - 100) / 4
            min_factor = round(90 - adjust)
            max_factor = round(110 - adjust)

            self.price_list[i] = self.price_list[i] * randint(min_factor, max_factor) / 100

    def drift_items(self):
        """item counts drift a percentage, they will drift on avg towards their base count"""
        for data in ItemTypes:
            #Will drift if the item is within the tech level of the market, otherwise sets it to 0
            if data.tech_level.value <= self.tech_level.value:
                #item counts can't drift back from 0, puts a hard but random floor on item counts
                item_base_count = self.inventory.get_item_base_count(data)
                if item_base_count != 0:
                    item_count = max(self.get_item_count(data), self.inventory.get_item_base_count(data) / 5)
                    factor = (item_count * 100 / item_base_count)
                    adjust = (factor - 100) / 4
                    min_factor = round(90 - adjust)
                    max_factor = round(110 - adjust)
                    new_value = item_count * randint(min_factor, max_factor) / 100
                    self.inventory.set_item(data, round(new_value))
                
            else:
                self.inventory.set_item(data, 0)

    def add_item(self, item, count):
        """Adds a specified number of a specified item to the market"""
        self.inventory.add_item(item, count)

    def remove_item(self, item, count):
        """Removes a specified number of a specified item from the market"""
        self.inventory.remove_item(item, count)

    def get_item_count(self, item):
        """Gets the number of a specified item in the market"""
        return self.inventory.get_item_count(item)

    def get_slot_count(self, slot):
        """Gets the number of a specified item in the market based
        on the slot of that item, useful for iteration"""
        return self.inventory.get_slot_count(slot)

    def get_item_price(self, item):
        """Gets the price of a specified item"""
        item_price = self.price_list[item.slot]
        item_base_price = self.inventory.get_item_base_price(item)

        #If the item is above the markets tech level, its price is marked up 50 percent
        if item.tech_level.value > self.tech_level.value:
            item_price *= 1.5
        return round(item_price * item_base_price / 100)

    def get_slot_price(self, slot):
        """Gets the price of a specified item based on
        the slot of that item, useful for iteration"""
        slot_price = self.price_list[slot]
        slot_base_price = self.inventory.get_slot_base_price(slot)

        #If the item is above the markets tech level, its price is marked up 50 percent
        if self.inventory.types[slot].tech_level.value > self.tech_level.value:
            slot_price *= 1.5
        return round(slot_price * slot_base_price / 100)


    def get_item_buy_price(self, item, merchant_skill):
        """Gets the buy price of a specified item"""

        #If the market does not have the item, return 0
        if self.get_item_count(item) == 0:
            return 0

        #Items are marked up when you are buying, this markup is reduced by the merchant skill
        markup = 64 / (48 + merchant_skill)

        return round(self.get_item_price(item) * markup)

    def get_slot_buy_price(self, slot, merchant_skill):
        """Gets the buy price of a specified item based on
        the slot of that item, useful for iteration"""

        #If the market does not have the item return 0
        if self.get_slot_count(slot) == 0:
            return 0

        #Items are marked up when you are buying, this markup is reduced by the merchant skill
        markup = 64 / (48 + merchant_skill)

        return round(self.get_slot_price(slot) * markup)

    def to_dict(self, merchant_skill):
        """Creates dictionary of market"""
        holder = {}
        holder["techLevel"] = {"value":self.tech_level.value, "name":self.tech_level.name}
        holder["inventory"] = self.inventory.to_dict()
        holder["prices"] = self.prices_to_dict(merchant_skill)
        return holder

    def prices_to_dict(self, merchant_skill):
        """Creates dictionary of buy and sell prices"""
        holder = {}
        for i in range(11):
            holder["price" + str(i)] = self.get_slot_price(i)
            holder["buy_price" + str(i)] = self.get_slot_buy_price(i, merchant_skill)
        return holder
