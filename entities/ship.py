import numpy as np
class ship:
    def __init__(self, x,y):
        # x, y position
        self.x,self.y = x, y

        # horizontal and vertical velocity
        self.vx = 0
        self.vy = 0

        # theta is the orientation of the ship
        self.theta = np.pi / 2

        # Points defines the points on the unit circle which formulate the polygon
        self.points = np.array([0,np.pi - .5, np.pi + .5])

        # radius of the ship (will fit inside circle with radius r centered at (x,y) )
        self.r = 5

        # Fire set to true when ship is firing a laser
        self.fire = False

        # Keeps track of previous frame position, used for blitting
        self.dirty = None
        self.dirtyrect = None

        # Hit tracks if the ship has been hit or not (Fail condition)
        self.hit = False

    def get_points(self):
        return list(zip(self.r * np.cos(self.points + self.theta) + self.x, self.r * np.sin(self.points + self.theta) + self.y))
