pygame = None
screen = None

def run(objs):
    """ Draws objects with get_points """
    for obj in objs:
        pygame.draw.polygon(screen, (0,0,0),obj.get_points())

    pygame.display.flip()
