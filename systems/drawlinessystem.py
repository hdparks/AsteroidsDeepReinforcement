pygame = None
screen = None
background = None

def run(objs):
    """ Draws objects with get_points """
    for obj in objs:
        b,e = obj.get_points()
        rect = pygame.draw.line(screen, (0,0,0),b,e)
        rect = rect.clip(screen.get_rect())
        try:
            obj.dirty = background.subsurface(rect)
            obj.dirtyrect = rect
        except ValueError as e:
            obj.dirty = None
            obj.dirtyrect = None
