#wanderingMonster.py
#Haley Burley
#4/20/2025

import random

class WanderingMonster:
    COLORS = {
        "Vampire": (255, 0, 0),       # Red
        "Pixie": (160, 32, 240),      # Purple
        "Frog": (0, 128, 0),          # Dark Green
    }

    def __init__(self, pos=None):
        monster = random.choice(list(self.COLORS.keys()))
        self.name = monster
        self.health = random.randint(15, 40)
        self.power = random.randint(5, 12)
        self.money = round(random.uniform(5, 20), 2)
        self.pos = pos or [random.randint(0, 9), random.randint(0, 9)]
        self.color = list(self.COLORS.get(monster, (255, 255, 255)))

    def move(self, occupied, town_pos):
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.pos[0] + dx
            new_y = self.pos[1] + dy
            if 0 <= new_x <= 9 and 0 <= new_y <= 9:
                if [new_x, new_y] not in occupied and [new_x, new_y] != town_pos:
                    self.pos = [new_x, new_y]
                    break
