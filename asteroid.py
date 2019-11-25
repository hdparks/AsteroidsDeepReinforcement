import numpy as np

class asteroid:
    def __init__(self,x,y,r,s, rot=None, vx=0, vy=0):
        self.x, self.y = x, y

        self.ss = np.linspace(0, 2 * np.pi, s)
        self.rs = np.random.randn(s) + r
        self.r = min(self.rs)
        self.theta = 0
        self.rot = rot if rot != None else np.random.randn() * .01
        self.vx = vx
        self.vy = vy

        self.blit_r = max(self.rs) + 3
        self.dirty = None

    def get_points(self):
        return list(zip(self.rs * np.cos(self.ss + self.theta) + self.x, self.rs * np.sin(self.ss + self.theta) + self.y))
