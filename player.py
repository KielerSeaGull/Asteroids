import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED

class Player(CircleShape):
    def __init__(self, x_pos: float, y_pos: float) -> None:
        super().__init__(x_pos, y_pos, PLAYER_RADIUS)
        self.rotation: float = 0.0

    # Eckpunkte eines Dreiecks mithilfe des Kreisradius bestimmen
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    # Zeichnet den Spieler als Dreieck, obwohl Hitbox Dreieck
    def draw(self, screen):
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    
    def rotate(self, delta_time: float):
         self.rotation += delta_time * PLAYER_TURN_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)
