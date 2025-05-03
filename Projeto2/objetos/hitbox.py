import glm

class Hitbox:
    def __init__(self, pos = glm.vec3(0), radius = 0):
        self.pos = pos
        self.radius = radius

    def is_hit(self, other: 'Hitbox') -> bool:
        # Calcula a distância 2D entre os centros (ignora o eixo Z)
        diff = glm.vec2(other.pos.x, other.pos.z) - glm.vec2(self.pos.x, self.pos.z)
        distance = glm.length(diff)
        return distance <= (self.radius + other.radius)
