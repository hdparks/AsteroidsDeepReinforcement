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

def events():
    global mainloop # Access the global mainloop variable

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print("QUIT!!")
            mainloop = False # pygame window closed by user

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                print("ESCAPE!")
                mainloop = False # User pressed ESC

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

    # Plan
    playerinputsystem.run(players)

    # Move
    shipdragsystem.run(players)
    movesystem.run(asteroids + players + lasers)
    treadmillsystem.run(asteroids + players)

    # Collide
    shipcollisionsystem.run(players, asteroids)
    lasercollisionsystem.run(lasers, asteroids)



def render():
    text = str(playtime)
    pygame.display.set_caption(text) # Print framerate in titlebar

    # Blitting stage
    blitsystem.run(asteroids + players + lasers)

    # Redraw stage
    drawlinessystem.run(lasers)
    drawsystem.run(asteroids + players)

    pygame.display.flip()

iter = 0
while mainloop:
    iter += 1
    milliseconds = clock.tick(FPS) # Does not go faster than FPS cap
    playtime += milliseconds / 1000.0

    events() # compute actions
    loop() # change state
    render() # print to screen

pygame.quit()
print("This game was played for {0:.2f} seconds".format(playtime))
print("Average framerate: {0:.2f} frames per second".format(iter /  playtime))
