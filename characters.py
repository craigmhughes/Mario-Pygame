import pygame


class mario:
    # Player variables
    x = 100
    y = 400
    w = 48
    h = 64
    s = 3

    image_x = 0
    image_y = 0

    image_start_bounds = 0
    image_end_bounds = 0

    image_time = pygame.time.get_ticks()
    images = pygame.image.load("assets/sprites/mario-sprites.png")
    images = pygame.transform.scale(images, (432, 1152))
    image_right = images
    image_left = pygame.transform.flip(images, True, False)
    started_imageloop = False

    is_left = False
    is_idle = False
    is_walk = False

    # Collision - List goes: L R T B
    collision = [False, False, False, False]

    last_jump = 0

    coin_count = 0
    jumpcount = 0
    is_jump = False

    parent = None

    def __init__(self):
        mario.parent = self


class enemy:
    # Location variables
    x = 100
    y = 400
    w = 48
    h = 64
    s = 1.5

    vel = 1.5

    enemy_type = None
    player = None

    image_x = 0
    image_y = 0

    image_start_bounds = 0
    image_end_bounds = 0

    image_time = pygame.time.get_ticks()
    images = pygame.image.load("assets/sprites/mario-sprites.png")
    images = pygame.transform.scale(images, (432, 1152))
    image_right = images
    image_left = pygame.transform.flip(images, True, False)
    started_imageloop = False
    left_count = 0

    is_left = False
    is_idle = False
    is_walk = False

    world = None

    # Collision - List goes: L R T B
    collision = [False, False, False, False]

    last_jump = 0

    coin_count = 0
    jumpcount = 0
    is_jump = False

    is_patrolling = False
    following_player = False
    found_gap = False

    time_since_follow = pygame.time.get_ticks()

    def __init__(self, enemy_type, x, y, world):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.world = world

    def ai(self):
        # Basic AI, TODO: animate
        self.run_through_images()

        if pygame.time.get_ticks() > self.time_since_follow + 6000 and not self.following_player:
            self.is_patrolling = True
            self.time_since_follow = pygame.time.get_ticks()

        self.detect_player(self.player)
        if self.is_patrolling and not self.following_player:
            self.patrol()

    def init_image_bounds(self, start, end):
        if not self.started_imageloop:
            self.image_x = start
        self.image_start_bounds = start
        self.image_end_bounds = end

    def detect_player(self, player):
        hit_y = self.y + 50 > player.y >= self.y - 50

        # Relative X's = actual x value will normally be half of screen --\
        # this gets the distance between the first ground piece and player/enemy
        player_rel_x = int(self.world[0][0].x + player.x)
        self_rel_x = int(self.world[0][0].x + self.x)

        if self_rel_x < player_rel_x < self_rel_x + 100 and hit_y:
            self.following_player = True
            self.is_patrolling = False

            if self_rel_x + self.w > player_rel_x - 10 or self.found_gap:
                self.s = 0
                self.is_walk = False
                self.flip_direction(1, True)
                self.image_y = 0
                self.init_image_bounds(0, 0)
            else:
                self.x += self.vel
                self.is_walk = True
                self.image_y = 3
                self.init_image_bounds(0, 6)

        elif self_rel_x > player_rel_x > self_rel_x - 100 and hit_y:
            self.following_player = True

            if player_rel_x + player.w - (self.w / 2) < self_rel_x <= player_rel_x + player.w + 10 or self.found_gap:
                self.s = 0
                self.is_walk = False
                self.flip_direction(0, True)
                self.image_y = 0
                self.init_image_bounds(0, 0)
            else:
                self.x -= self.vel
                self.is_walk = True
                self.image_y = 3
                self.init_image_bounds(2, 8)

        else:
            self.following_player = False

            if self.is_patrolling:
                self.s = self.vel * -1 if self.is_left else self.vel
                self.is_walk = True

                self.image_y = 3
                if self.is_left:
                    self.flip_direction(0, True)
                    self.init_image_bounds(2, 8)
                else:
                    self.flip_direction(1, True)
                    self.init_image_bounds(0, 6)
            else:
                self.s = 0
                self.is_walk = False
                if self.is_left:
                    self.flip_direction(0, True)
                self.image_y = 0
                self.init_image_bounds(0, 0)

        self.detect_ground()

    def detect_ground(self):
        world = self.world
        self.found_gap = False

        for ground in world[0]:
            # Check last piece of ground
            if world[0].index(ground) == len(world[0]) - 1 and (
                    ground.x + ground.w - self.w < self.x < ground.x + ground.w):
                self.flip_direction(1, False)
                self.found_gap = True
                self.x -= 5


            # Check first ground
            if world[0].index(ground) == 0 and (ground.x + 5 > self.x < ground.x + ground.w):
                self.flip_direction(0, False)
                self.found_gap = True
                self.x += 5

            # Check next piece of ground
            if world[0].index(ground) + 1 < len(world[0]):
                adj_ground = world[0][world[0].index(ground) + 1]

                if adj_ground.x >= ground.x + ground.w + 15 and (
                        ground.x + ground.w - self.w < self.x < ground.x + ground.w):
                    self.x -= 5
                    self.flip_direction(1, False)
                    self.found_gap = True


            # Check previous
            if world[0].index(ground) - 1 >= 0:
                adj_ground = world[0][world[0].index(ground) - 1]

                if adj_ground.x + adj_ground.w <= ground.x - 15 and ground.x < self.x < ground.x + 15:
                    self.flip_direction(0, False)
                    self.found_gap = True
                    self.x += 5

            if self.found_gap:
                self.following_player = False
                self.s = 0

    def patrol(self):
        if self.collision[3]:
            self.x += self.s
            self.is_walk = True
            if self.is_left:
                self.init_image_bounds(2, 8)
            else:
                self.init_image_bounds(0, 6)
            self.image_y = 3
        else:
            self.is_walk = False

        self.detect_ground()

    def flip_direction(self, dir, look):
        # Look variable determines whether character will move with direction or just look there
        if not look:
            if dir == 0:
                self.s *= -1
                self.is_left = False
                self.init_image_bounds(0, 6)
                self.images = self.image_right
                self.image_y = 3
            else:
                self.s *= -1
                self.is_left = True
                self.init_image_bounds(2, 8)
                self.images = self.image_left
                self.image_y = 3
        else:
            if dir == 0:
                self.images = self.image_left
                self.init_image_bounds(2, 8)
            else:
                self.is_left = False
                self.images = self.image_right

    def run_through_images(self):

        # Increment imageCounts per Sec
        if pygame.time.get_ticks() > self.image_time + 1000 or \
                pygame.time.get_ticks() > self.image_time + 100 and self.is_walk:

            self.image_time = pygame.time.get_ticks()

            # Reset image count based on boundary
            if self.image_x >= self.image_end_bounds:
                self.image_x = self.image_start_bounds
            else:
                self.started_imageloop = True
                self.image_x += 1