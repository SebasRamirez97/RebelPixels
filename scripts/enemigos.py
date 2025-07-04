import pygame
from .funciones_comunes import cargar_imagen as carga
from .funciones_comunes import crear_mascara as mascara
import math
import random
def imagenes_enemigos():
    caza = carga("assets/sprites/caza.png" , 0.07)
    bombardero = carga("assets/sprites/bombardero.png" , 0.08)
    fragata = carga("assets/sprites/fragata.png" , 0.12)
    carrier = carga("assets/sprites/carrier.png" , 0.12)
    nodriza = carga("assets/sprites/nodriza.png" , 0.12)
    return [caza, bombardero, fragata, carrier, nodriza]

def poscicion_poligonica(nave_central,escala, pos_nave_central, nave_vertice,cantidad,ventana,distancia,rotacion):
    
    ventana.blit(nave_central, pos_nave_central)
    for i in range(cantidad):
        angulo = 2 * math.pi * i / cantidad + rotacion
        x = pos_nave_central[0]  + distancia * math.cos(angulo) + (1024 * escala)/4
        y = pos_nave_central[1]  + distancia * math.sin(angulo) + (1024 * escala)/4
        vertice = (x,y)
        ventana.blit(nave_vertice,vertice)

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

def crear_conjunto_mascaras(lista_superficies):
    lista_mascaras = []
    for superficie in lista_superficies:
        mask = mascara(superficie)
        lista_mascaras.append(mask)

    return lista_mascaras