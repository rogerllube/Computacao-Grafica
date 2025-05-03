import glm
import math
from ..objeto import Objeto

class WaddleDee(Objeto):
    def __init__(self, loader):
        super().__init__(loader)
        
        self.loader = loader

        #cria os partes do waddle
        self.body = Objeto(loader)
        self.body.load_model("objetos/waddle_dee/body.obj", "objetos/waddle_dee/body.png")
        self.children.append(self.body)

        self.bandana = Objeto(loader)
        self.bandana.load_model("objetos/waddle_dee/bandana.obj", "objetos/waddle_dee/bandana.png")
        self.body.children.append(self.bandana)

        self.left_foot = Objeto(loader)
        self.left_foot.load_model("objetos/waddle_dee/left_foot.obj", "objetos/waddle_dee/body.png")
        self.children.append(self.left_foot)

        self.right_foot_rot_center = Objeto(loader)
        self.children.append(self.right_foot_rot_center)
        self.right_foot = Objeto(loader)
        self.right_foot.load_model("objetos/waddle_dee/right_foot.obj", "objetos/waddle_dee/body.png")
        self.children.append(self.right_foot)

        self.left_hand = Objeto(loader)
        self.left_hand.load_model("objetos/waddle_dee/left_hand.obj", "objetos/waddle_dee/body.png")
        self.body.children.append(self.left_hand)

        self.right_hand = Objeto(loader)
        self.right_hand.load_model("objetos/waddle_dee/right_hand.obj", "objetos/waddle_dee/body.png")
        self.body.children.append(self.right_hand)

        self.spear = Objeto(loader)
        self.spear.load_model("objetos/waddle_dee/spear.obj", "objetos/waddle_dee/spear.png")
        self.right_hand.children.append(self.spear)

        self.spear_edge = Objeto(loader)
        self.spear_edge.load_model("objetos/waddle_dee/spear_edge.obj", "objetos/waddle_dee/spear_edge.png")
        self.spear.children.append(self.spear_edge)




        #####parametros
        #transformacao inicial
        self.scale = glm.vec3(4)

        #walk
        self.walk_anim_speed = 1
        self.foot_rotation_range = [-30, 50]
        self.arm_rotation_range = [-25, 25] 
        self.body_rotation_range = [-5, 5]
        self.body_bounce_range   = [0.9, 1.1]
        self.right_foot.center.y = 0.75
        self.left_foot.center.y = 0.75
        self.body.center.y = 0.2

        ######variaveis
        self.left_foot.rotation_axis = glm.vec3(1,0,0)
        self.right_foot.rotation_axis = glm.vec3(1, 0, 0)

        self.left_hand.rotation_axis = glm.vec3(0, 1, 0)
        self.right_hand.rotation_axis = glm.vec3(0, 1, 0)

        self.body.rotation_axis = glm.vec3(0, 1, 0)

        self.walk_time = 0.0
        

        #aplica transformacao
        self.update_transform()




    def walk(self, delta_time: float):
        # 1) Atualiza o tempo de animação
        self.walk_time += delta_time * self.walk_anim_speed

        # 2) Cálculo para os pés
        min_f, max_f = self.foot_rotation_range
        amp_f = (max_f - min_f) / 2.0
        off_f = (max_f + min_f) / 2.0

        # 3) Cálculo para os braços
        min_a, max_a = self.arm_rotation_range
        amp_a = (max_a - min_a) / 2.0
        off_a = (max_a + min_a) / 2.0

        # 4) Cálculo para o corpo (rotação)
        min_b, max_b = self.body_rotation_range
        amp_b = (max_b - min_b) / 2.0
        off_b = (max_b + min_b) / 2.0

        # 5) Cálculo para o corpo (bouncing via escala)
        min_s, max_s = self.body_bounce_range
        amp_s = (max_s - min_s) / 2.0
        off_s = (max_s + min_s) / 2.0

        # 6) Seno para o ciclo (um ciclo completo = 2π)
        seno = math.sin(self.walk_time * 2 * math.pi)
        seno_double = math.sin(self.walk_time * 2 * math.pi * 2)

        # 7) Ângulos dos pés
        self.left_foot.rotation_angle  = off_f +  amp_f * seno
        self.right_foot.rotation_angle = off_f -  amp_f * seno

        # 8) Ângulos dos braços (em fase)
        self.left_hand.rotation_angle  = off_a -  amp_a * seno
        self.right_hand.rotation_angle = off_a -  amp_a * seno

        # 9) Ângulo de rotação do corpo (balanço suave)
        self.body.rotation_angle = off_b - amp_b * seno

        # 10) Escala do corpo (bouncing effect)
        bounce_scale = off_s + amp_s * seno_double
        self.body.scale = glm.vec3(1, bounce_scale, 1)

        # 11) Propaga transformações na hierarquia
        self.update_transform()
    
    def stop_walk(self):
        self.left_foot.rotation_angle = 0
        self.right_foot.rotation_angle = 0
        self.body.rotation_angle = 0
        self.walk_time = 0.0

        self.body.scale = glm.vec3(1)

        self.update_transform()

