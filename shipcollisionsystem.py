def run(ship, objs):
    """ Calculates if any object is colliding with the ship object """
    for obj in objs:
        if abs(ship.x - obj.x) + abs(ship.y - obj.y) < ship.r + obj.r:
            return True

    return False
