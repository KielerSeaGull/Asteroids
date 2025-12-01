import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_hight: int):
        super().__init__(self.containers)

        self.screen_width = screen_width
        self.screen_hight = screen_hight
        self.spawn_timer = 0.0

        self.edges = [
            [
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS,
                                         y * self.screen_hight),
            ],
            [
                pygame.Vector2(-1, 0),
                lambda y: pygame.Vector2(self.screen_width + ASTEROID_MAX_RADIUS,
                                         y * self.screen_hight),
            ],
            [
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(x * self.screen_width,
                                         -ASTEROID_MAX_RADIUS),
            ],
            [
                pygame.Vector2(0, -1),
                lambda x: pygame.Vector2(x * self.screen_width,
                                         self.screen_hight + ASTEROID_MAX_RADIUS),
            ],
        ]

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)