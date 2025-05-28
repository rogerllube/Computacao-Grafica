import glm
import math
from ..objeto import Objeto

class Cama(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader
        self.group_id = 1

        self.estrutura = Objeto(loader)
        self.estrutura.load_model("objetos/cama/Estrutura.obj", "objetos/cama/textures/Bedwood_Colorbase_Baked-min.png")
        self.children.append(self.estrutura)

        self.colchao = Objeto(loader)
        self.colchao.load_model("objetos/cama/Colchao.obj", "objetos/cama/textures/Bed_ColorBase_Baked-Purple.png")
        self.children.append(self.colchao)

        self.scale = glm.vec3(2)
        self.rotation_axis = glm.vec3(0, 1, 0)
        self.rotation_angle = -90.0
        self.update_transform()