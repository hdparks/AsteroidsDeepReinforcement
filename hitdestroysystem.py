def run(objs):
    for obj in objs:
        if obj.hit == True:
            objs.remove(obj)
