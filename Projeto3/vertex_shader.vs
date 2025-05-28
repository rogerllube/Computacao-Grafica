#version 330 core

// Entradas do VBO
in vec3 position;
in vec2 texture_coord;
in vec3 normals;

// Saídas para o Fragment Shader
out vec2 out_texture;
out vec3 out_fragPos; // Posição no Espaço do Mundo
out vec3 out_normal;  // Normal no Espaço do Mundo

// Uniforms
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    // Calcula a posição final na tela
    gl_Position = projection * view * model * vec4(position, 1.0);

    // Passa a coordenada de textura
    out_texture = texture_coord; // O nome da entrada é texture_coord

    // Calcula a posição do fragmento no Espaço do Mundo
    out_fragPos = vec3(model * vec4(position, 1.0));

    // Calcula a normal CORRETA no Espaço do Mundo
    // Usamos a inversa transposta da matriz de modelo (sem translação)
    // Isso garante que as normais permaneçam perpendiculares mesmo com escalas.
    out_normal = mat3(transpose(inverse(model))) * normals;
}