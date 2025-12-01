import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    #Groups
    updatable = pygame.sprite.Group()
    drawable =pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers =(asteroids, updatable, drawable)  
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    '''# Background
    image = pygame.image.load('assets/background.png')
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    Background(image, (drawable,))     # nur drawbar, nicht updatebar'''

    #Background Picture Alternative 2
    # Load image
    image = pygame.image.load('assets/background.png')
    # Scale image
    scaled_image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Blit=> Zeichnet image to the display
    screen.blit(scaled_image, (0, 0))
    # Update the display
    pygame.display.update()

    # Create Player
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)   
    asteroidfield = AsteroidField()



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

        pygame.display.flip()


if __name__ == "__main__":
    main()
