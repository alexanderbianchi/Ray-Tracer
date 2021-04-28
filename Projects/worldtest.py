from imports import *

# floor = Sphere()
# floor.transform = Scaling(10, 0.01, 10)
# floor.material = Material()
# floor.material.color = Color(1, 0.9, 0.9)
# floor.material.specular = 0

# leftWall = Sphere()
# leftWall.transform = Translation(
#     0, 0, 5) * RotationY(-math.pi/4) * RotationX(math.pi/2) * Scaling(10, 0.01, 10)

# leftWall.material = floor.material

# rightWall = Sphere()
# rightWall.transform = Translation(
#     0, 0, 5) * RotationY(math.pi/4) * RotationX(math.pi/2) * Scaling(10, 0.01, 10)

# rightWall.material = floor.material
###########################
middle = Sphere()
middle.transform = Translation(0, 1, 0)
middle.material.color = Color(0.1, 1, 0.5)
middle.material.diffuse = 0.7
middle.material.specular = 0.3
middle.material.pattern = Stripes(Color(.7, 1, .7), Color(.2, .7, 1))
# right = Sphere()
middle.material.pattern.setTransform(Scaling(.15, .15, .15))
# right.transform = Translation(1.5, 0.5, -0.5) * Scaling(0.5, 0.5, 0.5)
# right.material = Material()
# right.material.color = Color(0.5, 1, 0.1)
# right.material.diffuse = 0.7
# right.material.specular = 0.3

# left = Sphere()
# left.transform = Translation(-1.5, 0.33, -0.75) * Scaling(0.33, 0.33, 0.33)
# left.material.color = Color(1, 0.8, 0.1)
# left.material.diffuse = 0.7
# left.material.specular = 0.3

#objs = floor, leftWall, rightWall, left, right, middle
floor = Plane()
floor.material.color = Color(1, 1, 1)
#floor.material.pattern = Rings(Color(.7, 1, .7), Color(.2, .7, 1))
floor.material.reflectivity = 1.0
objs = [floor, middle]
w = World(PointLight(Point(-10, 10, -10), Color(1, 1, 1)), objs)


camera = Camera(320, 400, math.pi/3)

camera.transform = viewTransform(
    Point(-5, 1.7, 1), Point(0, .6, 0), Vector(0, 1, 0))

canvas = camera.render(w)

canvas.convert_to_ppm('ReflectionFinalInsta.ppm')
