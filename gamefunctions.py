#gamefunctions.py
#Haley Burley
#2/16/25

"""
gamefunctions.py

This module provides functions for an adventure-style game, including printing a welcome message,
displaying a shop menu, processing item purchases, and generating random monsters.

Functions:
- print_welcome(name): Prints a welcome message.
- print_shop_menu(item1Name, item1Price, item2Name, item2Price): Displays a formatted shop menu.
- purchase_item(itemPrice, startingMoney, quantityToPurchase): Calculates how many items can be bought.
- new_random_monster(): Generates a random monster with attributes.
"""

import random

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1) -> tuple:
    """
    Calculates how many items can be purchased and the remaining money.

    Args:
        itemPrice (float): Price of a single item.
        startingMoney (float): The total amount of money available.
        quantityToPurchase (int, optional): Number of items player wants to buy. Defaults to 1.

    Returns:
        tuple: (Number of items purchased, Remaining money)
    """
    total_cost = itemPrice * quantityToPurchase
    if total_cost <= startingMoney:
        return quantityToPurchase, startingMoney - total_cost
    else:
        max_purchasable = int(startingMoney // itemPrice)
        return max_purchasable, startingMoney - (max_purchasable * itemPrice)

def visit_shop(player_gold, inventory):
    items_for_sale = [
        {"name": "sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10, "price": 10},
        {"name": "holy hand grenade", "type": "consumable", "note": "defeats monster", "price": 12}
    ]

    print("\nWelcome to the shop!")
    for i, item in enumerate(items_for_sale, 1):
        print(f"{i}) {item['name'].title()} - {item['price']} gold")

    print(f"{len(items_for_sale)+1}) Leave shop")
    choice = input("Enter your choice: ")

    if not choice.isdigit() or int(choice) not in range(1, len(items_for_sale)+2):
        print("Invalid choice.")
        return player_gold, inventory

    if int(choice) == len(items_for_sale) + 1:
        return player_gold, inventory

    selected_item = items_for_sale[int(choice)-1]
    if player_gold >= selected_item["price"]:
        inventory.append(selected_item.copy())
        player_gold -= selected_item["price"]
        print(f"You bought a {selected_item['name']}!")
    else:
        print("Not enough gold!")

    return player_gold, inventory

def equip_item(inventory, item_type):
    relevant_items = [item for item in inventory if item["type"] == item_type]
    if not relevant_items:
        print(f"No {item_type}s available to equip.")
        return None

    print(f"Choose a {item_type} to equip:")
    for i, item in enumerate(relevant_items, 1):
        print(f"{i}) {item['name'].title()}")

    choice = input("Enter number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(relevant_items):
        selected = relevant_items[int(choice)-1]
        print(f"You have equipped {selected['name']}!")
        return selected
    else:
        print("Invalid choice.")
        return None

def new_random_monster() -> dict:
    """
    Generates a random monster with a name, description, health, power, and money.

    Returns:
        dict: A dictionary containing monster attributes.
    """
    monsters = [
        {
            "name": "Pixie",
            "description": "You find a sparkling little creature buzzing around. When it notices you, it rushes at you quickly with a sharp dagger.",
            "health": random.randint(10, 20),
            "power": random.randint(5, 10),
            "money": round(random.uniform(1, 15), 2),
        },
        {
            "name": "Frog",
            "description": "You discover a frog licking its lips as it looks you over.",
            "health": random.randint(5, 15),
            "power": random.randint(2, 7),
            "money": round(random.uniform(1, 10), 2),
        },
        {
            "name": "Vampire",
            "description": "A shadowy figure jumps out at you from behind a tree.",
            "health": random.randint(30, 50),
            "power": random.randint(10, 20),
            "money": round(random.uniform(5, 30), 2),
        }
    ]

    return random.choice(monsters)

def print_welcome(name: str) -> None:
    """
    Prints a welcome message centered within 20 characters.

    Args:
        name (str): The name of the player.

    Returns:
        None

    Example:
        >>> print_welcome("Alice")
        Hello, Alice!   
    """
    print(f"{'Hello, ' + name + '!':^20}")

def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """
    Prints a shop sign with menu items and prices.

    Args:
        item1Name (str): Name of the first item.
        item1Price (float): Price of the first item.
        item2Name (str): Name of the second item.
        item2Price (float): Price of the second item.

    Returns:
        None
    """
    content1 = f"{item1Name:<12} ${item1Price:.2f}"
    content2 = f"{item2Name:<12} ${item2Price:.2f}"
    content_width = max(len(content1), len(content2))

    line1 = f"| {content1:<{content_width}} |"
    line2 = f"| {content2:<{content_width}} |"

    border = f"/{'-' * (len(line1) - 2)}\\"
    bottom = f"\\{'-' * (len(line1) - 2)}/"

    print(border)
    print(line1)
    print(line2)
    print(bottom)

if __name__ == "__main__":
    print("Testing purchase_item function:")
    test_cases = [
        (1.23, 10, 3),
        (1.23, 2.01, 3),
        (3.41, 21.12, 1),
        (31.41, 21.12, 1),
        (5.00, 50.00, 12)
    ]
    
    for price, money, qty in test_cases:
        num_purchased, leftover_money = purchase_item(price, money, qty)
        print(f"Purchased: {num_purchased}, Money Left: ${leftover_money:.2f}")

    print("\nTesting default quantity parameter:")
    num_purchased, leftover_money = purchase_item(2.50, 10)
    print(f"Purchased: {num_purchased}, Money Left: ${leftover_money:.2f}")

    print("\nTesting new_random_monster function:")
    for _ in range(3):
        monster = new_random_monster()
        print(f"Name: {monster['name']}")
        print(f"Description: {monster['description']}")
        print(f"Health: {monster['health']}")
        print(f"Power: {monster['power']}")
        print(f"Money: ${monster['money']:.2f}\n")

    print("\nTesting print_welcome function:")
    print_welcome("Haley")
    print_welcome("Jeff")
    print_welcome("Professor")

    print("\nTesting print_shop_menu function:")
    print_shop_menu("Apple", 2.75, "Orange", 1.50)
    print_shop_menu("Egg", .23, "Milk", 12.34)

def test_functions():
    """
    Runs test cases for all functions.
    """
    print_welcome("Haley")
    print_shop_menu("Apple", 2.75, "Orange", 1.50)
    
    num_purchased, money_left = purchase_item(1.23, 10, 3)
    print(f"Purchased: {num_purchased}, Money Left: ${leftover_money:.2f}")
    
    monster = new_random_monster()
    print(f"Encountered monster: {monster['name']}, {monster['description']}, ${monster['money']:.2f}")

if __name__ == "__main__":
    test_functions()

def combat_loop(player_hp, monster, player_gold, weapon, inventory):
    """
    Handles the combat loop between the player and the monster.

    Args:
        player_hp (int): Player's health.
        monster (dict): The monster dictionary.
        player_gold (float): Player's gold.

    Returns:
        tuple: Updated player_hp and player_gold.
    """
    monster_hp = monster['health']
    monster_power = monster['power']
    monster_money = monster['money']

    while monster_hp > 0 and player_hp > 0:
        print(f"\nYour HP: {player_hp} | {monster['name']} HP: {monster_hp}")
        print("1) Attack")
        print("2) Run Away")
        choice = input("Enter choice (1-2): ")

        if choice == "2":
            print("You ran away and returned to town.")
            return player_hp, player_gold, weapon

        if weapon:
            damage = random.randint(10, 20)
            weapon["currentDurability"] -= 1
            if weapon["currentDurability"] <= 0:
                print(f"Your {weapon['name']} broke!")
                inventory.remove(weapon)
                weapon = None
        else:
            damage = random.randint(5, 10)

        monster_hp -= damage
        print(f"You hit the {monster['name']} for {damage} damage!")

        if monster_hp <= 0:
            print(f"You defeated the {monster['name']} and earned {monster_money:.2f} gold!")
            player_gold += monster_money
            break

        player_hp -= monster_power
        print(f"The {monster['name']} hit you for {monster_power} damage!")

        if player_hp <= 0:
            print("You have been defeated by the monster!")
            break

    return player_hp, player_gold, weapon

def handle_monster_fight(player_hp, player_gold, inventory, equipped_weapon):
    monster = new_random_monster()
    print(f"\nYou leave town and encounter a {monster['name']}!")
    print(monster["description"])

    # Check for consumable item
    consumables = [item for item in inventory if item["type"] == "consumable"]
    if consumables:
        print("You can use a consumable item to avoid the fight.")
        use_item = input(f"Use {consumables[0]['name']}? (y/n): ")
        if use_item.lower() == "y":
            inventory.remove(consumables[0])
            print(f"You used {consumables[0]['name']} and defeated the monster without damage!")
            player_gold += monster["money"]
            return player_hp, player_gold, equipped_weapon

    return combat_loop(player_hp, monster, player_gold, equipped_weapon, inventory)

def sleep(player_hp, player_gold, max_hp):
    """
    Restores the player's HP by a set amount in exchange for gold.

    Args:
        player_hp (int): The player's current HP.
        player_gold (float): The player's current gold.
        max_hp (int): The player's maximum HP.

    Returns:
        tuple: Updated player_hp and player_gold after sleeping.
    """
    cost = 5
    heal_amount = 10

    if player_gold < cost:
        print("Not enough gold to sleep at the Inn.")
        return player_hp, player_gold

    player_gold -= cost
    player_hp = min(player_hp + heal_amount, max_hp)
    print(f"You slept at an Inn and recovered {heal_amount} HP. Current HP: {player_hp}, Gold left: {player_gold:.2f}")
    return player_hp, player_gold

# This program implements four functions for an adventure-style game:
# 1. purchase_item(): Calculates how many items can be purchased with a given amount of money.
# 2. new_random_monster(): Generates a random monster with different attributes.
# 3. print_welcome(): Prints a welcome message that is centered within 20 characters.
# 4. print_shop_menu(): Prints a shop sign with menu items and prices.
# The program also includes test cases to demonstrate the functionality of both functions.