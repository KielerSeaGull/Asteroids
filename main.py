import pygame
import sys
from logger import log_state, log_event
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()

    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Auto-Registrierung in Gruppen
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # Fullscreen auf Monitor 0 (ggf. ändern)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0)
    W, H = screen.get_size()

    # Hintergrund laden
    bg_img = pygame.image.load('assets/background.png')
    bg_img = pygame.transform.scale(bg_img, (W, H))

    # Fonts und UI
    font = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)
    restart_rect = pygame.Rect(W // 2 - 220, H // 2 + 20, 200, 54)
    quit_rect    = pygame.Rect(W // 2 +  20, H // 2 + 20, 200, 54)

    # Game-State
    game_over = False

    def start_new_round():
        # Alles zurücksetzen und neue Objekte erzeugen
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        p = Player(W / 2, H / 2)
        af = AsteroidField(W, H)
        return p, af

    # Erststart
    player, asteroidfield = start_new_round()

    clock = pygame.time.Clock()
    dt = 0.0

    # Hilfsfunktion: Screen-Wrapping mit Radius
    def wrap_with_radius(pos, w, h, r):
        pos[0] = (pos[0] + r) % (w + 2 * r) - r
        pos[1] = (pos[1] + r) % (h + 2 * r) - r

    # Game-Loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Neustart per Mausklick auf Button
            if game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    log_event("restart_clicked")
                    player, asteroidfield = start_new_round()
                    game_over = False
                elif quit_rect.collidepoint(event.pos):
                    log_event("quit_clicked")
                    pygame.quit()
                    sys.exit()

            # Optional: Neustart per Taste R
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                log_event("restart_key")
                player, asteroidfield = start_new_round()
                game_over = False

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                log_event("escape_key")
                pygame.quit()
                sys.exit()

        dt = clock.tick(60) / 1000.0

        # Update nur, wenn nicht Game Over (Szene „friert“ ein)
        if not game_over:
            updatable.update(dt)

            # Kollisionen
            player_hit = False
            for asteroid in list(asteroids):
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_over = True
                    player_hit = True
                    break

                for shot in list(shots):
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        if asteroid.get_lvl() > 1:
                            log_event("asteroid_split")
                            asteroid.split()
                        else:
                            asteroid.kill()
                        shot.kill()

            # Wrapping (Modulo), nur für Entities, die wrappen sollen
            if not player_hit:
                for circle in updatable:
                    if isinstance(circle, (Shot, AsteroidField)):
                        continue
                    r = getattr(circle, "radius", 0)
                    wrap_with_radius(circle.position, W, H, r)

        # Render
        screen.blit(bg_img, (0, 0))
        for sprite in drawable:
            sprite.draw(screen)

        if game_over:
            # halbtransparentes Overlay
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            # Game Over Text
            t = font.render("Game Over", True, (255, 255, 255))
            screen.blit(t, (W // 2 - t.get_width() // 2, H // 2 - 100))

            #Button „Nochmal?“
            pygame.draw.rect(screen, (240, 240, 240), restart_rect)
            pygame.draw.rect(screen, (60, 60, 60), restart_rect, 2)
            label_restart = font_small.render("Nochmal?", True, (0, 0, 0))
            screen.blit(label_restart, (
            restart_rect.centerx - label_restart.get_width() // 2,
            restart_rect.centery - label_restart.get_height() // 2
            ))

            #Button „Beenden“
            pygame.draw.rect(screen, (240, 240, 240), quit_rect)
            pygame.draw.rect(screen, (60, 60, 60), quit_rect, 2)
            label_quit = font_small.render("Beenden", True, (0, 0, 0))
            screen.blit(label_quit, (
            quit_rect.centerx - label_quit.get_width() // 2,
            quit_rect.centery - label_quit.get_height() // 2
            ))

            # Hinweis auf Taste R
            hint = font_small.render("Drücke R für Neustart", True, (220, 220, 220))
            screen.blit(hint, (W // 2 - hint.get_width() // 2, H // 2 + 90))

        pygame.display.flip()

if __name__ == "__main__":
    main()