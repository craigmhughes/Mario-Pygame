import pygame
from pygame.rect import Rect

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
last_obj = current_world.level_one[0][len(current_world.level_one[0]) - 1]

gravity_val = player.s * 2

# Player variables
player_hit_camerabounds = False
block_hit = False

# Sounds
sound_dir = "assets/sounds/fx/"
sounds = [pygame.mixer.Sound(sound_dir + "player-jump.ogg"), pygame.mixer.Sound(sound_dir + "block-hit.ogg")]

music_dir = "assets/sounds/music/"
music = [music_dir + "overworld.mp3"]
pygame.mixer.music.load(music[0])

# Main game loop
run = True


#pygame.mixer.music.play(1)

# ////////////  START SETUP
def setup():
    for enemy in current_world.level_one[2]:
        enemy.world = current_world.level_one
        enemy.player = player
# ////////////  END SETUP


# ////////////  START GRAVITY
def gravity():

    player.y += gravity_val

    for enemy in current_world.level_one[2]:
        enemy.y += gravity_val
        check_side_bounds(enemy)
        check_bottom_bounds(enemy)
        enemy.ai()

    check_side_bounds(player)
    check_bottom_bounds(player)

    if player.jumpcount > 0:

        player.jumpcount = 0 if player.collision[3] else player.jumpcount - 1

        if not player.collision[2]:
            player.y -= (player.s * player.jumpcount) * 1.5
            player.started_imageloop = False
            init_image_bounds(player, 0, 0)

            if player.is_left:
                player.started_imageloop = False
                init_image_bounds(player, 8, 8)

    check_top_bounds(player)
    for enemy in current_world.level_one[2]:
        check_top_bounds(enemy)

# ////////////  END GRAVITY


# ////////////  START KEY CHECK

def check_key(key):
    global time_since_press

    if pygame.time.get_ticks() >= time_since_press + 5000 and not player.is_idle:
        player.is_idle = True
        player.started_imageloop = False
        print(player.is_idle)

    elif pygame.time.get_ticks() >= time_since_press + 100 or pygame.time.get_ticks() < player.last_jump + 300:

        if player.image_y != 0 and player.collision[3]:
            player.image_y = 0
            player.started_imageloop = False
            init_image_bounds(player, 0, 0)
            player.is_walk = False

    if key[pygame.K_LEFT] and player.x >= 0:

        if not player.collision[0]:
            if player.images != player.image_left:
                player.images = player.image_left

            if (player.image_y != 3 or not player.is_left) and player.collision[3]:
                player.started_imageloop = False
                player.image_y = 3
                init_image_bounds(player, 2, 8)
                player.is_walk = True

            player.is_left = True

            # Bases camera test on position of first ground block -- Make sure this is 0!
            if current_world.level_one[0][0].x < 0:
                # Check if last ground is in window and player is past camera clip
                if last_obj.x <= winW + last_obj.w and player.x > winW / 2:
                    player.x -= (player.s * 2) if player.is_jump else player.s
                else:
                    for index in current_world.level_one:
                        for obj in index:
                            obj.x += (player.s * 1.5) if player.is_jump else player.s
            else:
                player.x -= (player.s * 2) if player.is_jump else player.s

            reset_idle()

    if key[pygame.K_RIGHT] and player.x <= (winW - player.w):

        if not player.collision[1]:
            if player.images != player.image_right:
                player.images = player.image_right

            if (player.image_y != 3 or player.is_left) and player.collision[3]:
                player.started_imageloop = False
                player.image_y = 3
                init_image_bounds(player, 0, 6)
                player.is_walk = True

            player.is_left = False

            if not player_hit_camerabounds or last_obj.x <= winW - last_obj.w:
                player.x += (player.s * 2) if player.is_jump else player.s
            else:
                for index in current_world.level_one:
                    for obj in index:
                        obj.x -= (player.s * 1.5) if player.is_jump else player.s
            reset_idle()

    if key[pygame.K_UP]:

        # Check if player is touching a piece of ground and restricts jump times
        if player.collision[3] and pygame.time.get_ticks() > player.last_jump + 300:
            #pygame.mixer.Sound.play(sounds[0])
            player.image_y = 9
            player.image_x = 0
            player.jumpcount = 10
            player.is_jump = True
            player.last_jump = pygame.time.get_ticks()
            player.collision[3] = False

        reset_idle()

    if key[pygame.K_DOWN] and player.collision[3] and not player.is_walk:

        player.image_y = 9
        player.started_imageloop = False

        if player.is_left:
            init_image_bounds(player, 3, 3)
        else:
            init_image_bounds(player, 5, 5)

        reset_idle()

# ////////////  END KEY CHECK


# ////////////  START COLLISION CHECK

# COLLISION CHECKS ARE IN REFERENCE TO THE BLOCKS NOT THE PLAYER
def check_side_bounds(player):
    for index in current_world.level_one:
        for index in index:
            if player.y + player.h - 30 > index.y - (player.w / 2) and player.y < index.y + index.h:
                # Check left collision
                if index.x - 100 <= player.x + player.w < index.x:
                    player.collision[1] = True
                    player.collision[0] = False
                # Check right
                elif index.x + index.w - 30 < player.x < index.x + index.w + 5:
                    player.collision[0] = True
                    player.collision[1] = False
                else:
                    reset_sides()

                # if is enemy, do not clip
                try:
                    if index.enemy_type is not None:
                        player.collision[0] = False
                        player.collision[1] = False
                except AttributeError:
                    pass

            else:
                reset_sides()


def check_bottom_bounds(player):
    # Check if hit bottom of tile
    global block_hit

    for tiles in current_world.level_one:
        for index in tiles:

            if player.x + player.w >= index.x and player.x <= (index.x + index.w):
                if index.y + index.h + 20 > player.y >= index.y + index.h:

                    # Bumps block if is brick
                    try:
                        if (index.block_type == "brick" or index.block_type == "question") and not index.is_hit and not block_hit and player.jumpcount != 0:
                            # Fixes Awkward offset of brick collision
                            if tiles.index(index) + 1 <= len(tiles) - 1:
                                adj_obj = tiles[tiles.index(index) + 1]
                                if player.x + (player.w / 2) >= adj_obj.x:
                                    adj_obj.is_hit = True
                                    adj_obj.bump_count = 20
                                else:
                                    index.is_hit = True
                                    index.bump_count = 20
                            else:
                                index.is_hit = True
                                index.bump_count = 20

                            block_hit = True

                    except AttributeError:
                        pass

                    # Stop player jump if hit block
                    player.collision[2] = True
                    player.jumpcount = 0

                # else is needed to reset states of player and block after hit
                else:
                    player.collision[2] = False
                    try:
                        if (index.block_type == "brick" or index.block_type == "question") and index.bump_count == 0:
                            index.is_hit = False
                    except AttributeError:
                        pass
            else:
                player.collision[2] = False


def check_top_bounds(player):
    # Check if is on top of tile
    for tiles in current_world.level_one:
        for index in tiles:

            if player.x + player.w / 2 >= index.x and player.x <= (index.x + index.w):
                if player.y + player.h > index.y and player.y + (player.h / 2) < index.y - 20:

                    player.collision[3] = True
                    # if is enemy, do not clip
                    try:
                        if index.enemy_type is not None:
                            player.collision[3] = False
                    except AttributeError:
                        pass

                    try:
                        player.collision[3] = not index.is_hit
                    except AttributeError:
                        pass

                    if player.collision[3]:
                        # Ground hit noise
                        #if player.is_jump:
                            #pygame.mixer.Sound.play(sounds[1])
                        player.y = (index.y - player.h)
                        player.is_jump = False

                    # Start idle
                    if player.is_idle and not player.started_imageloop:
                        init_image_bounds(player, 0, 8)

# ////////////  END COLLISION CHECK


def reset_sides():
    player.collision[0] = False
    player.collision[1] = False


def reset_idle():
    global time_since_press
    player.is_idle = False
    time_since_press = pygame.time.get_ticks()
    player.started_imageloop = True


def init_image_bounds(obj, start, end):
    if not obj.started_imageloop:
        obj.image_x = start
    obj.image_start_bounds = start
    obj.image_end_bounds = end


# ////////////  START PLAYER IMAGES
def run_through_player_images():

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

# ////////////  END PLAYER IMAGES


# ////////////  START BLOCK IMAGES
def run_through_block_images(obj):
    global block_hit

    if pygame.time.get_ticks() > obj.image_time + 15 and obj.bump_count > 10:
        obj.y -= 1
        obj.bump_count -= 1
        # Lifts pickup out
        if obj.pick_up is not None and not obj.pick_up.is_hit:
            obj.pick_up.y -= 4

    if pygame.time.get_ticks() > obj.image_time + 1 and 10 >= obj.bump_count > 0:
        obj.y += 1
        obj.bump_count -= 1
        if obj.pick_up is not None:
            obj.pick_up.is_hit = True

    # Only hit one block at a time
    if pygame.time.get_ticks() > obj.image_time + 1 and obj.bump_count == 1:
        obj.y += 1
        obj.bump_count -= 1
        block_hit = False

    if pygame.time.get_ticks() > obj.image_time + 150:
        if obj.image_x >= obj.image_end_bounds:
            obj.image_time = pygame.time.get_ticks()
            obj.image_x = obj.image_start_bounds
        else:
            obj.image_time = pygame.time.get_ticks()
            obj.started_imageloop = True
            obj.image_x += 1

        if obj.pick_up is not None:
            pickup = obj.pick_up

            if pickup.image_x >= pickup.image_end_bounds:
                pickup.image_time = pygame.time.get_ticks()
                pickup.image_x = pickup.image_start_bounds
            else:
                pickup.image_time = pygame.time.get_ticks()
                pickup.started_imageloop = True
                pickup.image_x += 1

# ////////////  END BLOCK IMAGES


# ////////////  START RENDER WORLD
def render_world():
    # Show world
    win.blit(current_world.background, (current_world.x, current_world.y))

    # Show world objects -- TODO: Make this reusable, currently restricted to LEVEL ONE!
    for i in current_world.level_one:
        if current_world.level_one.index(i) != 2:
            for index in i:
                # Try needed as only brick and question blocks have type attr
                try:
                    if index.block_type == "brick" or index.block_type == "question":

                        # Render Pickups
                        if index.pick_up is not None:
                            pickup = index.pick_up
                            pickup.x = index.x
                            win.blit(pickup.background, (pickup.x, pickup.y),
                                     (pickup.image_x * pickup.w, pickup.image_y * pickup.h, pickup.w, pickup.h))

                            if pickup.x < player.x < pickup.x + pickup.w and player.y + player.h / 2 > pickup.y and player.y < pickup.y + pickup.h:

                                if pickup.type == "coin":
                                    player.coin_count += 1

                                index.pick_up = None

                            if pickup.type == "coin":
                                init_image_bounds(pickup, 0, 5)

                            if pickup.type == "shroom-0":
                                init_image_bounds(pickup, 0, 9)

                        # Init animation for block else will continue animation
                        if not index.started_imageloop:
                            # if index.pick_up is not None:
                            #     init_image_bounds(index, 0, 10)
                            # else:
                            if index.block_type == "brick":
                                init_image_bounds(index, 0, 1)
                            else:
                                init_image_bounds(index, 11, 11)
                            run_through_block_images(index)

                        else:
                            run_through_block_images(index)
                            pass
                except AttributeError:
                    pass
                if index.x + index.w > -5 and index.x < winW:
                    # Render objects here
                    if index.w > 32 or index.h > 32:
                        win.blit(index.background, (index.x, index.y),
                                 (index.image_x * 32, index.image_y * 32, index.w, index.h))
                    else:
                        win.blit(index.background, (index.x, index.y),
                                 (index.image_x * index.w, index.image_y * index.h, index.w, index.h))
        else:
            # Render enemies here
            for enemy in i:
                if enemy.x + enemy.w > -5 and enemy.x < winW:
                    win.blit(enemy.images, (enemy.x, enemy.y),
                             (enemy.image_x * enemy.w, enemy.image_y * enemy.h, enemy.w, enemy.h))


# ////////////  END RENDER WORLD

setup()

while run:
    CLOCK.tick(FPS)

    player_hit_camerabounds = player.x >= (winW / 2) - player.w

    # Check controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    render_world()

    gravity()
    check_key(keys)
    run_through_player_images()

    # Show Player
    win.blit(player.images, (player.x, player.y),
             (player.image_x * player.w, player.image_y * player.h, player.w, player.h))

    pygame.display.update()

pygame.quit()
