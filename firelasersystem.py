
def run(objs):
    """ For objects with fire, theta, x,y, vx,vy, spawns laser """
    lasers = []
    for obj in objs:
        if obj.fire:
            lasers.append( Laser(   obj.x,
                                    obj.y,
                                    obj.vx + 3 * np.cos(obj.theta),
                                    obj.vy + 3 * np.sin(obj.theta)) )
            obj.fire = False
    return lasers
