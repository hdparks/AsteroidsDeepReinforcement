pygame = None
screen = None
background = None

def run(objs):
    """ Draws objects with get_points """
    for obj in objs:
        rect = pygame.draw.polygon(screen, (0,0,0),obj.get_points())
        rect = rect.clip(screen.get_rect())
        obj.dirty = background.subsurface(rect)
        obj.dirtyrect = rect
