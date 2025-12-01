import pygame, random, math
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTROID_RND_ANGLES, RENDER_SPACE_BETWEEN_LINES, RENDER_LINE_HIGHT

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # how often can the Astroid split determines the lvl
        self.lvl = self.radius // ASTEROID_MIN_RADIUS
        self.facing_angle: float = random.uniform(0,360)
        self.num_tips = random.randint(3,8)
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "White", self.star(self.num_tips))
        self._draw_lvl_marks(screen)
    
    def update(self, dt: float):
        self.position += self.velocity * dt 
    
    def _draw_lvl_marks(self, screen) -> None:
        center_x, center_y = self.position
        lvl = self.get_lvl()
        half_height = (lvl * RENDER_LINE_HIGHT) // 2

        for i in range(1, lvl + 1):
            # direction: -1 for left, +1 for right, alternating
            direction = (-1) ** i

            if lvl % 2 == 0:
                # even level count: use half-offset + (i-1)//2
                step = (RENDER_SPACE_BETWEEN_LINES // 2) + ((i - 1) // 2) * RENDER_SPACE_BETWEEN_LINES
            else:
                # odd level count: pure multiples of spacing
                step = (i // 2) * RENDER_SPACE_BETWEEN_LINES

            my_pos_x = center_x + direction * step

            # vertical endpoints: always symmetric around center
            y1 = center_y - half_height
            y2 = center_y + half_height

            pygame.draw.line(screen, "Red", (my_pos_x, y1), (my_pos_x, y2), LINE_WIDTH)

    def _nice_inner_ratio(self, num_tips:int) -> float:
        return math.sin(math.pi / (2 * num_tips)) / math.sin(3 * math.pi / (2 * num_tips))

    # Eckpunkte eines Dreiecks mithilfe des Kreisradius bestimmen
    def star(self, num_tips: int, inner_ratio: float | None = None):
        if inner_ratio is None:
            inner_ratio = self._nice_inner_ratio(num_tips)
    
        points = []
        angle_step = 360 / (num_tips * 2)

        for i in range(num_tips * 2):
            # abwechselnd äußerer/innerer Radius
            r = self.radius if i % 2 == 0 else self.radius * inner_ratio
            angle = self.facing_angle + i * angle_step

            # Einheit in x-Richtung und dann drehen
            v = pygame.Vector2(1, 0).rotate(angle) * r
            points.append(self.position + v)

        return points

    def split(self):
        self.kill()
        random_angle: float = random.randrange(ASTROID_RND_ANGLES[0],ASTROID_RND_ANGLES[1])

        astroid1 = Asteroid(self.position[0], self.position[1], (self.lvl-1)*ASTEROID_MIN_RADIUS)
        astroid1.velocity = 1.3 * self.velocity
        astroid1.velocity.rotate_ip(random_angle)

        astroid2 = Asteroid(self.position[0], self.position[1], (self.get_lvl()-1)*ASTEROID_MIN_RADIUS)
        astroid2.velocity = 1.0 * self.velocity
        astroid2.velocity.rotate_ip(-random_angle)

    def get_lvl(self) -> int:
        return self.lvl

         


