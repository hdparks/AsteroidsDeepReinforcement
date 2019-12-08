screen = None

def run(objs):
    destroyed = 0
    for obj in objs:
        if obj.hit == True:
            destroyed += 1
            if obj.dirty != None and obj.dirtyrect != None:
                screen.blit(obj.dirty, obj.dirtyrect)
            objs.remove(obj)

    return destroyed
