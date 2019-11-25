import numpy as np
import pygame
import dirtysystem
import blitsystem
import movesystem
import treadmillsystem
import drawsystem
import playerinputsystem
import shipcollisionsystem
import shipdragsystem

from ship import ship
from asteroid import asteroid

pygame.init() # Initialize pygame

WIDTH, HEIGHT = 200,200

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Set screen size of pygame window
background = pygame.Surface(screen.get_size()) # Create empty pygame surface
background.fill((255,255,255)) # Fill with white
background = background.convert() # Convert surface to make blitting faster
screen.blit(background, (0,0)) # Copy background onto screen
clock = pygame.time.Clock() # Create Pygame clock object

mainloop = True
FPS = 30 # Desired framerate

playtime = 0.0 # Tracks how long the game has been played

# Initialize system variables
dirtysystem.WIDTH = WIDTH
dirtysystem.HEIGHT = HEIGHT
dirtysystem.background = background

blitsystem.screen = screen

treadmillsystem.WIDTH = WIDTH
treadmillsystem.HEIGHT = HEIGHT

drawsystem.pygame = pygame
drawsystem.screen = screen

playerinputsystem.pygame = pygame


## INITIALIZE GAME OBJECTS
asteroids = [asteroid(x,y,10,10,None,vx,vy) for x, y,vx,vy in zip(np.random.random(10) * 600, np.random.random(10) * 400, np.random.randn(10), np.random.randn(10))]
player = ship(WIDTH/2, HEIGHT/2) # Spawn player in the center


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

    playerinputsystem.run(player)
    shipdragsystem.run(player)
    dirtysystem.run(asteroids + [player])
    movesystem.run(asteroids  + [player])
    treadmillsystem.run(asteroids + [player])

    if shipcollisionsystem.run(player, asteroids):
        mainloop = False


def render():
    text = "FPS: {0:.2f}    Playtime: {1:.2f}".format(clock.get_fps(),playtime)
    pygame.display.set_caption(text) # Print framerate in titlebar

    # Blitting stage
    blitsystem.run(asteroids + [player])

    # Redraw stage
    drawsystem.run(asteroids + [player])


while mainloop:
    milliseconds = clock.tick(FPS) # Does not go faster than FPS cap
    playtime += milliseconds / 1000.0


    events() # compute actions
    loop() # change state
    render() # print to screen

pygame.quit()
print("This game was played for {0:.2f} seconds".format(playtime))
