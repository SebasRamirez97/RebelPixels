import pygame
from .funciones_comunes import cargar_imagen as carga

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
