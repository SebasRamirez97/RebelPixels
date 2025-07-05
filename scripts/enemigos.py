import math
import random

from .funciones_comunes import cargar_imagen as carga
from .funciones_comunes import crear_mascara as mascara
from .funciones_comunes import generar_diccionario as diccionario

def imagenes_enemigos():
    caza = carga("assets/sprites/caza.png" , 0.07)
    bombardero = carga("assets/sprites/bombardero.png" , 0.08)
    fragata = carga("assets/sprites/fragata.png" , 0.12)
    carrier = carga("assets/sprites/carrier.png" , 0.12)
    nodriza = carga("assets/sprites/nodriza.png" , 0.12)
    return [caza, bombardero, fragata, carrier, nodriza]

def crear_conjunto_mascaras(lista_superficies):
    lista_mascaras = []
    for superficie in lista_superficies:
        mask = mascara(superficie)
        lista_mascaras.append(mask)

    return lista_mascaras

def modificador_cordenada(pos_inicial,x,y):
    a = pos_inicial[0] + x
    b = pos_inicial[1] + y

    return (a,b)

def escuadron(nave,mask_nave,pos_lider, distancia):
    
    lista_diccionarios_naves = []
    formacion = [
    pos_lider,
    modificador_cordenada(pos_lider,distancia *-1, distancia *-1),
    modificador_cordenada(pos_lider,distancia, distancia *-1),
    modificador_cordenada(pos_lider,distancia *2, distancia *-2)]

    for posicion in formacion:
        diccionario_nave = {
            "posicion": posicion,
            "sprite_nave": nave,
            "mask_nave": mask_nave
        }
        lista_diccionarios_naves.append(diccionario_nave)
        
    return lista_diccionarios_naves
        
    

def varios_escuadrones(cantidad,nave,mask_nave,pos_lider,distancia_naves,distancia_esquad):
    lista_escuadrones = []
    for i in range(cantidad):
        base = (pos_lider[0]+i*distancia_esquad,pos_lider[1])
        escuadron_pos = escuadron(nave,mask_nave,base,distancia_naves)
        lista_escuadrones.append(escuadron_pos)

    return lista_escuadrones

def entrada_varios_escuadrones(cantidad,nave,mask_nave,pos_inicial,pos_final,distancia_naves,distancia_squad,ventana):
    
    fase = "entrada"
    escuadrones_posiciones = varios_escuadrones(cantidad,nave,mask_nave, pos_inicial, distancia_naves, distancia_squad)

    for escuadron in escuadrones_posiciones:
        for nave_enemiga in escuadron:
            ventana.blit(nave_enemiga["sprite_nave"], nave_enemiga["posicion"])

    if pos_inicial[1] >= pos_final[1]:
        fase = "batalla"
        escuadrones_posiciones = varios_escuadrones(cantidad, nave, mask_nave, pos_final, distancia_naves, distancia_squad)
    
    diccionario_situacion = {
        "fase" : fase,
        "escuadrones_posiciones" : escuadrones_posiciones
    }
    return diccionario_situacion

def batalla_varios_escuadrones(lista_escuadrones,velocidad_x,jugador_x,jugador_y,jugador_mask,ventana,disparos_enemigos):
    nuevos_escuadrones = []
    for escuadron in lista_escuadrones:
        escuadron_vivo = []
        for nave in escuadron:

            nave["posicion"] = (nave["posicion"][0] + velocidad_x, nave["posicion"][1])
            
            if random.randint(1, 180) == 1:  # 1 en 180 chance
                disparo = {"posicion": (nave["posicion"][0] + 34, nave["posicion"][1] + 30),
                            "velocidad": 5}
                disparos_enemigos.append(disparo)
            
            offset = (int(nave["posicion"][0] - jugador_x), int(nave["posicion"][1] - jugador_y))

            if jugador_mask.overlap(nave["mask_nave"], offset):
                print("💥 Nave destruida")
                # Acá podrías agregar explosión o sonido
            else:
                ventana.blit(nave["sprite_nave"], nave["posicion"])
                escuadron_vivo.append(nave)

        nuevos_escuadrones.append(escuadron_vivo)
    return nuevos_escuadrones , disparos_enemigos

def formacion_poligonica(nave_central,escala,mask_nave_central, pos_nave_central, nave_vertice,mask_nave_vertice,cantidad,distancia,rotacion):
    
    diccionario_nave_central = diccionario(nave_central,mask_nave_central,pos_nave_central)
    
    lista_diccionarios_poligomica = [diccionario_nave_central]
    
    for i in range(cantidad):
        angulo = 2 * math.pi * i / cantidad + rotacion
        x = pos_nave_central[0]  + distancia * math.cos(angulo) + (1024 * escala)/4
        y = pos_nave_central[1]  + distancia * math.sin(angulo) + (1024 * escala)/4
        pos_nave_vertice = (x,y)
        diccionario_nave_vertice = diccionario(nave_vertice,mask_nave_vertice,pos_nave_vertice)
        lista_diccionarios_poligomica.append(diccionario_nave_vertice)
    
    return lista_diccionarios_poligomica

def entrada_poligonica(nave_central, escala, mask_nave_central, pos_inicial_nave_central,
                       pos_final_nave_central, nave_vertice, mask_nave_vertice,
                       cantidad, distancia, rotacion, ventana):
    
    fase = "entrada"
    posicion_central_poligonica = pos_inicial_nave_central

    naves_poligomicas = formacion_poligonica(
        nave_central, escala, mask_nave_central, posicion_central_poligonica,
        nave_vertice, mask_nave_vertice, cantidad, distancia, rotacion
    )

    for nave in naves_poligomicas:
        ventana.blit(nave["sprite_nave"], nave["posicion"])

    if (pos_inicial_nave_central >= pos_final_nave_central):
        fase = "batalla"
        posicion_central_poligonica = pos_final_nave_central

    nave_central_dict = diccionario(nave_central, mask_nave_central, posicion_central_poligonica)
    diccionario_situacion = {
        "fase": fase,
        "posicion": posicion_central_poligonica,
        "nave_central": nave_central_dict
    }
    return diccionario_situacion

def inicializar_vertices_poligono(cantidad):
    vertices = []
    for i in range(cantidad):
        vertice = {
            "indice": i,
            "viva": True,
            # Podés agregar más propiedades si querés:
            # "tipo_disparo": disparo_laser_rapido,
            # "salud": 100,
        }
        vertices.append(vertice)
    return vertices

def batalla_poligomica(nave_central_dict, vertices_estado, escala, nave_vertice_sprite, mask_nave_vertice,
                       distancia, rotacion, velocidad_x, velocidad_y,
                       jugador_x, jugador_y, jugador_mask, ventana):

    # Mover nave central
    pos_central = nave_central_dict["posicion"]
    nueva_pos_central = (pos_central[0] + velocidad_x, pos_central[1] + velocidad_y)
    nave_central_dict["posicion"] = nueva_pos_central

    # Dibujar nave central
    ventana.blit(nave_central_dict["sprite_nave"],nave_central_dict["posicion"] )

    # Dibujar vértices vivos
    for vertice in vertices_estado:
        if vertice["viva"]:
            i = vertice["indice"]
            angulo = 2 * math.pi * i / len(vertices_estado) + rotacion
            x = nave_central_dict["posicion"][0] + distancia * math.cos(angulo) + (1024 * escala) / 4
            y = nave_central_dict["posicion"][1] + distancia * math.sin(angulo) + (1024 * escala) / 4
            pos = (x, y)

            offset = (int(pos[0] - jugador_x), int(pos[1] - jugador_y))
            if jugador_mask.overlap(mask_nave_vertice, offset):
                print(f"💥 Colisión con vértice {i}")
                vertice["viva"] = False
            else:
                ventana.blit(nave_vertice_sprite, pos)

    return nave_central_dict, vertices_estado

def trayectoria_cuadrada(posicion, direccion_actual, x_min, x_max, y_min, y_max):
    x, y = posicion
    velocidad_x = 0
    velocidad_y = 0

    if direccion_actual == "derecha":
        velocidad_x = 5
        velocidad_y = 0
        if x >= x_max:
            direccion_actual = "abajo"

    elif direccion_actual == "abajo":
        velocidad_x = 0
        velocidad_y = 5
        if y >= y_max:
            direccion_actual = "izquierda"

    elif direccion_actual == "izquierda":
        velocidad_x = -5
        velocidad_y = 0
        if x <= x_min:
            direccion_actual = "arriba"

    elif direccion_actual == "arriba":
        velocidad_x = 0
        velocidad_y = -5
        if y <= y_min:
            direccion_actual = "derecha"

    else:
        # Por si dirección_actual tiene un valor inesperado
        velocidad_x = 0
        velocidad_y = 0
        direccion_actual = "derecha"

    return velocidad_x, velocidad_y, direccion_actual