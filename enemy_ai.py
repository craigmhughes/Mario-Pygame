import pygame


class ai:

    current_world = None

    def run(self):
        current_world = self.current_world

        for i in current_world.level_one[2]:
            enemy = i

            for ground in current_world.level_one[0]:
                print(current_world.level_one[0][current_world.level_one[0].index(ground) + 1])

    def __init__(self, world):
        self.current_world = world
