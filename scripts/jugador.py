import pygame
from .funciones_comunes import cargar_imagen as carga
from .funciones_comunes import crear_mascara as mascara

def imagen_jugador():
    xwing = carga("assets/sprites/jugador.png" , 0.05)
    return xwing


def procesar_movimiento(mov_x, mov_y, velocidad):
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:  mov_x -= velocidad
    if teclas[pygame.K_RIGHT]: mov_x += velocidad
    if teclas[pygame.K_UP]:    mov_y -= velocidad
    if teclas[pygame.K_DOWN]:  mov_y += velocidad
    return mov_x, mov_y


def mascara_jugador(jugador):
    mask = mascara(jugador)
    return mask


# Lista de proyectiles
proyectiles = []

def disparar(jugador_x, jugador_y):
    # Ajusta la posición inicial
    proyectiles.append([jugador_x + 5 , jugador_y+20])
    proyectiles.append([jugador_x + 43, jugador_y+20])
def actualizar_proyectiles(ventana):
    for p in proyectiles[:]:
        p[1] -= 7  # Velocidad hacia arriba
        if p[1] < 0:
            proyectiles.remove(p)
        pygame.draw.rect(ventana, COLOR_PROYECTIL, (p[0], p[1], ANCHO_PROYECTIL, ALTO_PROYECTIL))
        
#Color proyectil
COLOR_PROYECTIL = (150, 0, 255)
ANCHO_PROYECTIL = 3
ALTO_PROYECTIL = 10

