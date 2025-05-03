import glm
from ..objeto import Objeto

class Grass(Objeto):
    #num_x e num_y definem quanto de tiles de grass vai renderizar
    def __init__(self, loader):
        super().__init__(loader)
        
         # Seta os nomes do modelo e da textura específicos para grama
        self.loader = loader
        self.model_path = "objetos/grass/grass.obj"
        self.texture_path = "objetos/grass/grass.jpg"
        self.scale = glm.vec3(0.05)
        self.rotation_axis = glm.vec3(1,0,0)
        self.rotation_angle = -90




    def generate(self, num_x, num_z):
        size = 300 #300 é o tamanho do obj

        #carrega os tiles de grass
        vertice_init, vertice_count, texture_id = self.loader.load_obj_and_texture(
            self.model_path, 
            self.texture_path
        )

        for i in range(num_x):
            for j in range(num_z):
                tile = Objeto(self.loader)
                tile.vertice_init = self.vertice_init
                tile.vertice_count = vertice_count
                tile.texture_id = texture_id
                tile.translation = glm.vec3(
                    size * ((-num_x + 1)/2 + i),
                    size * ((-num_z + 1)/2 + j),
                    0
                )
                self.children.append(tile)
        self.update_transform()
