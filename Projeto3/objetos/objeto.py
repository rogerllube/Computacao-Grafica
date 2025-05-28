import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from numpy import random
from PIL import Image

from file_loader import Loader 


class Objeto:
    def __init__(self, loader: Loader):
        self.loader = loader
        self.children = [] 
        self.center = glm.vec3(0.0) # centro para as transformacoes
        self.translation = glm.vec3(0.0)  # Translação local
        self.rotation_angle = 0.0          # Ângulo em radianos
        self.rotation_axis = glm.vec3(0, 0, 1)  # Eixo padrão Z
        self.scale = glm.vec3(1.0)     # Escala local
        self.global_transform = glm.mat4(1.0)
        self.texture_id = 0
        self.vertice_init = 0
        self.vertice_count = 0

        #ID do Grupo de Iluminação
        # 0 = Externo (Padrão), 1 = Interno, 2 = Skybox, etc
        self.group_id = 0 

        # --- Parâmetros de Material (Padrão) ---
        self.ka = 0.1  # Coeficiente ambiente
        self.kd = 0.8  # Coeficiente difuso
        self.ks = 0.1  # Coeficiente especular
        self.ns = 16.0 # Expoente especular

        # --- Parâmetros de Luz (se este objeto for uma fonte de luz) ---
        self.light_on = True
        self.light_color = glm.vec3(1.0, 1.0, 1.0)
        self.light_ambient = 0.1
        self.light_diffuse = 0.8
        self.light_specular = 1.0
        # Valores de atenuação
        self.light_constant = 1.0
        self.light_linear = 0.0014
        self.light_quadratic = 0.0007

    #retorna a matriz de transformacao local
    #nao retorna a matriz global(matriz do pai * matriz local)
    def get_local_transform(self):

        matrix_transform = glm.mat4(1.0)
        
        # Ordem das operações: Scale -> Rotate -> Translate
        matrix_transform = glm.translate(matrix_transform, self.center)

        matrix_transform = glm.translate(matrix_transform, self.translation)
        
        if self.rotation_angle != 0:
            angle = math.radians(self.rotation_angle)
            matrix_transform = glm.rotate(matrix_transform, 
                                         angle, 
                                         self.rotation_axis)
                                         
        matrix_transform = glm.scale(matrix_transform, self.scale)

        matrix_transform = glm.translate(matrix_transform, -self.center)
        
        return matrix_transform
    

    #atualiza o matriz de transformacao global, inclusive dos filhos
    def update_transform(self, parent_transform=glm.mat4(1.0)):
        self.global_transform =  parent_transform * self.get_local_transform()
        for child in self.children:
            child.group_id = self.group_id
            child.update_transform(self.global_transform)

    def get_world_position(self) -> glm.vec3:
        #Retorna a posição atual do objeto no espaço do mundo.
        return glm.vec3(self.global_transform[3])

    #renderiza o objeto e seus filhos
    def draw(self, program):

        # Envia os parâmetros de MATERIAL deste objeto para a GPU
        loc_ka = glGetUniformLocation(program, "ka")
        glUniform1f(loc_ka, self.ka)
        loc_kd = glGetUniformLocation(program, "kd")
        glUniform1f(loc_kd, self.kd)
        loc_ks = glGetUniformLocation(program, "ks")
        glUniform1f(loc_ks, self.ks)
        loc_ns = glGetUniformLocation(program, "ns")
        glUniform1f(loc_ns, self.ns)         

        glUniform1i(glGetUniformLocation(program, "objectGroupID"), self.group_id)
            
        # Envia a matriz de modelo
        loc_model = glGetUniformLocation(program, "model")
        matrix_array = np.array(self.global_transform, dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, matrix_array)

        glBindTexture(GL_TEXTURE_2D, self.texture_id) #define id da textura do modelo
        glDrawArrays(GL_TRIANGLES, self.vertice_init, self.vertice_count) ## renderizando

        for child in self.children:
            child.draw(program)

    #carrega o modelo do objeto
    def load_model(self, obj_file, texture_file):
        self.vertice_init, self.vertice_count, self.texture_id = self.loader.load_obj_and_texture(obj_file, texture_file)
        return self.vertice_init, self.vertice_count, self.texture_id