import pygame


class Mario:
    # Player variables
    x = 50
    y = 50
    w = 48
    h = 64
    s = 10

    image_x = 0
    image_y = 0

    image_start_bounds = 0
    image_end_bounds = 0

    image_time = pygame.time.get_ticks()
    images = pygame.image.load("mario-sprites.png")
    images = pygame.transform.scale(images, (432, 1152))
    image_right = images
    image_left = pygame.transform.flip(images, True, False)
    started_imageloop = False

    is_left = False
    is_idle = False

    jumpcount = 0
    is_jump = False

    parent = None

    def __init__(self):
        Mario.parent = self
