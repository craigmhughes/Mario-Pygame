import pygame
import objects


class overWorld:
    # world variables
    x = 0
    y = 0
    width = 0
    height = 0

    # stage = None

    background = pygame.image.load("assets/sprites/backgrounds/overworld.png")

    tile_w = objects.tiles.w

    # Collection of objects which make up Scene/Level - TODO: Possibly convert to own class?
    level_one = None

    def get_ground(self, stage):

        if stage == 1:
            return [objects.tiles(self.tile_w * 0, 568, 4, 1, 0, 12), objects.tiles(self.tile_w * 4, 568, 4, 1, 0, 12),
                    objects.tiles(self.tile_w * 8, 568, 4, 1, 0, 12), objects.tiles(self.tile_w * 12, 568, 1, 1, 8, 4), ]

    def get_objects(self, stage):

        if stage == 1:
            return [objects.tiles(self.tile_w * 0, 468, 4, 1, 4, 12)]

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.background = pygame.transform.scale(self.background, (w, h))
        self.level_one = [self.get_ground(1), self.get_objects(1)]
