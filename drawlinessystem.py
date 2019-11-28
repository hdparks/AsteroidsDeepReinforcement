pygame = None
screen = None

def run(objs):
    """ Draws objects with get_points """
    for obj in objs:
        b,e = obj.get_points()
        pygame.draw.line(screen, (0,0,0),b,e)
