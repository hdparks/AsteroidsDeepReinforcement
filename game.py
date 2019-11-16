import numpy as np
import pygame
pygame.init() # Initialize pygame

WIDTH, HEIGHT = 640,480
screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Set screen size of pygame window
background = pygame.Surface(screen.get_size()) # Create empty pygame surface
background.fill((255,255,255)) # Fill with white
background = background.convert() # Convert surface to make blitting faster
screen.blit(background, (0,0)) # Copy background onto screen
clock = pygame.time.Clock() # Create Pygame clock object

mainloop = True
FPS = 30 # Desired framerate

playtime = 0.0 # Tracks how long the game has been played

## OBJECT DEFINITIONS
class ship:
    def __init__(self, x,y):
        self.x,self.y = x, y
        self.vx = 0
        self.vy = 0
        self.theta = np.pi / 2
        self.cooldown = 0
        self.fire_delay = 5
        self.points = np.array([0,np.pi - .5, np.pi + .5, 0])
        self.r = 5
        self.dirty = None

    def move(self):
        # Calc dirty for blitting
        try:
            self.dirty = background.subsurface((self.x - 10,self.y - 10,20,20))
            self.dx = self.x - 10
            self.dy = self.y - 10
        except ValueError as e:
            self.dirty = None

        self.x += self.vx
        self.y += self.vy

    def get_points(self):
        return list(zip(self.r * np.cos(self.points + self.theta) + self.x, self.r * np.sin(self.points + self.theta) + self.y))




class blob:
    def __init__(self,x,y,r,s, rot=None, vx=0, vy=0):
        self.x, self.y = x, y

        self.ss = np.linspace(0, 2 * np.pi, s+1)
        self.rs = np.random.randn(s) + r
        self.diam = 2 * max(self.rs) + 3
        self.rs = np.hstack([self.rs, self.rs[0]])
        self.theta = 0
        self.rot = rot if rot != None else np.random.randn() * .01
        self.vx = vx
        self.vy = vy

        self.dirty = None

    def rotate(self):
        self.theta += self.rot

    def move(self):
        # First mark current location for blitting
        try:
            self.dirty = background.subsurface((self.x - self.diam/2, self.y-self.diam/2, self.diam, self.diam))
            self.dx,self.dy = self.x - self.diam/2, self.y-self.diam/2
        except ValueError as e:
            self.dirty = None


        # update x,y with vx,vy
        self.x += self.vx
        self.y += self.vy

        # When a blob exits the play area, reset on the other side
        if self.x > WIDTH:
            self.x = self.x % WIDTH - self.diam

        if self.x < - self.diam:
            self.x = WIDTH + self.diam + self.x

        if self.y > HEIGHT:
            self.y = self.y % WIDTH - self.diam

        if self.y < -self.diam:
            self.y = HEIGHT + self.diam + self.y



    def get_points(self):
        return list(zip(self.rs * np.cos(self.ss + self.theta) + self.x, self.rs * np.sin(self.ss + self.theta) + self.y))


## INITIALIZE GAME OBJECTS
blobs = [blob(x,y,10,10,vx,vy) for x, y,vx,vy in zip(np.random.random(10) * 600, np.random.random(10) * 400, np.random.randn(10), np.random.randn(10))]
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
    for b in blobs:
        b.rotate()
        b.move()

def render():
    text = "FPS: {0:.2f}    Playtime: {1:.2f}".format(clock.get_fps(),playtime)
    pygame.display.set_caption(text) # Print framerate in titlebar

    # Blitting stage
    for b in blobs:
        if b.dirty != None:
            screen.blit(b.dirty,(b.dx,b.dy))

    if player.dirty != None:
        screen.blit(player.dirty,(player.dx,player.dy))

    # Redraw stage
    for b in blobs:
        pygame.draw.polygon(screen,(0,0,0),b.get_points())

    pygame.draw.polygon(screen,(0,0,0),player.get_points())

    pygame.display.flip() # Update pygame display

while mainloop:
    milliseconds = clock.tick(FPS) # Does not go faster than FPS cap
    playtime += milliseconds / 1000.0


    events() # compute actions
    loop() # change state
    render() # print to screen

pygame.quit()
print("This game was played for {0:.2f} seconds".format(playtime))
