import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH

class Player(CircleShape):
    def __init__(self, x_pos: float, y_pos: float) -> None:
        super().__init__(x_pos, y_pos, PLAYER_RADIUS)
        self.rotation: float = 0.0

    # Zeichnet den Spieler als Dreieck, obwohl Hitbox Dreieck
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        
