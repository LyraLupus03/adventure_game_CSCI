#game.py
#Haley Burley
#4/6/2025

"""
game.py

This script imports functions from gamefunctions.py and calls those functions for an 
adventure-style game where you can buy items and fight monsters.
"""
import gamefunctions

def main():
    """
    Runs the main game logic, prompting user input and using imported functions.
    """
    (player_name, player_hp, player_gold, max_hp,
    player_inventory, equipped_weapon, equipped_armor, doctor_visits) = gamefunctions.start_game()

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold:.2f}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Equip Item")
        print("5) Craft Potion")
        print("6) Quit")
        print("7) Save and Quit")

        choice = input("Enter choice (1-7): ")
        while choice not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Invalid input. Please choose 1, 2, 3, 4, 5, 6, or 7.")
            choice = input("Enter choice (1-7): ")

        if choice == "1":
            player_hp, player_gold, equipped_weapon, doctor_visits = gamefunctions.explore_until_town(
                player_hp, player_gold, player_inventory, equipped_weapon, doctor_visits)
        elif choice == "2":
            player_hp, player_gold = gamefunctions.sleep(player_hp, player_gold, max_hp)
        elif choice == "3":
            player_gold, player_inventory = gamefunctions.visit_shop(player_gold, player_inventory)
        elif choice == "4":
            equipped_weapon, equipped_armor = gamefunctions.handle_equipment(
                player_inventory, equipped_weapon, equipped_armor)
        elif choice == "5":
            player_inventory = gamefunctions.visit_crafting_station(player_inventory)
        elif choice == "6":
            print("Thanks for playing!")
        elif choice == "7":
            gamefunctions.save_and_quit("savefile.json", player_name, player_hp,
                player_gold, max_hp, player_inventory, equipped_weapon, equipped_armor, doctor_visits)
            break

if __name__ == "__main__":
    main()
