WIDTH = None
HEIGHT = None

def run(objs):
    """ Objects with x,y are wrapped around the play area """
    for obj in objs:
        if obj.x > WIDTH + 20:
            obj.x = -10

        if obj.y > HEIGHT + 20:
            obj.y = -10

        if obj.x < -20:
            obj.x = WIDTH + 10

        if obj.y < -20:
            obj.y = HEIGHT + 10
