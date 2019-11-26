def run(ships, objs):
    """ Calculates if any object is colliding with a ship object """
    for ship in ships:
        for obj in objs:
            if abs(ship.x - obj.x) + abs(ship.y - obj.y) < ship.r + obj.r:
                return True

    return False
