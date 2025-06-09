import glm
import math
from ..objeto import Objeto

class Lampada(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader
        self.group_id = 1

        self.tampa = Objeto(loader)
        self.tampa.load_model("objetos/lampada/tampa.obj", "objetos/lampada/textures/tampa.png")
        self.children.append(self.tampa)

        self.grade = Objeto(loader)
        self.grade.load_model("objetos/lampada/grade.obj", "objetos/lampada/textures/grade.png")
        self.children.append(self.grade)

        self.suporte = Objeto(loader)
        self.suporte.load_model("objetos/lampada/suporte.obj", "objetos/lampada/textures/suporte.png")
        self.children.append(self.suporte)

        self.light_obj = Objeto(loader)
        self.light_obj.translation = glm.vec3(2, 4.5, 2)
        self.light_obj.is_light_source = True 
        self.light_obj.light_color = glm.vec3(1.0, 1.0, 1.0)
        self.light_obj.light_diffuse = 2.4
        self.light_obj.light_specular = 3.6
        self.light_obj.light_ambient = 1
        self.light_obj.light_linear = 0.05
        self.light_obj.light_quadratic = 0.05
        self.children.append(self.light_obj)

        self.scale = glm.vec3(1, 1, 1)
        self.translation = glm.vec3(14, 8, -116)
        
        self.rotation_axis = glm.vec3(0, 1, 0)
        self.rotation_angle = -90.0

        self.update_transform()