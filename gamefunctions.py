#gamefunctions.py
#Haley Burley
#2/16/25

"""
gamefunctions.py

This script provides functions for an adventure-style game, including sleeping to restore health,
displaying a shop menu, processing item purchases, and generating random monsters to fight.

Functions:
- print_welcome(name):
    Prints a welcome message, centered within a fixed width.

- print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    Displays a decorative ASCII menu for shop items.

- purchase_item(itemPrice, startingMoney, quantityToPurchase):
    Calculates how many items can be bought with available money.

- visit_shop(player_gold, inventory):
    Displays a shop menu and allows the player to purchase items.

- equip_item(inventory, item_type):
    Lets the player choose an item of a specified type (weapon/armor) to equip.

- handle_equipment(inventory, equipped_weapon, equipped_armor):
    Prompts the user to equip either a weapon or armor and updates equipped gear.

- new_random_monster():
    Returns a randomly generated monster with name, description, stats, and reward.

- combat_loop(player_hp, monster, player_gold, weapon, inventory):
    Runs the combat sequence between the player and the monster, updating health and inventory.

- handle_monster_fight(player_hp, player_gold, inventory, equipped_weapon):
    Sets up a monster encounter and lets the player fight or use a consumable.

- handle_revive(player_gold, doctor_visits): 
    Applies the revival system after defeat.

- handle_adventure(player_hp, player_gold, inventory, equipped_weapon, doctor_visits): 
    Manages full fight + revive flow.

- sleep(player_hp, player_gold, max_hp):
    Restores player HP by a fixed amount in exchange for gold.

- save_game(filename, game_data):
    Saves the player’s game state to a JSON file.

- load_game(filename):
    Loads and returns game data from a JSON file.

- start_game(filename="savefile.json"):
    Prompts the player to start a new game or load a previous save, returning full game state.

- save_and_quit(filename, player_name, player_hp, player_gold, max_hp, inventory, weapon, armor):
    Saves all game data to a file and exits the game.

- launch_map(player_pos, monster_pos, town_pos)
    Launches the Pygame window and handles user input to move around a 10x10 grid.

- get_persistent_map_state()
    Handles loading or initializing map state from file.

- save_map_state(player_pos)
    Saves player’s current position on the map.

- launch_map_adventure(player_hp, player_gold, inventory, equipped_weapon, doctor_visits)
    Wrapper for handling town, monster, or exit results.

- explore_until_town(player_hp, player_gold, inventory, equipped_weapon, doctor_visits)
    Keeps the player in the map exploration loop until they return to town or exit.
"""

import random
import pygame
import os
import json

def print_welcome(name: str) -> None:
    """
    Prints a decorative welcome message centered in a 40-character wide box.

    Args:
        name (str): The name of the player.

    Returns:
        None 
    """
    print(f"\n{'=' * 40}")
    print(f"{'Hello, ' + name + '!':^40}")
    print(f"{'=' * 40}\n")

def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """
    Prints a stylized ASCII box shop sign with menu items and prices.

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

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1) -> tuple:
    """
    Calculates how many items can be purchased and the remaining money.

    Args:
        itemPrice (float): Price of a single item.
        startingMoney (float): Player's current money.
        quantityToPurchase (int, optional): Number of items player wants to buy. Defaults to 1.

    Returns:
        tuple: (int) Number of items purchased, (float) remaining money.
    """
    total_cost = itemPrice * quantityToPurchase
    if total_cost <= startingMoney:
        return quantityToPurchase, startingMoney - total_cost
    else:
        max_purchasable = int(startingMoney // itemPrice)
        return max_purchasable, startingMoney - (max_purchasable * itemPrice)

def visit_shop(player_gold, inventory):
    """
    Displays the shop interface, allows the player to purchase an item if they have enough gold,
    and updates the inventory and gold accordingly.

    Args:
        player_gold (float): The player's current gold.
        inventory (list): The player's inventory list of item dictionaries.

    Returns:
        tuple: (float) Updated player gold, (list) Updated inventory.
    """
    items_for_sale = [
        {"name": "sword", "type": "weapon", "maxDurability": 5, "currentDurability": 5, "price": 10},
        {"name": "shield", "type": "armor", "maxDurability": 5, "currentDurability": 5, "price": 8},
        {"name": "holy hand grenade", "type": "consumable", "note": "defeats monster", "price": 12}
    ]

    print("\nWelcome to the shop!")

    # Build formatted lines for each item
    item_lines = []
    for i, item in enumerate(items_for_sale, 1):
        name = f"{i}) {item['name'].title()}"
        price = f"${item['price']:.2f}"
        item_lines.append(f"| {name:<30}{price:>7} |")

    # Determine width based on longest line
    content_width = max(len(line) for line in item_lines)
    border = f"/{'-' * (content_width - 2)}\\"
    bottom = f"\\{'-' * (content_width - 2)}/"

    # Print box
    print(border)
    for line in item_lines:
        print(line)
    print(bottom)

    # Add option to leave shop
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
    """
    Prompts the player to choose an item of a specific type (e.g., weapon or armor) to equip from their inventory.

    Args:
        inventory (list): The player's inventory containing item dictionaries.
        item_type (str): The type of item to equip (e.g., "weapon", "armor").

    Returns:
        dict or None: The equipped item dictionary if selection is valid, otherwise None.
    """
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

def handle_equipment(inventory, equipped_weapon, equipped_armor):
    """
    Prompts the player to choose to equip a weapon or armor.

    Args:
        inventory (list): The player's inventory.
        equipped_weapon (dict or None): Currently equipped weapon.
        equipped_armor (dict or None): Currently equipped armor.

    Returns:
        tuple: (dict or None) Updated equipped_weapon, (dict or None) Updated equipped_armor.
    """
    print("What would you like to equip?")
    print("1) Weapon")
    print("2) Armor")
    equip_choice = input("Enter choice (1-2): ")
    while equip_choice not in ["1", "2"]:
        print("Invalid input.")
        equip_choice = input("Enter choice (1-2): ")

    if equip_choice == "1":
        equipped_weapon = equip_item(inventory, "weapon")
    elif equip_choice == "2":
        equipped_armor = equip_item(inventory, "armor")

    return equipped_weapon, equipped_armor

def new_random_monster() -> dict:
    """
    Generates a random monster with a name, description, health, power, and money.

    Returns:
        dict: A dictionary containing the monster's name, description, health, power, and money reward.
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

def combat_loop(player_hp, monster, player_gold, weapon, inventory):
    """
    Handles the combat loop between the player and the monster.

    Args:
        player_hp (int): The player's current HP.
        monster (dict): Dictionary representing the monster's stats and description.
        player_gold (float): The player's current amount of gold.
        weapon (dict or None): The currently equipped weapon (if any).
        inventory (list): The player's inventory containing items.

    Returns:
        tuple:
            (int) Updated player HP,
            (float) Updated player gold,
            (dict or None) Updated equipped weapon (may be None if broken).
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

        damage_taken = monster_power

        # Reduce damage if armor is equipped
        armor = next((item for item in inventory if item["type"] == "armor"), None)
        if armor:
            print(f"Your {armor['name']} absorbs some damage!")
            damage_taken = max(0, damage_taken - 5)
            armor["currentDurability"] -= 1
            if armor["currentDurability"] <= 0:
                print(f"Your {armor['name']} broke!")
                inventory.remove(armor)

        player_hp -= damage_taken
        print(f"The {monster['name']} hit you for {damage_taken} damage!")

        if player_hp <= 0:
            print("You have been defeated by the monster!")
            return "revive", player_gold, weapon
            break

    return player_hp, player_gold, weapon

def handle_monster_fight(player_hp, player_gold, inventory, equipped_weapon):
    """
    Initiates a monster encounter. Allows the player to either use a consumable item to defeat
    the monster instantly or engage in combat.

    Args:
        player_hp (int): The player's current HP.
        player_gold (float): The player's current gold.
        inventory (list): The player's inventory including consumables.
        equipped_weapon (dict or None): The currently equipped weapon, if any.

    Returns:
        tuple:
            (int) Updated player HP,
            (float) Updated player gold,
            (dict or None) Updated equipped weapon (may break in combat).
    """
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
    
    result = combat_loop(player_hp, monster, player_gold, equipped_weapon, inventory)

    if result[0] == "revive":
        return "revive", result[1], result[2]

    return result

def handle_revive(player_gold, doctor_visits):
    """
    Handles revival after defeat, including doctor rescue logic and gold deduction.

    Args:
        player_gold (float): The player's current gold.
        doctor_visits (int): How many times the doctor has already rescued the player.

    Returns:
        tuple:
            - (int) player_hp (restored to 10),
            - (float) updated player_gold,
            - (int) updated doctor_visits
    """
    doctor_visits += 1
    player_hp = 10

    if doctor_visits == 1:
        print("\nA stranger finds you unconscious and brings you to a doctor.")
        print("The doctor patches you up for free. You're restored to 10 HP.")
    else:
        player_gold -= 10
        print("\nOnce again, the doctor finds you... but this time, it costs you 10 gold.")
        print(f"Your new gold balance is: {player_gold:.2f}")

    return player_hp, player_gold, doctor_visits

def handle_adventure(player_hp, player_gold, inventory, equipped_weapon, doctor_visits):
    """
    Handles the monster encounter and revival process if the player is defeated.

    Args:
        player_hp (int): Current HP of the player.
        player_gold (float): Current gold.
        inventory (list): Player's inventory.
        equipped_weapon (dict or None): Equipped weapon.
        doctor_visits (int): Number of times revived by the doctor.

    Returns:
        tuple: 
            (int) Updated player_hp,
            (float) Updated player_gold,
            (dict or None) Updated equipped_weapon,
            (int) Updated doctor_visits
    """
    result = handle_monster_fight(player_hp, player_gold, inventory, equipped_weapon)

    if result[0] == "revive":
        player_gold = result[1]
        equipped_weapon = result[2]
        player_hp, player_gold, doctor_visits = handle_revive(player_gold, doctor_visits)
    else:
        player_hp, player_gold, equipped_weapon = result

    return player_hp, player_gold, equipped_weapon, doctor_visits

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

def save_game(filename: str, game_data: dict) -> None:
    """
    Saves the game state to a JSON file.

    Args:
        filename (str): The name of the file to save to.
        game_data (dict): The player's game state.
    
    Returns:
        None
    """
    try:
        with open(filename, 'w') as f:
            json.dump(game_data, f, indent=4)
        print(f"Game saved to {filename}!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(filename: str) -> dict:
    """
    Loads the game state from a JSON file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        dict or None: Loaded game data if successful, or None if loading fails.
    """
    try:
        with open(filename, 'r') as f:
            game_data = json.load(f)
        print(f"Game loaded from {filename}!")
        return game_data
    except FileNotFoundError:
        print(f"No save file found at {filename}.")
    except Exception as e:
        print(f"Error loading game: {e}")
    return None

def start_game(filename="savefile.json"):
    """
    Handles game start logic, prompting the user to load or start new.
    Returns initialized game state.

    Returns:
        tuple: (player_name, player_hp, player_gold, max_hp, player_inventory, equipped_weapon, equipped_armor, doctor_visits)
    """
    print("Welcome to the Adventure Game!")
    print("1) Start New Game")
    print("2) Load Saved Game")
    start_choice = input("Enter choice (1-2): ")
    while start_choice not in ["1", "2"]:
        print("Invalid input. Please choose 1 or 2.")
        start_choice = input("Enter choice (1-2): ")

    if start_choice == "2" and os.path.exists(filename):
        data = load_game(filename)
        if data:
            print_welcome(data.get("player_name", "Unknown"))
            return (
                data.get("player_name", "Unknown"),
                data.get("player_hp", 30),
                data.get("player_gold", 10),
                data.get("max_hp", 30),
                data.get("player_inventory", []),
                data.get("equipped_weapon"),
                data.get("equipped_armor"),
                data.get("doctor_visits", 0)
            )
        else:
            print("Failed to load. Starting a new game...")

    # Default new game state
    player_name = input("Enter your name: ")
    print_welcome(player_name)
    return (
        player_name,
        30,  # player_hp
        10,  # player_gold
        30,  # max_hp
        [],  # inventory
        None,  # equipped_weapon
        None,  # equipped_armor
        0    # doctor_visits
        )

def save_and_quit(filename, player_name, player_hp, player_gold, max_hp, inventory, weapon, armor, doctor_visits):
    """
    Saves game state and quits.

    Args:
        filename (str): The name of the file to save data into.
        player_name (str): The player's name.
        player_hp (int): The player's current HP.
        player_gold (float): The player's current gold.
        max_hp (int): The player's maximum HP.
        inventory (list): The player's inventory of items.
        weapon (dict or None): The currently equipped weapon.
        armor (dict or None): The currently equipped armor.
        doctor_visits (int): Number of times the player has been revived by the doctor.

    Returns:
        None
    """
    game_data = {
        "player_name": player_name,
        "player_hp": player_hp,
        "player_gold": player_gold,
        "max_hp": max_hp,
        "player_inventory": inventory,
        "equipped_weapon": weapon,
        "equipped_armor": armor,
        "doctor_visits": doctor_visits
    }
    save_game(filename, game_data)
    print("Game saved. Goodbye!")

MAP_STATE_FILE = "map_state.json"

def get_persistent_map_state():
    """
    Loads or initializes the persistent map state with fixed monster/town positions.

    Returns:
        dict: Dictionary with player position, town position, monster position.
    """
    if os.path.exists(MAP_STATE_FILE):
        with open(MAP_STATE_FILE, 'r') as f:
            return json.load(f)
    else:
        # Default map state
        state = {
            "player_pos": [5, 5],
            "town_pos": [5, 5],
            "monster_pos": [2, 7]
        }
        with open(MAP_STATE_FILE, 'w') as f:
            json.dump(state, f)
        return state
    
def save_map_state(player_pos):
    """
    Saves the player's last position to persist across sessions.

    Args:
        player_pos (tuple): The player's current (x, y) grid coordinates.

    Returns:
        None
    """
    state = get_persistent_map_state()
    state["player_pos"] = player_pos
    with open(MAP_STATE_FILE, 'w') as f:
        json.dump(state, f)

def launch_map(player_pos, monster_pos, town_pos):
    """
    Launches a graphical 10x10 grid using Pygame where the player can move and encounter events.

    Args:
        player_pos (list): Current [x, y] grid coordinates.
        monster_pos (list): Monster [x, y] location.
        town_pos (list): Town [x, y] location.

    Returns:
        str: "monster", "town", or "exit"
    """
    pygame.init()
    TILE_SIZE = 32
    GRID_SIZE = 10
    WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE

    print("Opening map...")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adventure Map")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_map_state(player_pos)
                pygame.quit()
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    save_map_state(player_pos)
                    pygame.quit()
                    return "exit"
                elif event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and player_pos[1] < 9:
                    player_pos[1] += 1
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and player_pos[0] < 9:
                    player_pos[0] += 1

        # Check for events
        if player_pos == monster_pos:
            save_map_state(player_pos)
            pygame.quit()
            return "monster"
        if player_pos == town_pos and player_pos != monster_pos:
            save_map_state(player_pos)
            pygame.quit()
            return "town"

        # Drawing
        screen.fill((0, 0, 0))  # Clear screen

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # draw grid border

        # Draw town
        pygame.draw.circle(
            screen, (0, 255, 0),
            (town_pos[0] * TILE_SIZE + TILE_SIZE // 2, town_pos[1] * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 3
        )

        # Draw monster
        pygame.draw.circle(
            screen, (255, 0, 0),
            (monster_pos[0] * TILE_SIZE + TILE_SIZE // 2, monster_pos[1] * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 3
        )

        # Draw player
        player_rect = pygame.Rect(
            player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (0, 0, 255), player_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return "exit"
        
def launch_map_adventure(player_hp, player_gold, inventory, equipped_weapon, doctor_visits):
    """
    Handles the launch and interaction with the exploration map, triggering events accordingly.

    Args:
        player_hp (int): Player HP
        player_gold (float): Player gold
        inventory (list): Inventory list
        equipped_weapon (dict): Equipped weapon
        doctor_visits (int): Number of times revived

    Returns:
        tuple: Updated (player_hp, player_gold, equipped_weapon, doctor_visits)
    """
    import random

    while True:
        state = get_persistent_map_state()

        # Randomize monster position (not overlapping town)
        while True:
            new_monster = [random.randint(0, 9), random.randint(0, 9)]
            if new_monster != state["town_pos"]:
                break

        state["monster_pos"] = new_monster

        # Move player off town or monster tile before launching map
        def move_off_tile(tile):
            if state["player_pos"] == tile:
                if tile[1] < 9:
                    state["player_pos"][1] += 1
                else:
                    state["player_pos"][1] -= 1

        move_off_tile(state["town_pos"])
        move_off_tile(state["monster_pos"])

        save_map_state(state["player_pos"])  # Save new starting position
        result = launch_map(state["player_pos"], state["monster_pos"], state["town_pos"])

        if result == "monster":
            player_hp, player_gold, equipped_weapon, doctor_visits = handle_adventure(
                player_hp, player_gold, inventory, equipped_weapon, doctor_visits
            )
            print("Returning to the map...")
            return "continue", player_hp, player_gold, equipped_weapon, doctor_visits
        elif result == "town":
            print("You returned to town.")
            return "town", player_hp, player_gold, equipped_weapon, doctor_visits
        else:
            print("You left the map without incident.")
            return "town", player_hp, player_gold, equipped_weapon, doctor_visits
    
def explore_until_town(player_hp, player_gold, inventory, equipped_weapon, doctor_visits):
    """
    Keeps the player in the map exploration loop until they return to town or exit.

    Returns:
        tuple: Updated (player_hp, player_gold, equipped_weapon, doctor_visits)
    """
    while True:
        result, player_hp, player_gold, equipped_weapon, doctor_visits = launch_map_adventure(
            player_hp, player_gold, inventory, equipped_weapon, doctor_visits
        )
        if result == "town":
            break
    return player_hp, player_gold, equipped_weapon, doctor_visits
