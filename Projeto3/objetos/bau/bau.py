import glm
import math
from ..objeto import Objeto

class Bau(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader

        self.base = Objeto(loader)
        self.base.load_model("objetos/bau/Base.obj", "objetos/bau/OldChest.png")
        self.children.append(self.base)

        self.tampa = Objeto(loader)
        self.tampa.load_model("objetos/bau/Tampa.obj", "objetos/bau/OldChest.png")
        self.children.append(self.tampa)

        self.scale = glm.vec3(1.5)
        self.rotation_axis = glm.vec3(0, 1, 0)
        self.rotation_angle = 90
        self.update_transform()