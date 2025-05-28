import glm
import math
from ..objeto import Objeto

class Kirby(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader
        self.group_id = 1

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
        self.animcycle = 0.0
        self.grow_range = [4, 6]

        self.update_transform()

    def grow(self, delta_time : float):

        self.animcycle = (self.animcycle + delta_time)
        min_s, max_s = self.grow_range
        self.center = glm.vec3(0, -0.5, 0)

        amp_s = (max_s - min_s) / 2.0
        off_s = (max_s + min_s) / 2.0

        bounce_scale = off_s + amp_s * math.sin(self.animcycle * 2 * math.pi)
        self.scale = glm.vec3(bounce_scale)
        

        self.update_transform()

    def stop_grow(self):
        self.scale = glm.vec3(4)
        self.animcycle = 0
        self.update_transform()


