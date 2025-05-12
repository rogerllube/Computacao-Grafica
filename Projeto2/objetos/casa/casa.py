import glm
import math
from ..objeto import Objeto

class Casa(Objeto):
    def __init__(self, loader):
        super().__init__(loader)

        self.loader = loader

        self.paredes = Objeto(loader)
        self.paredes.load_model("objetos/casa/Paredes.obj", "objetos/casa/textures/paredes.jpeg")
        self.children.append(self.paredes)

        self.chao = Objeto(loader)
        self.chao.load_model("objetos/casa/Chao.obj", "objetos/casa/textures/chao.jpeg")
        self.children.append(self.chao)

        self.chamine = Objeto(loader)
        self.chamine.load_model("objetos/casa/Chamine.obj", "objetos/casa/textures/tijolo.png")
        self.children.append(self.chamine)

        self.colunas = Objeto(loader)
        self.colunas.load_model("objetos/casa/Colunas.obj", "objetos/casa/textures/tijolo.png")
        self.children.append(self.colunas)

        self.telhadoFrente = Objeto(loader)
        self.telhadoFrente.load_model("objetos/casa/Telhado_frente.obj", "objetos/casa/textures/madeira.jpeg")
        self.children.append(self.telhadoFrente)

        self.telhadoFundo = Objeto(loader)
        self.telhadoFundo.load_model("objetos/casa/Telhado_fundo.obj", "objetos/casa/textures/madeira.jpeg")
        self.children.append(self.telhadoFundo)

        self.telhado = Objeto(loader)
        self.telhado.load_model("objetos/casa/Telhado.obj", "objetos/casa/textures/tijolo.png")
        self.children.append(self.telhado)

        self.tabuas = Objeto(loader)
        self.tabuas.load_model("objetos/casa/Tabuas.obj", "objetos/casa/textures/madeira.jpeg")
        self.children.append(self.tabuas)

        self.batente = Objeto(loader)
        self.batente.load_model("objetos/casa/Batente.obj", "objetos/casa/textures/madeira.jpeg")
        self.children.append(self.batente)

        self.janelas = Objeto(loader)
        self.janelas.load_model("objetos/casa/Janelas.obj", "objetos/casa/textures/madeira.jpeg")
        self.children.append(self.janelas)

        self.scale = glm.vec3(900)
        self.rotation_axis = glm.vec3(0, 1, 0)
        self.rotation_angle = -90.0
        self.update_transform()