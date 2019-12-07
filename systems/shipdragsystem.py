def run(ships):
    """ Add some drag to the ship to allow for better controllability """
    for ship in ships:
        ship.vx *= 0.95
        ship.vy *= 0.95
