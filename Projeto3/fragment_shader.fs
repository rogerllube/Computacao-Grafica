#version 330 core

out vec4 FragColor;

// --- Entradas do Vertex Shader ---
in vec2 out_texture;
in vec3 out_normal;
in vec3 out_fragPos;

// --- Struct da Luz ---
struct PointLight {
    vec3 position;
    vec3 color;

    // Intensidades individuais
    float ambient;
    float diffuse;
    float specular;

    // Atenuação
    float constant;
    float linear;
    float quadratic;

    //ID do Grupo da Luz
    int groupID;

    //Se esta aceso
    int on;
};

// --- Constantes e Uniforms ---
#define MAX_LIGHTS 10
uniform PointLight lights[MAX_LIGHTS];
uniform int numActiveLights;
uniform vec3 viewPos;
uniform sampler2D samplerTexture;

// Uniforms de Material
uniform float ka;
uniform float kd;
uniform float ks;
uniform float ns;

//Uniforms globais editaveis com tecla
uniform float globalAmbientLevel;
uniform float globalDiffuseMult;
uniform float globalSpecularMult;

//ID do Grupo do Objeto
uniform int objectGroupID;



// --- Função para Calcular uma Luz ---
vec3 CalcPointLight(PointLight light, vec3 norm, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);

    // --- Atenuação ---
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

    // --- Componentes (Usando intensidades da LUZ e coeficientes do MATERIAL) ---
    // Ambiente
    vec3 ambient_comp = light.ambient * light.color * ka;

    // Difusa
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse_comp = light.diffuse * diff * light.color * kd * globalDiffuseMult;

    // Especular
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
    vec3 specular_comp = light.specular * spec * light.color * ks * globalSpecularMult;

    // Aplica a atenuação
    return (ambient_comp + diffuse_comp + specular_comp) * attenuation;
}

// --- Shader Principal ---
void main() {
    vec3 norm = normalize(out_normal);
    vec3 viewDir = normalize(viewPos - out_fragPos);
    vec4 texColor = texture(samplerTexture, out_texture);

    vec3 ambient_global = vec3(globalAmbientLevel);

    // Acumula o efeito de todas as luzes ativas
    vec3 light_result = vec3(0.0, 0.0, 0.0);
    for(int i = 0; i < numActiveLights; i++) {
        if (lights[i].groupID == objectGroupID && lights[i].on == 1) {
            light_result += CalcPointLight(lights[i], norm, out_fragPos, viewDir);
        }
    }

    // A cor final é o resultado acumulado das luzes, modulado pela textura
    FragColor = vec4((ambient_global + light_result), 1.0) * texColor;
}