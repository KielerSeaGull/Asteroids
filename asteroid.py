import pygame, random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTROID_RND_ANGLES, RENDER_SPACE_BETWEEN_LINES, RENDER_LINE_HIGHT

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # how often can the Astroid split determines the lvl
        self.lvl = self.radius // ASTEROID_MIN_RADIUS
    
    def draw(self, screen):
        pygame.draw.circle(screen, "White", self.position, self.radius, LINE_WIDTH)
        self.draw_lvl(screen)
    
    def update(self, dt: float):
        self.position += self.velocity * dt 
    
    def draw_lvl(self, screen) -> None:
        center_x = self.position[0]
        center_y = self.position[1]

        # gerade Zahlen
        if self.get_lvl() % 2 == 0:
            for i in range(1,self.get_lvl()+1):
                positions: list[tuple] = []
                #(-1)**i ==> alterniert zwischen - (links) und + (rechts) vom center
                # center + halber Abstand dann in Abhängigkeit von i (lvl) wie oft der Abstand kommen muss
                my_pos_x = center_x + ((RENDER_SPACE_BETWEEN_LINES//2) + ((i-1)//2) * RENDER_SPACE_BETWEEN_LINES) * (-1)**i

                # halbe linie nach unten und oben von centerhöhe zeichnen
                # j in range(i,i+2) macht, dass wir immer auf der gleichen Höhe wie zuvor sind
                for j in range(i,i+2):
                    my_pos_y = center_y + ((self.get_lvl() * RENDER_LINE_HIGHT)//2) * (-1)**j
                    positions.append((my_pos_x, my_pos_y))
                pygame.draw.line(screen, "White", positions[0], positions[1],LINE_WIDTH)


        # ungerade Zahlen
        else:
            for i in range(1,self.get_lvl()+1):
                positions: list[tuple] = []
                #(-1)**i ==> alterniert zwischen - (links) und + (rechts) vom center
                # center + in Abhängigkeit von i (lvl) wie oft der Abstand kommen muss
                my_pos_x = center_x + ((i//2) * RENDER_SPACE_BETWEEN_LINES) * (-1)**i

                # halbe linie nach unten und oben von centerhöhe zeichnen
                # j in range(i,i+2) macht, dass wir immer auf der gleichen Höhe wie zuvor sind
                for j in range(i,i+2):
                    my_pos_y = center_y + ((self.get_lvl() * RENDER_LINE_HIGHT)//2) * (-1)**j
                    positions.append((my_pos_x, my_pos_y))
                pygame.draw.line(screen, "White", positions[0], positions[1],LINE_WIDTH)



    def split(self):
        self.kill()
        random_angle: float = random.randrange(ASTROID_RND_ANGLES[0],ASTROID_RND_ANGLES[1])
        astroid1 = Asteroid(self.position[0], self.position[1], (self.lvl-1)*ASTEROID_MIN_RADIUS)
        astroid1.velocity = 1.3 * self.velocity
        astroid1.velocity.rotate_ip(random_angle)

        astroid2 = Asteroid(self.position[0], self.position[1], (self.get_lvl()-1)*ASTEROID_MIN_RADIUS)
        astroid2.velocity = 1.0 * self.velocity
        astroid2.velocity.rotate_ip(-random_angle)

        #self.kill()

    def get_lvl(self) -> int:
        return self.lvl

         


