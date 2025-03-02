"""
game.py

This script imports functions from gamefunctions.py and calls those functions.
"""

import gamefunctions

def main():
    """
    Runs the main game logic, prompting user input and using imported functions.
    """
    # Ask for the player's name
    player_name = input("Enter your name: ")
    gamefunctions.print_welcome(player_name)

    # Display shop menu
    print("\nWelcome to the shop!")
    gamefunctions.print_shop_menu("Sword", 10.0, "Shield", 15.0)

    # Item purchase
    money = float(input("\nHow much money do you have? "))
    item_price = float(input("Enter the price of an item you want to buy: "))
    quantity = int(input("Enter quantity to purchase: "))

    purchased, remaining_money = gamefunctions.purchase_item(item_price, money, quantity)
    print(f"\nYou purchased {purchased} item(s). Money left: ${remaining_money:.2f}")

    # Generate a random monster
    print("\nA monster appears!")
    monster = gamefunctions.new_random_monster()
    print(f"Name: {monster['name']}\nDescription: {monster['description']}")

if __name__ == "__main__":
    main()
