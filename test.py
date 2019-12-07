import numpy as np
from tqdm import tqdm
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

playerinputsystem.pygame = pygame

hitdestroysystem.screen = screen


## INITIALIZE GAME OBJECTS
asteroids = [asteroid(x,y,10,10,vx,vy) for x, y,vx,vy in zip(np.random.random(10) * 600, np.random.random(10) * 400, np.random.randn(10), np.random.randn(10))]
players = [ship( WIDTH/2, HEIGHT/2)] # Spawn player in the dead center
lasers = []

def events():
    global mainloop # Access the global mainloop variable

    # Here is where the interaction happens: state is gathered and actions are taken

def loop():
    global mainloop # Access the global mainloop variable

    # Create
    asteroidsplitsystem.run(asteroids)
    newlasers = firelasersystem.run(players)
    lasers.extend(newlasers)

    # Destroy
    hitdestroysystem.run(players)
    if len(players) == 0:
        mainloop = False
        return

    hitdestroysystem.run(asteroids)
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
t_loop = tqdm()
while mainloop:
    iter += 1
    milliseconds = clock.tick() # Time how long the frame took
    playtime += milliseconds / 1000.0

    events() # compute actions
    loop() # change state
    render() # print to screen

    t_loop.set_description("Run time: {}, Clock time: {}".format(iter / 30, playtime))

pygame.quit()
print("This simulation was run for {0:.2f} seconds".format(playtime))
print("Average framerate: {0:.2f} frames per second".format(iter /  playtime))
