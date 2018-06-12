import pygame
import Characters

pygame.init()

# Window Variables
winW = 500
winH = 500

win = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("My Game")
CLOCK = pygame.time.Clock()
FPS = 60

time_since_press = pygame.time.get_ticks()

player = Characters.Mario

# Main game loop
run = True


def gravity():

    if player.is_jump == 0 and player.y <= (winH - player.h):

        player.y = player.y + player.s

    if player.jumpcount > 0:

        player.jumpcount -= 1
        player.y -= (player.s * player.jumpcount) * 0.4
        player.started_imageloop = False
        init_image_bounds(0, 0)

        if player.is_left:
            player.started_imageloop = False
            init_image_bounds(8, 8)

    if player.y >= (winH - player.h):

        player.y = (winH - player.h)
        if player.image_y != 0:
            player.image_y = 0
            player.started_imageloop = False
            init_image_bounds(0, 0)

        if player.is_idle and not player.started_imageloop:
            init_image_bounds(0, 8)


def check_key(keys):
    global time_since_press

    if pygame.time.get_ticks() >= time_since_press + 5000 and not player.is_idle:
        player.is_idle = True
        player.started_imageloop = False
        print(player.is_idle)

    if keys[pygame.K_LEFT] and player.x >= 0:

        player.is_left = True
        player.x = player.x - player.s
        reset_idle()

        if player.images != player.image_left:
            player.images = player.image_left

    if keys[pygame.K_RIGHT] and player.x <= (winW - player.w):

        player.is_left = False
        player.x = player.x + player.s
        reset_idle()

        if player.images != player.image_right:
            player.images = player.image_right

    if keys[pygame.K_UP] and player.y >= (winH - player.h):

        player.image_y = 9
        player.jumpcount = 10
        reset_idle()

    if keys[pygame.K_DOWN] and player.y >= (winH - player.h):

        player.image_y = 9
        player.started_imageloop = False
        init_image_bounds(5, 5)
        reset_idle()

        if player.is_left:
            player.started_imageloop = False
            init_image_bounds(3, 3)


def reset_idle():
    global time_since_press
    time_since_press = pygame.time.get_ticks()
    player.started_imageloop = True
    player.is_idle = False


def init_image_bounds(start, end):
    if not player.started_imageloop:
        player.image_x = start
    player.image_start_bounds = start
    player.image_end_bounds = end


def run_through_images():

    # Increment imageCounts per Sec
    if pygame.time.get_ticks() > player.image_time + 1000:
        player.image_time = pygame.time.get_ticks()

        # Reset image count based on boundary
        if player.image_x < player.image_end_bounds:
            player.image_x += 1
            player.started_imageloop = True
        else:
            player.image_x = player.image_start_bounds


init_image_bounds(0, 8)

while run:
    CLOCK.tick(FPS)

    # Check controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
    gravity()
    check_key(keys)
    run_through_images()

    win.fill((0, 0, 0))
    win.blit(player.images, (player.x, player.y), (player.image_x * player.w,player.image_y * player.h,player.w,player.h))

    pygame.display.update()

pygame.quit()
