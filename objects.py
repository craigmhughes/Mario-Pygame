import pygame


class tiles:

    x = 0
    y = 0
    w = 32
    h = 32

    image_x = 0
    image_y = 0

    background = pygame.image.load("assets/sprites/backgrounds/tiles/overworld-tiles.png")
    background = pygame.transform.scale2x(background)

    def __init__(self, x, y, imgx, imgy):
        self.x = x
        self.y = y
        self.image_x = imgx
        self.image_y = imgy
