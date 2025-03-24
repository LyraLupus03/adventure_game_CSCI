"""
game.py

This script imports functions from gamefunctions.py and calls those functions.
"""
# hello
import gamefunctions

def main():
    """
    Runs the main game logic, prompting user input and using imported functions.
    """
    # Ask for the player's name
    player_name = input("Enter your name: ")
    gamefunctions.print_welcome(player_name)

    player_hp = 30
    player_gold = 10
    max_hp = 30

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold:.2f}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")

        choice = input("Enter choice (1-3): ")
        while choice not in ["1", "2", "3"]:
            print("Invalid input. Please choose 1, 2, or 3.")
            choice = input("Enter choice (1-3): ")

        if choice == "1":
            player_hp, player_gold = gamefunctions.handle_monster_fight(player_hp, player_gold)
        elif choice == "2":
            player_hp, player_gold = gamefunctions.sleep(player_hp, player_gold, max_hp)
        elif choice == "3":
            print("Thanks for playing!")
            break

    # TEST Display shop menu
    #print("\nWelcome to the shop!")
    #gamefunctions.print_shop_menu("Sword", 10.0, "Shield", 15.0)

    # TEST Item purchase
    #money = float(input("\nHow much money do you have? "))
    #item_price = float(input("Enter the price of an item you want to buy: "))
    #quantity = int(input("Enter quantity to purchase: "))

    #purchased, remaining_money = gamefunctions.purchase_item(item_price, money, quantity)
    #print(f"\nYou purchased {purchased} item(s). Money left: ${remaining_money:.2f}")

    # TEST Generate a random monster
    #print("\nA monster appears!")
    #monster = gamefunctions.new_random_monster()
    #print(f"Name: {monster['name']}\nDescription: {monster['description']}")

if __name__ == "__main__":
    main()
