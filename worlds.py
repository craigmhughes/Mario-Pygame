import pygame
import objects
import characters


class overWorld:
    # world variables
    x = 0
    y = 0
    width = 0
    height = 0

    # stage = None

    background = pygame.image.load("assets/sprites/backgrounds/overworld.png")

    tile_w = objects.tiles.w
    tile_h = objects.tiles.h

    block_w = objects.blocks.w
    block_h = objects.blocks.h

    # Collection of objects which make up Scene/Level
    level_one = None

    def get_ground(self, stage):

        b_bound = 568

        if stage == 1:
            return [objects.tiles(self.tile_w * 0, b_bound, 4, 1, 0, 12),
                    objects.tiles(self.tile_w * 4, b_bound, 4, 1, 0, 12),
                    objects.tiles(self.tile_w * 8, b_bound, 4, 1, 0, 12),
                    objects.tiles(self.tile_w * 12, b_bound, 1, 1, 8, 4),

                    # Hill Start
                    objects.tiles(self.tile_w * 15, b_bound - (self.tile_h * 2), 2, 3, 5, 4),
                    objects.tiles(self.tile_w * 17, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 19, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 21, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 23, b_bound - (self.tile_h * 2), 2, 3, 6, 4),

                    objects.tiles(self.tile_w * 25, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 27, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 29, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 31, b_bound - (self.tile_h * 2), 2, 3, 6, 4),
                    objects.tiles(self.tile_w * 33, b_bound - (self.tile_h * 2), 2, 3, 6, 4)

                    # Floater 1
                    #objects.tiles(self.tile_w * 5, b_bound - (self.tile_h * 7), 2, 4, 5, 4),
                    ]

    def get_objects(self, stage):

        if stage == 1:
            return [objects.blocks(self.block_w * 8, 430, 1, 1, 0, 0, "coin"),
                    objects.blocks(self.block_w * 9, 430, 1, 1, 0, 0, "none"),
                    objects.blocks(self.block_w * 10, 430, 1, 1, 11, 0, "shroom-0"),
                    objects.blocks(self.block_w * 11, 430, 1, 1, 0, 0, "none")]

    def get_enemies(self, stage):
        if stage == 1:
            return [characters.enemy("turtle", 150, 400, None),
                    characters.enemy("turtle", 650, 350, None)]

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.background = pygame.transform.scale(self.background, (w, h))
        self.level_one = [self.get_ground(1), self.get_objects(1), self.get_enemies(1)]
