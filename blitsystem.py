screen = None

def run(objs):
    """ for each object with dirty their most recent position """
    for obj in objs:
        if obj.dirty != None and obj.dirtyrect != None:
            screen.blit( obj.dirty, obj.dirtyrect )
