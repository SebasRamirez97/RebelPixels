import pygame
from .funciones_comunes import cargar_imagen as carga
import math
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


def escuadron(nave,pos_lider, distancia, ventana):
    ventana.blit(nave, pos_lider)
    ventana.blit(nave,modificador_cordenada(pos_lider,distancia *-1, distancia *-1))
    ventana.blit(nave,modificador_cordenada(pos_lider,distancia, distancia *-1))
    ventana.blit(nave,modificador_cordenada(pos_lider,distancia *2, distancia *-2))

def varios_escuadrones(cantidad,nave,pos_lider,distancia_naves,distancia_esquad,ventana):
    for i in range(cantidad):
        escuadron(nave,(pos_lider[0]+i*distancia_esquad,pos_lider[1]),distancia_naves,ventana)