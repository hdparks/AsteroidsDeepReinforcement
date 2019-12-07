WIDTH = None
HEIGHT = None

def run(objs):
    """ Removes out-of-bounds lasers """
    for obj in objs:
        if obj.x > WIDTH or obj.x < 0 or obj.y > HEIGHT or obj.y < 0:
            obj.hit = True
