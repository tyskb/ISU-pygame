#item class
import random

class Item:
    def __init__(self, name, min_price, max_price):
        self.name = name
        self.min_price = min_price
        self.max_price = max_price
        self.price = random.randint(min_price, max_price)
    
        def __str__(self):
            return f"{self.name}: {self.price}"

class ItemsManager:
    def __init__(self):
        self.items = [
            Item("NFT", 500, 5000),
            Item("Bitcoin", 3000, 100000),
            Item("Bubble Tea", 3, 15),
            Item("GPU", 200, 3000),
            Item("PS5", 200, 1200),
            Item("Car", 3000, 90000),
            Item("Shoes", 40, 1000),
            Item("Watch", 50, 1000),
        ]

    def randomly_change_prices(self, num_items_to_change):
        items_to_update = random.sample(self.items, k=min(num_items_to_change, len(self.items)))

        for item in items_to_update:
            min_percentage_change, max_percentage_change = 5, 15
            percentage_change = random.randint(min_percentage_change, max_percentage_change) / 100
            new_price = max(item.min_price, min(item.max_price, round(item.price * (1 + percentage_change))))
            item.price = new_price

    def display_prices(self):
        updated_items = []
        for item in self.items:
            updated_items.append(f"{item.name} Price: {int(item.price)}")
        return updated_items
    

class PlayerInventory:
    def __init__(self, max_size, initial_money):
        self.max_size = max_size
        self.money = initial_money
        self.inventory = {}

    def buy_item(self, item, quantity):
        if len(self.inventory) + quantity > self.max_size:
            return False, "Not enough space in the inventory."

        total_cost = item.price * quantity
        if self.money >= total_cost:
            self.money -= total_cost

            # Update inventory dictionary
            if item in self.inventory:
                self.inventory[item] += quantity
            else:
                self.inventory[item] = quantity

            return True, f"Successfully bought {quantity} {item.name}(s) for {total_cost} money."
        else:
            return False, "Not enough money to buy the items."

    def sell_items(self, items, quantities):
        for item, quantity in zip(items, quantities):
            if item in self.inventory and self.inventory[item] >= quantity:
                # Remove items from inventory and add money to balance
                self.inventory[item] -= quantity
                selling_price = item.price * quantity
                self.money += selling_price
            else:
                return False, "Not enough items to sell or item not found in the inventory."

        return True, f"Successfully sold items for {selling_price} money."

    def get_inventory_info(self):
        inventory_info = []
        for item in self.inventory:
            inventory_info.append(item.name)
        return inventory_info

    def get_money(self):
        return self.money
    
    def get_inventory(self):
        return self.inventory

    def __str__(self):
        return f"Money: {self.money}, Inventory: {self.get_inventory_info()}"