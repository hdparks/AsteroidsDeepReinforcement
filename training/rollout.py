import numpy as np
from tqdm import tqdm
import pygame

import systems.blitsystem as blitsystem
import systems.movesystem as movesystem
import systems.treadmillsystem as treadmillsystem
import systems.drawsystem as drawsystem
import systems.drawlinessystem as drawlinessystem
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

def rollout(policy_network):

    pygame.init() # Initialize pygame

    WIDTH, HEIGHT = 200,200

    screen = pygame.Surface((WIDTH,HEIGHT)) # Set screen size of pygame window
    background = pygame.Surface((WIDTH + 50, HEIGHT + 50 )) # Create empty pygame surface
    background.fill((255,255,255)) # Fill with white
    background = background.convert(screen) # Convert surface to make blitting faster
    screen.blit(background, (0,0)) # Copy background onto screen
    clock = pygame.time.Clock() # Create Pygame clock object

    mainloop = True

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

    hitdestroysystem.screen = screen


    ## INITIALIZE GAME OBJECTS
    asteroids = [asteroid(x,y,10,10,vx,vy) for x, y,vx,vy in zip(np.random.random(10) * 600, np.random.random(10) * 400, np.random.randn(10), np.random.randn(10))]
    players = [ship( WIDTH/2, HEIGHT/2)] # Spawn player in the dead center
    lasers = []


    # These are used to define the rollout, and are what will be returned
    rollout = []
    asteroids_destroyed = 0
    reward_bank = 0
    prev_screen = None

    def events(iter):
        nonlocal mainloop # Access the global mainloop variable
        nonlocal prev_screen
        nonlocal reward_bank

        # Here is where the interaction happens: state is gathered and actions are taken


        # On the first round, do nothing (policy network needs information from 2 frames)
        current_screen = pygame.surfarray.array2d(screen)

        if iter == 0:
            prev_screen = current_screen

        state = np.array([ current_screen, prev_screen])  # Current state is the last two frames
        prev_screen = current_screen

        action, a_dist = policy_network.get_action(state) # Returns an array of probabilities size = action space
        # Draw from the action_dist to get the action
        rollout.append((state,action,a_dist,reward_bank)) # reward = 0,
        reward_bank = 0
        # Take action
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
        nonlocal asteroids_destroyed
        nonlocal reward_bank

        # Create
        asteroidsplitsystem.run(asteroids)
        newlasers = firelasersystem.run(players)
        lasers.extend(newlasers)

        # Destroy
        hitdestroysystem.run(players)
        if len(players) == 0:
            mainloop = False
            return

        k = hitdestroysystem.run(asteroids)
        asteroids_destroyed += k
        reward_bank += k

        if len(asteroids) == 0:
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

        # Blitting stage
        blitsystem.run(asteroids + players + lasers)

        # Redraw stage
        drawlinessystem.run(lasers)
        drawsystem.run(asteroids + players)


    iter = 0
    # t_loop = tqdm()

    while mainloop:
        milliseconds = clock.tick() # Time how long the frame took
        playtime += milliseconds / 1000.0

        events(iter) # compute actions
        loop() # change state
        render() # print to screen

        # t_loop.set_description("Run time: {}, Clock time: {}".format(iter / 30, playtime))
        iter += 1

        if len(players) == 0 or len(asteroids) == 0:
            break


    pygame.quit()

    # Update final rollout entry
    s,a,a_dist,r = rollout[-1]
    r = -10 if len(asteroids) > 0 else 1 # Reward
    rollout[-1] = (s,a,a_dist,r)


    # print()
    # print("This simulation was run for {0:.2f} seconds".format(playtime))
    # print("Average framerate: {0:.2f} frames per second".format(iter /  playtime))

    return rollout, asteroids_destroyed, playtime, iter / playtime
