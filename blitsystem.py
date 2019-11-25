screen = None

def run(objs):
    """ for each object with dirty, dx, dy, blit their most recent position """
    for obj in objs:
        screen.blit(obj.dirty,(obj.dx, obj.dy))
