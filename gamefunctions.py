#gamefunctions.py
#Haley Burley
#2/16/25

import random

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Calculates how many items can be purchased and the remaining money.
    """
    total_cost = itemPrice * quantityToPurchase
    if total_cost <= startingMoney:
        return quantityToPurchase, startingMoney - total_cost
    else:
        max_purchasable = int(startingMoney // itemPrice)
        return max_purchasable, startingMoney - (max_purchasable * itemPrice)

def new_random_monster():
    """
    Generates a random monster with name, description, health, power, and money.
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

def print_welcome(name):
    """
    Prints a welcome message that is centered within 20 characters.
    """
    print(f"{'Hello, ' + name + '!':^20}")

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a shop sign with menu items and prices, and a border around it.
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

# This program implements four functions for an adventure-style game:
# 1. purchase_item(): Calculates how many items can be purchased with a given amount of money.
# 2. new_random_monster(): Generates a random monster with different attributes.
# 3. print_welcome(): Prints a welcome message that is centered within 20 characters.
# 4. print_shop_menu(): Prints a shop sign with menu items and prices.
# The program also includes test cases to demonstrate the functionality of both functions.