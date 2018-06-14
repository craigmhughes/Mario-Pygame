import pygame
import objects


class overWorld:
    # world variables
    x = 0
    y = 0
    width = 0
    height = 0

    #stage = None

    background = pygame.image.load("assets/sprites/backgrounds/overworld.png")

    tile_w = objects.tiles.w

    # Collection of objects which make up Scene/Level - TODO: Possibly convert to own class?
    level_one = [objects.tiles(tile_w * 0, 568, 7, 4), objects.tiles(tile_w * 1, 568, 7, 4), objects.tiles(tile_w * 2, 568, 7, 4),
                 objects.tiles(tile_w * 3, 568, 7, 4), objects.tiles(tile_w * 4, 568, 7, 4), objects.tiles(tile_w * 5, 568, 7, 4),
                 objects.tiles(tile_w * 6, 568, 7, 4), objects.tiles(tile_w * 7, 568, 7, 4), objects.tiles(tile_w * 8, 568, 7, 4),
                 objects.tiles(tile_w * 9, 568, 7, 4), objects.tiles(tile_w * 10, 568, 7, 4), objects.tiles(tile_w * 11, 568, 7, 4),
                 objects.tiles(tile_w * 12, 568, 7, 4), objects.tiles(tile_w * 13, 568, 7, 4), objects.tiles(tile_w * 14, 568, 7, 4),
                 objects.tiles(tile_w * 15, 568, 7, 4), objects.tiles(tile_w * 16, 568, 7, 4), objects.tiles(tile_w * 17, 568, 7, 4),
                 objects.tiles(tile_w * 18, 568, 7, 4), objects.tiles(tile_w * 19, 568, 7, 4), objects.tiles(tile_w * 20, 568, 8, 4),]

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.background = pygame.transform.scale(self.background, (w, h))