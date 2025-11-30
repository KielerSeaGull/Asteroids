import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import *

def main():
    
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    updatable = pygame.sprite.Group()
    drawable =pygame.sprite.Group()
    # Create Player
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)   

    #Background Picture
    # Load image
    image = pygame.image.load('assets/background.png')
    # Scale image
    scaled_image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Blit image to the display
    screen.blit(scaled_image, (300, 250))
    # Update the display
    pygame.display.update()

    gameclock = pygame.time.Clock()
    dt: float = 0.0
    #Game-Loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #screen.fill("black")
        screen.blit(scaled_image, (0, 0))
        #pygame.display.update()
        # updates PlayerPosition
        player.update(dt)
        #### player gets renderd
        player.draw(screen)
        pygame.display.flip()
        # wartet 1/60 Sekunde <==> bestcase: 60FPS (Grenze nach oben)
        gameclock.tick(60)
        #Umrechnung von Millisek -> Sek
        dt = gameclock.tick(60)/1000


if __name__ == "__main__":
    main()
