import pygame


class tiles:

    x = 0
    y = 0
    w = 32
    h = 32

    image_x = 0
    image_y = 0

    is_clippable = True

    background = pygame.image.load("assets/sprites/backgrounds/tiles/overworld-tiles.png")
    background = pygame.transform.scale2x(background)

    # w & h are multiples of existing w & h variables
    def __init__(self, x, y, w, h, imgx, imgy):
        self.x = x
        self.y = y
        self.w *= w
        self.h *= h
        self.image_x = imgx
        self.image_y = imgy


class blocks:
    x = 0
    y = 0
    w = 32
    h = 32

    image_x = 0
    image_y = 0

    image_start_bounds = 0
    image_end_bounds = 0
    started_imageloop = False
    image_time = pygame.time.get_ticks()

    block_type = None
    is_broken = False
    is_hit = False
    pick_up = None
    bump_count = 0

    background = pygame.image.load("assets/sprites/backgrounds/tiles/object-tiles.png")

    def __init__(self, x, y, w, h, imgx, imgy, p_up):
        self.x = x
        self.y = y
        self.w *= w
        self.h *= h
        self.image_x = imgx
        self.image_y = imgy
        self.pick_up = None if p_up == "none" else pickup(self.x, self.y, p_up)

        if imgx == 0:
            self.block_type = "brick"


class pickup:
    x = 0
    y = 0
    w = 32
    h = 32

    image_x = 0
    image_y = 0

    # Default pickup type is coin
    type = "coin"

    image_start_bounds = 0
    image_end_bounds = 0
    started_imageloop = False
    image_time = pygame.time.get_ticks()

    is_hit = False

    background = pygame.image.load("assets/sprites/backgrounds/tiles/object-tiles.png")

    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y

        if p_type == "shroom-0":
            self.type = p_type
            self.image_x = 0
            self.image_y = 1
        if p_type == "shroom-1":
            self.type = p_type
            self.image_x = 1
            self.image_y = 1
        if p_type == "shroom-2":
            self.type = p_type
            self.image_x = 2
            self.image_y = 1

        if p_type == "star":
            self.type = p_type
            self.image_x = 3
            self.image_y = 1

        if p_type == "flower":
            self.type = p_type
            self.image_x = 4
            self.image_y = 1

        if p_type == "coin":
            self.type = p_type
            self.image_x = 1
            self.image_y = 2
