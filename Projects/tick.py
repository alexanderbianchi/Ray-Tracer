
import sys
sys.path.append('../')
from raytracer.components.canvas import *


def tick(enviorment, projectile):
    position = projectile['position'] + projectile['velocity']
    velocity = projectile['velocity'] + \
        enviorment['gravity'] + enviorment['wind']
    velocity.normalize()*7
    return {'position': position, 'velocity': velocity}


def render(projectile, enviorment, grid):
    positions = [projectile['position']]
    while True:
        projectile = tick(enviorment, projectile)

        if (projectile['position'].x > 0
            and projectile['position'].y > 0
            and projectile['position'].y < grid.height
                and projectile['position'].x < grid.width):

            positions.append(projectile['position'])
        else:
            break
    print(len(positions))
    for x in positions:

        grid.write_pixel(floor(grid.width - x.x),
                         floor(grid.height-x.y), colors(1, 0, 0))


canvas = Canvas(900, 550)
projectile = {'position': Vector(
    50, 30, 0), 'velocity': Vector(1, 1.8, 0).normalize()*7}
enviorment = {'wind': Vector(0, -0.01, 0), 'gravity': Vector(0, -0.1, 0)}
render(projectile, enviorment, canvas)
canvas.convert_to_ppm('test.ppm')
