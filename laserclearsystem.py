objs = []

def run():
    """ Removes out-of-bounds lasers """
    for obj in objs:
        if obj.x > WIDTH or obj.x < 0 or obj.y > HEIGHT or obj.y < 0:
            objs.remove(obj)
