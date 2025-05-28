import glm
import random
from ..objeto import Objeto
from ..hitbox import Hitbox

#armazena informacoes de cada tipo de objeto para geracao automatica
class ForestObjectType():
    def __init__(self, loader):
        #parametros para geracao
        self.max_iteration = 10000
        self.max_num = 1000
        self.same_type_spacing = 10 #distancia minima entre objetos na geracao
        self.dif_type_spacing = 3 #distancia minima entre objetos de outros tipos
        self.scale = glm.vec3(2)
        self.scale_variation = 0.6
        self.spread = [400,400]
        self.model_path = ""
        self.texture_path = ""

        #parametros locais
        self.vertice_init = 0
        self.vertice_count = 0
        self.texture_id = 0
        self.obj_num = 0

        self.loader = loader

    #carrega o modelo
    def load_model(self):
        self.vertice_init, self.vertice_count, self.texture_id = self.loader.load_obj_and_texture(
            self.model_path, 
            self.texture_path
        )

    #cria e inicializa 1 objeto desse tipo
    def generate(self, pos):
        obj = Objeto(self.loader)
        obj.vertice_count = self.vertice_count
        obj.vertice_init = self.vertice_init
        obj.texture_id = self.texture_id
        obj.translation = pos
        obj.scale = self.scale * random.uniform(1-self.scale_variation, 1+self.scale_variation)
        obj.rotation_axis = glm.vec3(0,1,0)
        obj.rotation_angle = random.random() * 360

        self.obj_num+=1

        return obj 
    
        

#gera automaticamente a floresta
#caso ja tiver objeto na cena, adicione-o no hitbox_list
class ForestGenerator(Objeto):
    #num_x e num_y definem quanto de tiles de grass vai renderizar
    def __init__(self, loader):
        super().__init__(loader)

        #parametros editaveis para geracao
        self.hitbox_list = []
        self.objTypes = []

        
        #criar os models dos objetos
        tree = ForestObjectType(loader)
        tree.model_path = "objetos/forest/tree.obj"
        tree.texture_path = "objetos/forest/forest.png"
        self.objTypes.append(tree)

        stone = ForestObjectType(loader)
        stone.model_path = "objetos/forest/stone.obj"
        stone.texture_path = "objetos/forest/forest.png"
        stone.max_num = 500
        stone.same_type_spacing = 12
        stone.dif_type_spacing = 2
        self.objTypes.append(stone)

        
    #gera automaticamente a floresta
    #coloque elementos ja existentes no hitbox_list
    def generate(self, hitbox_list = None):
        #inicializa os objetos
        self.children = []
        if(hitbox_list):
            self.hitbox_list = hitbox_list
        else:
            self.hitbox_list = []


        #para cada tipo de objeto
        for objType in self.objTypes:
            #inicializa
            objType.load_model()
            objType.obj_num = 0

            #gera os objetos
            for i in range(objType.max_iteration):
                #define o hitbox do novo objeto
                new_hitbox = Hitbox()
                new_hitbox.pos = glm.vec3(
                    random.uniform(-objType.spread[0]/2, objType.spread[0]/2),
                    0,
                    random.uniform(-objType.spread[1]/2, objType.spread[1]/2) 
                )
                new_hitbox.radius = objType.same_type_spacing

                #verifica se colide com algum objeto
                is_hit = False
                for hitbox in self.hitbox_list:
                    if(hitbox.is_hit(new_hitbox)):
                        is_hit = True
                
                #gera o objeto
                if(not is_hit):
                    self.hitbox_list.append(new_hitbox)

                    new_obj = objType.generate(new_hitbox.pos)

                    self.children.append(new_obj)

                    if(objType.obj_num >= objType.max_num):
                        break
            
            #modifica o spacing (spacing diferente entre objetos de tipo igual e diferente)
            for i in range(objType.obj_num):
                self.hitbox_list[-i-1].radius = objType.dif_type_spacing

            print('Gerou {} modelos do tipo {}.'.format(objType.obj_num, objType.model_path))

        self.update_transform()