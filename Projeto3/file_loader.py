from OpenGL.GL import *
from PIL import Image

class Loader:
    def __init__(self):
        self.vertices_list = []
        self.textures_coord_list = []
        self.normals_list = []
        self.numberTextures = 0

        glEnable(GL_TEXTURE_2D)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        glEnable(GL_LINE_SMOOTH)



    def load_model_from_file(self, filename):
        """Loads a Wavefront OBJ file. """
        objects = {}
        vertices = []
        normals = []
        texture_coords = []
        faces = []

        material = None

        # abre o arquivo obj para leitura
        for line in open(filename, "r"): ## para cada linha do arquivo .obj
            """Loads a Wavefront OBJ file. """

        # abre o arquivo obj para leitura
        for line in open(filename, "r"): ## para cada linha do arquivo .obj
            if line.startswith('#'): continue ## ignora comentarios
            values = line.split() # quebra a linha por espaço
            if not values: continue

            ### recuperando vertices
            if values[0] == 'v':
                vertices.append(values[1:4])

            ### recuperando normais
            if values[0] == 'vn':
                normals.append(values[1:4])

            ### recuperando coordenadas de textura
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            ### recuperando faces 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                face_normals = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    face_normals.append(int(w[2]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, face_normals, material))

        model = {}
        model['vertices'] = vertices
        model['texture'] = texture_coords
        model['faces'] = faces
        model['normals'] = normals

        return model

    def load_texture_from_file(self, img_textura):
        texture_id = self.numberTextures
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        img = Image.open(img_textura)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)
        #image_data = np.array(list(img.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

        self.numberTextures += 1
        return texture_id

    '''
    É possível encontrar, na Internet, modelos .obj cujas faces não sejam triângulos. Nesses casos, precisamos gerar triângulos a partir dos vértices da face.
    A função abaixo retorna a sequência de vértices que permite isso. Créditos: Hélio Nogueira Cardoso e Danielle Modesti (SCC0650 - 2024/2).
    '''
    def circular_sliding_window_of_three(self, arr):
        if len(arr) == 3:
            return arr
        circular_arr = arr + [arr[0]]
        result = []
        for i in range(len(circular_arr) - 2):
            result.extend(circular_arr[i:i+3])
        return result


    def load_obj_and_texture(self, objFile, texture_file):
        modelo = self.load_model_from_file(objFile)
        
        ### inserindo vertices do modelo no vetor de vertices
        verticeInicial = len(self.vertices_list)
        print('Processando modelo {}. Vertice inicial: {}'.format(objFile, len(self.vertices_list)))

        for face_data in modelo['faces']:
            face_indices, texture_indices, normal_indices, material = face_data

            # --- INÍCIO DA MODIFICAÇÃO (TRIANGULAÇÃO) ---
            if len(face_indices) < 3:
                continue # Ignora linhas ou pontos

            # Se já for um triângulo, adiciona como está
            if len(face_indices) == 3:
                triangles_v = [face_indices[0], face_indices[1], face_indices[2]]
                triangles_t = [texture_indices[0], texture_indices[1], texture_indices[2]]
                triangles_n = [normal_indices[0], normal_indices[1], normal_indices[2]]
            else:
                # Se for um polígono (ex: 4+ vértices), usa triangulação em leque
                # (V0, V1, V2), (V0, V2, V3), (V0, V3, V4), ...
                triangles_v = []
                triangles_t = []
                triangles_n = []
                v0, t0, n0 = face_indices[0], texture_indices[0], normal_indices[0]

                for i in range(1, len(face_indices) - 1):
                    v1, t1, n1 = face_indices[i], texture_indices[i], normal_indices[i]
                    v2, t2, n2 = face_indices[i+1], texture_indices[i+1], normal_indices[i+1]
                    
                    triangles_v.extend([v0, v1, v2])
                    triangles_t.extend([t0, t1, t2])
                    triangles_n.extend([n0, n1, n2])
            
            # Adiciona os vértices triangulados às listas
            for v_idx in triangles_v:
                self.vertices_list.append(modelo['vertices'][v_idx - 1])
            for t_idx in triangles_t:
                # Cuidado com o índice 0 que você adiciona se a textura não existir!
                # Se o índice for 0, você precisa decidir o que fazer (usar um padrão ou pular)
                # Aqui, assumimos que 0 significa o primeiro (índice 0), mas seu OBJ usa 1-based.
                # Se 0 significa "sem textura", você precisará de um tratamento especial.
                # A linha abaixo assume que 0 se torna -1 e pega o último, o que é PROVAVELMENTE ERRADO.
                # É melhor garantir que seus OBJs TENHAM coordenadas de textura ou ter um padrão.
                # Uma abordagem mais segura se 0 significa "sem textura":
                if t_idx > 0:
                   self.textures_coord_list.append(modelo['texture'][t_idx - 1])
                else:
                   self.textures_coord_list.append([0.0, 0.0]) # Adiciona uma coordenada padrão (0,0)
                   
            for n_idx in triangles_n:
                self.normals_list.append(modelo['normals'][n_idx - 1])
            
        verticeFinal = len(self.vertices_list)
        print('Processando modelo {}. Vertice final: {}'.format(objFile, len(self.vertices_list)))
        
        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        texture_id = self.load_texture_from_file(texture_file)
            
        
        return verticeInicial, verticeFinal - verticeInicial, texture_id