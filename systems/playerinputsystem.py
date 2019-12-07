import numpy as np
pygame = None

def run(players):
    """ Applys player input to ship """
    k = pygame.key.get_pressed()

    for player in players:
        if k[pygame.K_w]: # Jet forward
            player.vx += np.cos(player.theta)
            player.vy += np.sin(player.theta)

        if k[pygame.K_a]: # Rotate left
            player.theta -= 0.12

        if k[pygame.K_d]: # Rotate right
            player.theta += 0.12

        if k[pygame.K_SPACE]: # Fire lasers
            player.fire = True
