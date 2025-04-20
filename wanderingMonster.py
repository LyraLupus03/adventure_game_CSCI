#wanderingMonster.py
#Haley Burley
#4/20/2025

import random

class WanderingMonster:
    """
    A class representing a wandering monster on the map.

    Attributes:
        name (str): Monster name.
        health (int): Current HP.
        power (int): Attack strength.
        money (float): Gold reward if defeated.
        pos (list): [x, y] grid position.
        color (tuple): RGB color used on the map.
    """

    COLORS = {
        "Zombie": (255, 0, 0),
        "Slime": (0, 255, 0),
        "Ghost": (200, 200, 255),
    }

    def __init__(self, pos=None):
        monster = random.choice(["Zombie", "Slime", "Ghost"])
        self.name = monster
        self.health = random.randint(15, 40)
        self.power = random.randint(5, 12)
        self.money = round(random.uniform(5, 20), 2)
        self.pos = pos or [random.randint(0, 9), random.randint(0, 9)]
        self.color = self.COLORS.get(monster, (255, 255, 255))

    def move(self, occupied, town_pos):
        """
        Moves the monster randomly in one of the 4 directions if within bounds.

        Args:
            occupied (list): List of [x, y] tiles to avoid.
            town_pos (list): Town coordinates to avoid.

        Returns:
            None
        """
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.pos[0] + dx
            new_y = self.pos[1] + dy
            if 0 <= new_x <= 9 and 0 <= new_y <= 9:
                if [new_x, new_y] not in occupied and [new_x, new_y] != town_pos:
                    self.pos = [new_x, new_y]
                    break
