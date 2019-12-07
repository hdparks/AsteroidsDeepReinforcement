from entities.asteroid import asteroid
import numpy as np

def run(asteroids):
    for a in asteroids:
        if a.hit:
            # Spawn two smaller asteroids
            if a.r == 10:
                # make 2 midsized
                asteroids.extend([asteroid(a.x,a.y,8,10,a.vx + np.random.randn(), a.vy + np.random.randn()) for _ in range(2)])

            if a.r == 8:
                # make 2 smaller
                asteroids.extend([asteroid(a.x,a.y,5,10,a.vx + np.random.randn(), a.vy + np.random.randn()) for _ in range(2)])
