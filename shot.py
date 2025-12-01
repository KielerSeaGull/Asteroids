import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_SHOT_SPEED

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "White", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity *  dt 