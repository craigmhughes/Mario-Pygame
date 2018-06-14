import pygame
import characters
import worlds

pygame.init()

# Window Variables
winW = 800
winH = 600

win = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("My Game")
CLOCK = pygame.time.Clock()
FPS = 60

time_since_press = pygame.time.get_ticks()

# Objects
player = characters.mario()
current_world = worlds.overWorld(winW, winH)

# Sounds
sound_dir = "assets/sounds/fx/"
sounds = [pygame.mixer.Sound(sound_dir + "player-jump.ogg"), pygame.mixer.Sound(sound_dir + "block-hit.ogg")]

music_dir = "assets/sounds/music/"
music = [music_dir + "overworld.mp3"]
pygame.mixer.music.load(music[0])

# Main game loop
run = True


# pygame.mixer.music.play(1)


def gravity():

    player.y += player.s * 2

    if player.jumpcount > 0:

        player.jumpcount -= 1
        player.y -= (player.s * player.jumpcount) * 1.5
        player.started_imageloop = False
        init_image_bounds(0, 0)

        if player.is_left:
            player.started_imageloop = False
            init_image_bounds(8, 8)

    for index in current_world.level_one:
        if (index.x - (index.w / 2)) <= player.x <= (index.x + (index.w / 2)):
            if player.y >= (index.y - player.h):

                # Ground hit noise
                if player.is_jump:
                    pygame.mixer.Sound.play(sounds[1])

                player.y = (index.y - player.h)
                player.is_jump = False
                player.collision[3] = True

                if player.is_idle and not player.started_imageloop:
                    init_image_bounds(0, 8)


def check_key(key):
    global time_since_press

    if pygame.time.get_ticks() >= time_since_press + 5000 and not player.is_idle:
        player.is_idle = True
        player.started_imageloop = False
        print(player.is_idle)

    elif pygame.time.get_ticks() >= time_since_press + 100:

        if player.image_y != 0 and player.collision[3]:
            player.image_y = 0
            player.started_imageloop = False
            init_image_bounds(0, 0)
            player.is_walk = False

    if key[pygame.K_LEFT] and player.x >= 0:

        if player.images != player.image_left:
            player.images = player.image_left

        if (player.image_y != 3 or not player.is_left) and player.collision[3]:
            player.started_imageloop = False
            player.image_y = 3
            init_image_bounds(2, 8)
            player.is_walk = True

        player.is_left = True
        player.x -= (player.s * 2) if player.is_jump else player.s
        reset_idle()

    if key[pygame.K_RIGHT] and player.x <= (winW - player.w):

        if player.images != player.image_right:
            player.images = player.image_right

        if (player.image_y != 3 or player.is_left) and player.collision[3]:
            player.started_imageloop = False
            player.image_y = 3
            init_image_bounds(0, 6)
            player.is_walk = True

        player.is_left = False
        player.x += (player.s * 3) if player.is_jump else player.s
        reset_idle()

    if key[pygame.K_UP]:

        if player.collision[3]:
            pygame.mixer.Sound.play(sounds[0])
            player.image_y = 9
            player.image_x = 0
            player.jumpcount = 10
            player.is_jump = True
            player.collision[3] = False

        reset_idle()

    if key[pygame.K_DOWN] and player.collision[3] and not player.is_walk:

        player.image_y = 9
        player.started_imageloop = False

        if player.is_left:
            init_image_bounds(3, 3)
        else:
            init_image_bounds(5, 5)

        reset_idle()


def reset_idle():
    global time_since_press
    player.is_idle = False
    time_since_press = pygame.time.get_ticks()
    player.started_imageloop = True


def init_image_bounds(start, end):
    if not player.started_imageloop:
        player.image_x = start
    player.image_start_bounds = start
    player.image_end_bounds = end


def run_through_images():
    # Increment imageCounts per Sec
    if pygame.time.get_ticks() > player.image_time + 1000 or \
            pygame.time.get_ticks() > player.image_time + 100 and player.is_walk:

        player.image_time = pygame.time.get_ticks()

        # Reset image count based on boundary
        if player.image_x >= player.image_end_bounds:
            player.image_x = player.image_start_bounds
        else:
            player.started_imageloop = True
            player.image_x += 1


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

    # Show world
    win.blit(current_world.background, (current_world.x, current_world.y))

    # Show world objects -- TODO: Make this reusable, currently restricted to LEVEL ONE!
    for index in current_world.level_one:
        win.blit(index.background, (index.x, index.y),
                 (index.image_x * index.w, index.image_y * index.h, index.w, index.h))

    # Show Player
    win.blit(player.images, (player.x, player.y),
             (player.image_x * player.w, player.image_y * player.h, player.w, player.h))

    pygame.display.update()

pygame.quit()
