import glm
import math
from ..objeto import Objeto

class Dedede(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader

        #cria os partes do dedede
        self.body = Objeto(loader)
        self.body.load_model("objetos/dedede/body.obj", "objetos/dedede/dedede.png")
        self.children.append(self.body)

        self.left_foot = Objeto(loader)
        self.left_foot.load_model("objetos/dedede/left_foot.obj", "objetos/dedede/dedede.png")
        self.children.append(self.left_foot)

        self.right_foot_rot_center = Objeto(loader)
        self.children.append(self.right_foot_rot_center)
        self.right_foot = Objeto(loader)
        self.right_foot.load_model("objetos/dedede/right_foot.obj", "objetos/dedede/dedede.png")
        self.children.append(self.right_foot)

        self.left_hand = Objeto(loader)
        self.left_hand.load_model("objetos/dedede/left_hand.obj", "objetos/dedede/dedede.png")
        self.body.children.append(self.left_hand)

        self.right_hand = Objeto(loader)
        self.right_hand.load_model("objetos/dedede/right_hand.obj", "objetos/dedede/dedede.png")
        self.body.children.append(self.right_hand)

        self.hammer = Objeto(loader)
        self.hammer.load_model("objetos/dedede/hammer.obj", "objetos/dedede/hammer.png")
        self.left_hand.children.append(self.hammer)


        

        #####parametros editaveis

        #transformacao inicial
        self.scale = glm.vec3(3)

        #walk animation
        self.walk_anim_speed = 1.6
        self.foot_rotation_range = [-30, 50]
        self.arm_rotation_range = [-25, 25] 
        self.body_rotation_range = [-5, 5]
        self.body_bounce_range   = [0.9, 1.1]
        self.right_foot.center.y = 0.75
        self.left_foot.center.y = 0.75
        self.body.center.y = 0.2

        #walk translation and rotation
        self.circle_center = glm.vec3(0.0, 0.0, 0.0)
        self.circle_radius = 50
        self.inicial_angle = math.radians(0) #angulo inicial em relacao a si mesmo
        self.circle_angle  = math.radians(-20.0) #angulo de rotacao em relacao ao centro do circulo
        self.circle_speed  = math.radians(25.0) #degrees per second

        #hammer
        self.left_hand.center = glm.vec3(0.75, 1.1, 0.26)





        ######variaveis
        self.left_foot.rotation_axis = glm.vec3(1,0,0)
        self.right_foot.rotation_axis = glm.vec3(1, 0, 0)

        self.left_hand.rotation_axis = glm.vec3(1, 0, 0)
        self.right_hand.rotation_axis = glm.vec3(0, 1, 0)

        self.body.rotation_axis = glm.vec3(0, 1, 0)

        self.walk_time = 0.0




        #rotacao e translacao inicial
        self.translation = glm.vec3(
            self.circle_center.x + self.circle_radius * math.cos(self.circle_angle),
            self.circle_center.y,
            self.circle_center.z + self.circle_radius * math.sin(self.circle_angle)
        )
        dir_x0 = -math.sin(self.circle_angle)
        dir_z0 =  math.cos(self.circle_angle)
        self.rotation_axis = glm.vec3(0,1,0)
        self.rotation_angle = math.degrees(math.atan2(dir_x0, dir_z0) + self.inicial_angle)
        

        #aplica transformacao
        self.update_transform()



    #faz a animacao e o movimento de andar
    def walk(self, delta_time: float):

        self.walk_anim(delta_time)

        self.walk_move(delta_time)

        self.update_transform()


    #calcula a animacao de andar
    def walk_anim(self, delta_time: float):
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
        self.right_hand.rotation_angle = off_a -  amp_a * seno

        # 9) Ângulo de rotação do corpo (balanço suave)
        self.body.rotation_angle = off_b - amp_b * seno

        # 10) Escala do corpo (bouncing effect)
        bounce_scale = off_s + amp_s * seno_double
        self.body.scale = glm.vec3(1, bounce_scale, 1)

    

    #calcula o movimento de andar
    def walk_move(self, delta_time: float):
        # 1) atualiza ângulo ao longo do tempo
        self.circle_angle += delta_time * self.circle_speed

        # 2) calcula nova posição ao longo do círculo
        x = self.circle_center.x + self.circle_radius * math.cos(self.circle_angle)
        z = self.circle_center.z + self.circle_radius * math.sin(self.circle_angle)
        self.translation = glm.vec3(x, self.translation.y, z)

        # 3) orienta o objeto para a tangente do círculo
        dir_x = -math.sin(self.circle_angle)
        dir_z =  math.cos(self.circle_angle)
        self.rotation_axis = glm.vec3(0,1,0)
        self.rotation_angle = math.degrees(math.atan2(dir_x, dir_z) + self.inicial_angle)




    #reseta os parametros de animacao de andar
    def stop_walk(self):
        self.left_foot.rotation_angle = 0
        self.right_foot.rotation_angle = 0
        self.body.rotation_angle = 0
        self.walk_time = 0.0

        self.body.scale = glm.vec3(1)

        self.update_transform()


    
    def lower_hammer(self):
            self.left_hand.rotation_angle = 125.0
            self.update_transform()

    def raise_hammer(self):
            self.left_hand.rotation_angle = 0.0
            self.update_transform()

