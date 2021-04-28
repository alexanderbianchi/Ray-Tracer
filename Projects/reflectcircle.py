from imports import *

middle = Sphere()
middle.transform = Translation(0, 1, 0)
#middle.transform = Translation(0, 1, 1.2)
middle.material.color = Color(0.1, 0.1, 0.1)
middle.material.diffuse = 0.7
middle.material.specular = 0.3

middle.material.reflectivity = 1.0

right = Sphere()


right.transform = Translation(2.5, 0.5, -0.5) * Scaling(0.5, 0.5, 0.5)
#right.transform = Translation(0, 0.5, -.7) * Scaling(0.5, 0.5, 0.5)
right.material = Material()
right.material.color = Color(0.5, 1, 0.1)
right.material.diffuse = 0.7
right.material.specular = 0.3
right.material.pattern = Stripes(Color(.7, 1, .7), Color(.2, .7, 1))
right.material.pattern.setTransform(Scaling(.1, .1, .1))

left = Sphere()
#left.transform = Translation(2.5, 0.7, 1.5) * Scaling(0.7, 0.7, 0.7)
# left.transform = Translation(3, 1.5, 0) * Scaling(1.5, 1.5, 1.5)
# left.material.color = Color(1, 0.9, 0.9)
# left.material.diffuse = 0.7
# left.material.specular = 1
# left.material.shininess = 300
# left.material.reflectivity = 0.2
# left.material.refractiveIndex = .7
# left.material.transparency = 1

floor = Plane()
floor.material.color = Color(1, 1, 1)
#floor.material.pattern = Rings(Color(.7, 1, .7), Color(.2, .7, 1))

floor.material.reflectivity = 1.0
objs = [floor, middle, right]
w = World(PointLight(Point(10, 10, 10), Color(1, 1, 1)), objs)


camera = Camera(700, 700, math.pi/3)


camera.transform = viewTransform(
    Point(7, 1.7, 0), Point(0, .6, 0), Vector(0, 1, 0))

canvas = camera.render(w)

canvas.convert_to_ppm('refractive11asdasfasf.ppm')
