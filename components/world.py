import sys
from raytracer.components.tuples import *
from raytracer.components.matrix import *
import math
from raytracer.components.rays import *
from raytracer.components.canvas import *
from raytracer.components.lighting import *
from raytracer.components.shapes import *

x = Sphere()
y = Sphere()
x.material = Material(Color(.8, 1, .6), 0.1, 0.7, 0.9, 200)
y.transform *= Scaling(0.5, 0.5, 0.5)
obj = [x, y]


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben


class World():
    def __init__(self, light=PointLight(Point(-10, 10, -10), Color(1, 1, 1)), objects=obj):
        # might want to make the world default like its own thing
        self.light = light
        self.objects = objects

    def intersect(self, r):
        intersects = Intersections()

        for obj in self.objects:
            ray2 = r.transform(obj.transform.inverse())
            hits = obj.localIntersect(
                ray2)
            if hits:
                intersects.intersections = hits.intersections + intersects.intersections

        intersects.intersections.sort()
        return intersects

    def refracted(self, comps, remaining):
        if comps['object'].material.transparency == 0 or remaining <= 0:
            return Color(0, 0, 0)

        nRatio = comps['n1'] / comps['n2']
        cosi = comps['eyev'].dot(comps['normalv'])
        sin2t = (nRatio * nRatio) * (1-(cosi * cosi))
        if sin2t > 1:
            return Color(0, 0, 0)
        cost = math.sqrt((1-sin2t))
        direction = (comps['normalv'] *
                     (nRatio * cosi - cost)) - (comps['eyev'] * nRatio)
        refractRay = Ray(comps['underPoint'], direction)
        color = self.colorAt(refractRay, remaining-1) * \
            comps['object'].material.transparency
        return color

    def shadeHit(self, comps, remaining):
        # potential to add ability to handle multiple light sources
        shadowed = self.isShadowed(comps['overPoint'])
        surface = lighting(comps['object'].material,
                           self.light, comps['point'], comps['eyev'],
                           comps['normalv'], shadowed, comps['object'])
        reflected = self.reflectiveColor(comps, remaining)
        refracted = self.refracted(comps, remaining)
        m = comps['object'].material
        if m.reflectivity > 0 and m.transparency > 0:
            reflectance = schlick(comps)
            return surface + reflected * reflectance + refracted * (1-reflectance)

        return surface + reflected + refracted

    def colorAt(self, r, remaining=10):
        x = self.intersect(r)
        hit = x.hit()
        if hit:
            comps = hit.prep(r, x)
            return self.shadeHit(comps, remaining)
        else:
            return Color(0, 0, 0)

    def isShadowed(self, point):
        v = self.light.position - point
        distance = v.magnitude()
        direction = v.normalize()
        r = Ray(point, direction)

        intersections = self.intersect(r)
        hit = intersections.hit()

        if hit and hit.t < distance:
            return True
        else:
            return False

    def reflectiveColor(self, comps, remaining):
        if remaining <= 0:
            return Color(0, 0, 0)
        if comps['object'].material.reflectivity == 0:
            return Color(0, 0, 0)
        else:
            reflectRay = Ray(comps['overPoint'], comps['reflectv'])
            color = self.colorAt(reflectRay, remaining-1)
            return color * (comps['object'].material.reflectivity)


def viewTransform(frm, to, up):
    forward = to - frm
    forward.normalize()
    upn = up.normalize()
    left = forward.cross(upn)
    trueUp = left.cross(forward)
    orientation = Matrix([
        [left.x, left.y, left.z, 0],
        [trueUp.x, trueUp.y, trueUp.z, 0],
        [-forward.x, -forward.y, -forward.z, 0],
        [0, 0, 0, 1],
    ])
    return orientation * Translation(-frm.x, -frm.y, -frm.z)


identity = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


class Camera():
    def __init__(self, hsize, vsize, fov, transform=False):
        self.hsize = hsize
        self.vsize = vsize
        self.fov = fov
        if transform is False:
            transform = identity

        self.transform = transform

        halfView = math.tan(self.fov/2)
        aspect = self.hsize/self.vsize
        if aspect >= 1:
            self.halfWitdh = halfView
            self.halfHeight = halfView/aspect

        else:
            self.halfWitdh = halfView * aspect
            self.halfHeight = halfView

        self.pixelSize = (self.halfWitdh * 2) / self.hsize

    def rayForPixel(self, px, py):
        xoffset = (px + 0.5) * self.pixelSize
        yoffset = (py + 0.5) * self.pixelSize

        worldX = self.halfWitdh - xoffset
        worldY = self.halfHeight - yoffset
        i = self.transform.inverse()
        pixel = i * Point(worldX, worldY, -1)
        origin = i * Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return Ray(origin, direction)

    def render(self, world):
        image = Canvas(self.hsize, self.vsize)
        l = self.hsize * self.vsize
        i = 0
        for y in range(0, self.vsize):
            for x in range(0, self.hsize):
                ray = self.rayForPixel(x, y)
                color = world.colorAt(ray)
                image.write_pixel(x, y, color)
                i += 1
                progress(i, l, suffix='')
        return image


def schlick(comps):
    cos = comps['eyev'].dot(comps['normalv'])
    if comps['n1'] > comps['n2']:
        n = comps['n1'] / comps['n2']
        sin2t = n ** 2 * (1-cos**2)
        if sin2t > 0:
            return 1

        cost = math.sqrt(1-sin2t)
        cos = cost
    r0 = (((comps['n1'] - comps['n2']) / (comps['n1'] + comps['n2']))**2)

    return r0 + (1 - r0) * (1-cos) ** 5
