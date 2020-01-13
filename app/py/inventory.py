"""File for Inventory Class"""
from .enums import ItemTypes

class Inventory:
    """Inventory holds dictory of item counts where key is the item type and value is the count"""

    def __init__(self):
        """Creates an inventory and sets all item counts to 0"""
        self.items = {}
        #types is for retrieving the item enum associated with a slot
        self.types = {}
        #total_count holds total number of item
        self.total_count = 0
        for data in ItemTypes:
            self.types[data.slot] = data
            self.items[data.slot] = 0

    def set_item(self, item, count):
        """Sets count of a specified item in the inventory"""
        self.total_count += (count - self.items[item.slot])
        self.items[item.slot] = count

    def add_item(self, item, count):
        """Adds a specified number of a specified item to the inventory"""
        self.total_count += count
        self.items[item.slot] = self.items[item.slot] + count

    def remove_item(self, item, count):
        """Removes a specified number of a specified item from inventory and returns if possible"""
        if self.items[item.slot] >= count:
            self.items[item.slot] = self.items[item.slot] - count
            return True
        return False

    def get_item_count(self, item):
        """Returns count of a specified item"""
        return self.items[item.slot]

    def get_slot_count(self, slot):
        """Returns count of a specified item based on the slot of the item, useful for iteration"""
        return self.items[slot]

    def get_item_base_price(self, item):
        """Returns the base price of an item"""
        return item.price

    def get_slot_base_price(self, slot):
        """Returns the base price of an item based on the slot of the item, useful for iteration"""
        return self.types[slot].price

    def get_item_base_count(self, item):
        """Returns the base count of an item"""
        return item.count

    def get_slot_base_count(self, slot):
        """Returns the base count of an item based on the slot of the item, useful for iteration"""
        return self.types[slot].count

    def clear(self):
        """Empties inventory"""
        for data in ItemTypes:
            self.items[data.slot] = 0

    def to_dict(self):
        """Creates dictionary of inventory"""
        holder = {}
        for item in ItemTypes:
            holder["item" + str(item.slot)] = self.item_to_dict(item, self.get_item_count(item))
        return holder

    def item_to_dict(self, item, count):
        """Creates dictionary of item"""
        holder = {}
        holder["name"] = item.name
        holder["slot"] = item.slot
        holder["size"] = item.size
        holder["base_price"] = item.price
        holder["base_count"] = item.count
        holder["count"] = count
        return holder
