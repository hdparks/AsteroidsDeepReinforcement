import numpy as np
pygame = None

def run(player):
    """ Applys player input to ship """
    k = pygame.key.get_pressed()

    if k[pygame.K_w]: # Forward pressed
        player.vx += np.cos(player.theta)
        player.vy += np.sin(player.theta)

    if k[pygame.K_a]: # Rotate left
        player.theta -= 0.12

    if k[pygame.K_d]: # Rotate right
        player.theta += 0.12
