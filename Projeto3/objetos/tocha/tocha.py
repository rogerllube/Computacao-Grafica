import glm
import math
from ..objeto import Objeto

class Tocha(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader
        self.group_id = 1

        self.tocha = Objeto(loader)
        self.tocha.load_model("objetos/tocha/Tocha.obj", "objetos/tocha/textures/torch_albedo.png")
        self.children.append(self.tocha)

        self.light_obj = Objeto(loader)
        self.light_obj.translation = glm.vec3(0, 2/200, 6/200)
        self.light_obj.is_light_source = True 
        self.light_obj.light_color = glm.vec3(1.0, 0.5, 0.0)
        self.light_obj.light_diffuse = 2.4
        self.light_obj.light_specular = 3.6
        self.light_obj.light_ambient = 0
        self.light_obj.light_linear = 0.1
        self.light_obj.light_quadratic = 0.1
        self.children.append(self.light_obj)

        self.translation = glm.vec3(-20.8, 10, -112)
        self.scale = glm.vec3(200)
        self.rotation_axis = glm.vec3(0, 1, 0)
        self.rotation_angle = 90.0

        self.update_transform()