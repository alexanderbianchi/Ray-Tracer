from raytracer.components.tuples import *
import math
from raytracer.components.shapes import *


class Canvas():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[Color(0, 0, 0) for j in range(width)]
                       for n in range(height)]

    def write_pixel(self, x, y, color):
        self.canvas[y][x] = color

    def pixel_at(self, x, y):
        return self.canvas[y][x]

    def show_canvas(self):
        return self.canvas

    def convert_to_ppm(self, name):
        ppm = open(name, 'a+')
        start = 'P3\n{} {}\n255\n'.format(
            self.width, self.height)  # the characters to start
        colors = [start]
        tracker = 0

        for i in self.canvas:
            for j in i:

                numbers = j.to_rgb()

                tracker += len(numbers) + 1
                colors.append(numbers + ' ')

                if tracker > 53:
                    colors.append('\n')
                    tracker = 0

        ppm.write(''.join(colors))

        ppm.close()
