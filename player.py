from circleshape import CircleShape
from constants import PLAYER_RADIUS

class Player(CircleShape):
    def __init__(self, x_pos: int, y_pos: int) -> None:
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