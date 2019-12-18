import numpy as np
import pygame
import systems.blitsystem as blitsystem
import systems.movesystem as movesystem
import systems.treadmillsystem as treadmillsystem
import systems.drawsystem as drawsystem
import systems.drawlinessystem as drawlinessystem
import systems.playerinputsystem as playerinputsystem
import systems.shipcollisionsystem as shipcollisionsystem
import systems.shipdragsystem as shipdragsystem
import systems.firelasersystem as firelasersystem
import systems.lasercollisionsystem as lasercollisionsystem
import systems.hitdestroysystem as hitdestroysystem
import systems.laserclearsystem as laserclearsystem
import systems.asteroidsplitsystem as asteroidsplitsystem

from entities.ship import ship
from entities.asteroid import asteroid
from entities.laser import laser

def visualize(network):
    pygame.quit()
    pygame.init() # Initialize pygame

    WIDTH, HEIGHT = 200,200

    screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Set screen size of pygame window
    background = pygame.Surface((WIDTH + 50, HEIGHT + 50 )) # Create empty pygame surface
    background.fill((255,255,255)) # Fill with white
    background = background.convert() # Convert surface to make blitting faster
    screen.blit(background, (0,0)) # Copy background onto screen
    clock = pygame.time.Clock() # Create Pygame clock object

    mainloop = True
    FPS = 30 # Desired framerate

    playtime = 0.0 # Tracks how long the game has been played

    # Initialize system variables
    blitsystem.screen = screen
    blitsystem.background = background

    treadmillsystem.WIDTH = WIDTH
    treadmillsystem.HEIGHT = HEIGHT

    laserclearsystem.WIDTH = WIDTH
    laserclearsystem.HEIGHT = HEIGHT

    drawsystem.pygame = pygame
    drawsystem.screen = screen
    drawsystem.background = background

    drawlinessystem.pygame = pygame
    drawlinessystem.screen = screen
    drawlinessystem.background = background

    playerinputsystem.pygame = pygame

    hitdestroysystem.screen = screen


    ## INITIALIZE GAME OBJECTS
    asteroids = [asteroid(x,y,10,10,vx,vy) for x, y,vx,vy in zip(np.random.random(10) * 600, np.random.random(10) * 400, np.random.randn(10), np.random.randn(10))]
    players = [ship( WIDTH/2, HEIGHT/2)] # Spawn player in the dead center
    lasers = []

    prev_screen = None
    def events(iter):
        nonlocal mainloop # Access the global mainloop variable
        nonlocal prev_screen

        current_screen = pygame.surfarray.array2d(screen)

        if iter == 0:
            prev_screen = current_screen

        state = np.array([ current_screen, prev_screen])
        prev_screen = current_screen

        action, _ = network.get_action(state)

        player = players[0]
        if action[0]: # Jet forward
            player.vx += np.cos(player.theta)
            player.vy += np.sin(player.theta)

        if action[1]: # Rotate left
            player.theta -= 0.12

        if action[2]: # Rotate right
            player.theta += 0.12

        if action[3]: # Fire lasers
            player.fire = True

    def loop():
        nonlocal mainloop # Access the global mainloop variable

        # Create
        asteroidsplitsystem.run(asteroids)
        newlasers = firelasersystem.run(players)
        lasers.extend(newlasers)

        # Destroy
        p = hitdestroysystem.run(players)
        if len(players) == 0:
            print("Player was hit...")
            mainloop = False
            return

        hitdestroysystem.run(asteroids)
        if len(asteroids) == 0:
            print("All asteroids cleared")
            mainloop = False
            return

        hitdestroysystem.run(lasers)
        laserclearsystem.run(lasers)


        # Move
        shipdragsystem.run(players)
        movesystem.run(asteroids + players + lasers)
        treadmillsystem.run(asteroids + players)

        # Collide
        shipcollisionsystem.run(players, asteroids)
        lasercollisionsystem.run(lasers, asteroids)



    def render():
        text = "{:.2f}".format(playtime)
        pygame.display.set_caption(text) # Print framerate in titlebar

        # Blitting stage
        blitsystem.run(asteroids + players + lasers)

        # Redraw stage
        drawlinessystem.run(lasers)
        drawsystem.run(asteroids + players)

        pygame.display.flip()

    iter = 0
    while mainloop:
        pygame.event.pump()

        milliseconds = clock.tick(FPS) # Does not go faster than FPS cap
        playtime += milliseconds / 1000.0
        events(iter) # compute actions
        loop() # change state
        render() # print to screen
        iter += 1

    pygame.quit()
    print("This game was played for {0:.2f} seconds".format(playtime))
    print("Average framerate: {0:.2f} frames per second".format(iter /  playtime))
