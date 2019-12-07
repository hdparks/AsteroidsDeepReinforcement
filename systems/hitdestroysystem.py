screen = None

def run(objs):
    for obj in objs:
        if obj.hit == True:
            if obj.dirty != None and obj.dirtyrect != None:
                screen.blit(obj.dirty, obj.dirtyrect)
            objs.remove(obj)
