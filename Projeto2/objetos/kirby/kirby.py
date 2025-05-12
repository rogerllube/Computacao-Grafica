import glm
import math
from ..objeto import Objeto

class Kirby(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader

        self.body = Objeto(loader)
        self.body.load_model("objetos/kirby/body.obj", "objetos/kirby/baking.png")
        self.children.append(self.body)

        self.hands = Objeto(loader)
        self.hands.load_model("objetos/kirby/hands.obj", "objetos/kirby/baking.png")
        self.children.append(self.hands)

        self.feet = Objeto(loader)
        self.feet.load_model("objetos/kirby/feet.obj", "objetos/kirby/baking.png")
        self.children.append(self.feet)

        self.scale = glm.vec3(4)
        self.update_transform()
