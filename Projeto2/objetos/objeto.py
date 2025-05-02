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
        self.translation = glm.vec3(0.0)  # Translação local
        self.rotation_angle = 0.0          # Ângulo em radianos
        self.rotation_axis = glm.vec3(0, 0, 1)  # Eixo padrão Z
        self.scale = glm.vec3(1.0)     # Escala local
        self.global_transform = glm.mat4(1.0)
        self.texture_id = 0
        self.vertice_init = 0
        self.vertice_count = 0


    def get_local_transform(self):

        matrix_transform = glm.mat4(1.0)
        
        # Ordem das operações: Scale -> Rotate -> Translate
        matrix_transform = glm.translate(matrix_transform, self.translation)
        
        if self.rotation_angle != 0:
            angle = math.radians(self.rotation_angle)
            matrix_transform = glm.rotate(matrix_transform, 
                                         angle, 
                                         self.rotation_axis)
                                         
        matrix_transform = glm.scale(matrix_transform, self.scale)
        
        return matrix_transform
    


    def update_transform(self, parent_transform=glm.mat4(1.0)):
        self.global_transform =  self.get_local_transform() * parent_transform
        for child in self.children:
            child.update_transform(self.global_transform)


    def draw(self, program):
        loc_model = glGetUniformLocation(program, "model")
        matrix_array = np.array(self.global_transform, dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, matrix_array)

        glBindTexture(GL_TEXTURE_2D, self.texture_id) #define id da textura do modelo
        glDrawArrays(GL_TRIANGLES, self.vertice_init, self.vertice_count) ## renderizando

        for child in self.children:
            child.draw(program)


    def load_model(self, obj_file, texture_file):
        self.vertice_init, self.vertice_count, self.texture_id = self.loader.load_obj_and_texture(obj_file, texture_file)
        return self.vertice_init, self.vertice_count, self.texture_id