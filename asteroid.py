import numpy as np

class asteroid:
    def __init__(self, x, y, r, s, vx,vy):

        self.x, self.y = x, y

        self.ss = np.linspace(0, 2 * np.pi, s) # s defines the number of sides
        self.rs = np.random.randn(s) + r # r defineds the radius
        self.r = r
        self.s = s
        self.theta = 0
        self.rot = np.random.randn() * .01
        self.vx = vx
        self.vy = vy

        self.dirty = None
        self.dirtyrect = None

        # Flag determining if asteroid was hit by a laser
        self.hit = False

    def get_points(self):
        return list(zip(self.rs * np.cos(self.ss + self.theta) + self.x, self.rs * np.sin(self.ss + self.theta) + self.y))
