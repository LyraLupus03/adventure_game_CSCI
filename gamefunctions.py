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
            "money": round(random.uniform(1, 50), 2),
        },
        {
            "name": "Frog",
            "description": "You discover a frog licking its lips as it looks you over.",
            "health": random.randint(5, 15),
            "power": random.randint(2, 7),
            "money": round(random.uniform(10, 150), 2),
        },
        {
            "name": "Vampire",
            "description": "A shadowy figure jumps out at you from behind a tree.",
            "health": random.randint(30, 50),
            "power": random.randint(10, 20),
            "money": round(random.uniform(5, 100), 2),
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
    border = "/----------------\\"
    print(border)
    print(f"| {item1Name:<12} ${item1Price:>6.2f} |")
    print(f"| {item2Name:<12} ${item2Price:>6.2f} |")
    print("\\----------------/")

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
        print(f"Purchased: {num_purchased}, Money Left: {leftover_money}")

    print("\nTesting default quantity parameter:")
    num_purchased, leftover_money = purchase_item(2.50, 10)
    print(f"Purchased: {num_purchased}, Money Left: {leftover_money}")

    print("\nTesting new_random_monster function:")
    for _ in range(3):
        monster = new_random_monster()
        print(f"Name: {monster['name']}")
        print(f"Description: {monster['description']}")
        print(f"Health: {monster['health']}")
        print(f"Power: {monster['power']}")
        print(f"Money: {monster['money']}\n")

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
    print(f"Purchased: {num_purchased}, Money Left: {money_left}")
    
    monster = new_random_monster()
    print(f"Encountered monster: {monster['name']}, {monster['description']}")

if __name__ == "__main__":
    test_functions()

# This program implements four functions for an adventure-style game:
# 1. purchase_item(): Calculates how many items can be purchased with a given amount of money.
# 2. new_random_monster(): Generates a random monster with different attributes.
# 3. print_welcome(): Prints a welcome message that is centered within 20 characters.
# 4. print_shop_menu(): Prints a shop sign with menu items and prices.
# The program also includes test cases to demonstrate the functionality of both functions.