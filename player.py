import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, SHOT_RADIUS, LINE_WIDTH, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
    def __init__(self, x_pos: float, y_pos: float) -> None:
        super().__init__(x_pos, y_pos, PLAYER_RADIUS)
        self.rotation: float = 0.0
        self.cooldown: float = 0.0

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

    def move(self, delta_time: float):
         unit_vector = pygame.Vector2(0,1)
         rotated_vector = unit_vector.rotate(self.rotation)
         rotated_vector_with_speed = rotated_vector * PLAYER_SPEED * delta_time
         self.position += rotated_vector_with_speed

    def shoot(self):
         shot = Shot(self.position[0], self.position[1], SHOT_RADIUS)
         unit_vector = pygame.Vector2(0,1)
         rotated_unit_v = unit_vector.rotate(self.rotation)
         shot.velocity = rotated_unit_v * PLAYER_SHOT_SPEED
    
    def set_cooldown(self, cooldown_sec: float) -> None:
        self.cooldown = cooldown_sec       

    
# Key Binding- hier wird abgerufen was passieren soll, wenn der jeweilige 
# Knopf gedrückt wird
    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            #Wenn kein Cooldown vorhanden, stelle Cooldown ein und schieße
            if self.cooldown <= 0:
             self.set_cooldown(PLAYER_SHOOT_COOLDOWN_SECONDS)
             self.shoot()
            
