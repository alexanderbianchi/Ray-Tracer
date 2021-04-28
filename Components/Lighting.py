from raytracer.components.tuples import *
from raytracer.components.matrix import *
import math


class PointLight():
    def __init__(self, position, intensity):
        self.intensity = intensity
        self.position = position

    def __eq__(self, other):
        try:
            if self.intensity == other.intensity and self.position == other.position:
                return True
        except:
            pass
        return False


class Material():
    def __init__(
            self,
            color=Color(1, 1, 1),
            ambient=0.1,
            diffuse=0.9,
            specular=0.9,
            shininess=200,
            pattern=False,
            reflectivity=0,
            transparency=0,
            refractiveIndex=1):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.pattern = pattern
        self.reflectivity = reflectivity
        self.transparency = transparency
        self.refractiveIndex = refractiveIndex

    def __eq__(self, other):
        if (self.color != other.color or
            self.ambient != other.ambient or
            self.diffuse != other.diffuse or
            self.specular != other.specular or
                self.shininess != other.shininess):
            return False
        return True


def lighting(material, light, point, eyev, normalv, inShadow=False, obj=None):
    if material.pattern:
        c = material.pattern.colorAtObject(point, obj)
    else:
        c = material.color
    effective_color = c.hadamard(light.intensity)
    ambient = effective_color * material.ambient

    if inShadow == True:
        return ambient
    lightv = light.position - point
    lightv.normalize()
    light_dot_normal = lightv.dot(normalv)
    if light_dot_normal < 0:
        black = Color(0, 0, 0)
        diffuse = black
        specular = black
    else:
        diffuse = effective_color * material.diffuse * light_dot_normal
        lightv = -lightv
        reflectv = lightv.reflect(normalv)
        reflect_dot_eye = reflectv.dot(eyev)
        if reflect_dot_eye <= 0:
            specular = Color(0, 0, 0)
        else:
            factor = pow(reflect_dot_eye, material.shininess)
            specular = light.intensity * material.specular * factor

    answer = ambient + diffuse + specular

    return answer
