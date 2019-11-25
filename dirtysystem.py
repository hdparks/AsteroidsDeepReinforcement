WIDTH = None
HEIGHT = None
background = None

def run(objs):
    """Iterates through objects, updating objects 'dirty' attribute
        based on its x,y, and blit_r attributes"""
    for obj in objs:
        obj.dx = max(obj.x - obj.blit_r, 0)
        obj.dy = max(obj.y - obj.blit_r, 0)
        w = min(WIDTH - obj.dx, 2 * obj.blit_r)
        h = min(HEIGHT - obj.dy, 2 * obj.blit_r)
        obj.dirty = background.subsurface((obj.dx, obj.dy, w, h))
