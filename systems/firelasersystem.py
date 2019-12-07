from entities.laser import laser
import numpy as np

def run(objs):
    """ For objects with fire, theta, x,y, vx,vy, spawns laser """
    lasers = []
    for obj in objs:
        if obj.fire:
            lasers.append( laser(   obj.x,
                                    obj.y,
                                    obj.vx + 8 * np.cos(obj.theta),
                                    obj.vy + 8 * np.sin(obj.theta)) )
            obj.fire = False
    return lasers
