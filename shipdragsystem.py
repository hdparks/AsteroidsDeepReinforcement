def run(ship):
    """ Add some drag to the ship to allow for better controllability """
    ship.vx *= 0.95
    ship.vy *= 0.95
