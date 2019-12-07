def run(objs):
    """ Moves objects with x,y,vx,vy """
    for obj in objs:
        obj.x += obj.vx
        obj.y += obj.vy
