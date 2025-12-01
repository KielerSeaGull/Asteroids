import pygame
import sys
#from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()

    #Groups
    updatable = pygame.sprite.Group()
    drawable =pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers =(asteroids, updatable, drawable)  
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # Fullscreen on second monitor
    screen = pygame.display.set_mode(
        (0, 0),
        pygame.FULLSCREEN,
        display=0   # <-- change to the monitor index you want
    )

    default_screen_size = screen.get_size()
    # Load image
    image = pygame.image.load('assets/background.png')
    # Scale image
    scaled_image = pygame.transform.scale(image, default_screen_size)
    # Blit=> Zeichnet image to the display
    screen.blit(scaled_image, (0, 0))
    # Update the display
    pygame.display.update()

    # Create Player
    player = Player(default_screen_size[0]/2, default_screen_size[1]/2)   
    asteroidfield = AsteroidField(default_screen_size[0], default_screen_size[1])

    gameclock = pygame.time.Clock()
    dt: float = 0.0

    #Game-Loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    
        # wartet 1/60 Sekunde <==> bestcase: 60FPS (Grenze nach oben)
        #Umrechnung von Millisek -> Sek
        dt = gameclock.tick(60)/1000

        #updatet Positionen von allen Objekten
        updatable.update(dt)

         # Hintergrund zeichnen
        screen.blit(scaled_image, (0, 0))

        #Rendert die zu rendernden Objekte
        for sprite in drawable:
            sprite.draw(screen)
        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    if asteroid.get_lvl() > 1:
                        log_event("asteroid_split")
                        asteroid.split()
                    else:
                        asteroid.kill()
                    shot.kill()

        for circle in updatable:
            if isinstance(circle, (Shot, AsteroidField)):
                continue
            my_x, my_y = circle.position

            if my_x - circle.radius >= default_screen_size[0]:
                circle.position[0] = 0
            elif my_x + circle.radius <= 0:
                circle.position[0] = default_screen_size[0]
            if my_y - circle.radius >= default_screen_size[1]:
                circle.position[1] = 0
            elif my_y + circle.radius <= 0:
                circle.position[1] = default_screen_size[1]





        pygame.display.flip()


if __name__ == "__main__":
    main()
