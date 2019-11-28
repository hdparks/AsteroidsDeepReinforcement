import numpy as np

def run(lasers, objs):
    objxyr = np.array([[obj.x, obj.y, obj.r] for obj in objs])


    for laser in lasers:
        xy = np.array([laser.x, laser.y])

        # Collisions occur when a laser penetrates the radius of an asteroid
        collisions = np.linalg.norm(xy - objxyr[:,:-1], axis = 1) < objxyr[:,-1]
        if any(collisions):
            idx = np.argmax(collisions) # Grabs index of first collision
            objs[idx].hit = True
            laser.hit = True
