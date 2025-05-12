import glm
import math
from ..objeto import Objeto

class Skybox(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader

        self.skybox = Objeto(loader)
        self.skybox.load_model("objetos/skybox/skybox.obj", "objetos/skybox/Texture.png")
        self.children.append(self.skybox)

        self.scale = glm.vec3(4.5)

