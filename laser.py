import numpy as np

class laser:
    def __init__(self,x,y,vx,vy):
        # Defines the head of the lazer
        self.x = x
        self.y = y

        # Defines direction of movement of the lazer
        self.vx = vx
        self.vy = vy

        # Defines the blitwork of the lazer (Could be shortened)
        self.dirty = None
        self.dirtyrect = None

        # Flag determining if the laser has hit a target
        self.hit = False

    def get_points(self):
        return (self.x, self.y), (self.x - self.vx, self.y - self.vy)
