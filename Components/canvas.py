import math


class colors():
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other):
        red = self.red + other.red
        green = self.green + other.green
        blue = self.blue + other.blue

        return colors(red, green, blue)

    def __sub__(self, other):
        red = self.red - other.red
        green = self.green - other.green
        blue = self.blue - other.blue

        return colors(red, green, blue)

    def __eq__(self, other):
        if (self.red == other.red and
            self.green == other.green and
                self.blue == other.blue):
            return True
        return False

    def __mul__(self, scalar):
        red = self.red * scalar
        green = self.green * scalar
        blue = self.blue * scalar
        return colors(red, green, blue)

    def show(self):
        return (self.red, self.green, self.blue)

    def hadamard(self, other):
        red = self.red * other.red
        green = self.green * other.green
        blue = self.blue * other.blue

        return colors(red, green, blue)

    def to_rgb(self):
        r = str(clamp(math.ceil(self.red * 255), 0, 255))
        g = str(clamp(math.ceil(self.green * 255), 0, 255))
        b = str(clamp(math.ceil(self.blue * 255), 0, 255))

        return ' '.join([r, g, b])

    def __round__(self, idx=4):
        return colors(round(self.red, idx), round(self.green, idx), round(self.blue, idx))

    def __str__(self):
        return str((self.red, self.green, self.blue))


def clamp(n: float, minn: int, maxn: int) -> int:
    return int(max(min(maxn, n), minn))


class Canvas():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[colors(0, 0, 0) for j in range(width)]
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
