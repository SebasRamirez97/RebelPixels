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


def disparar(jugador_x, jugador_y, proyectiles):
    proyectiles.append({
        "rect": pygame.Rect(jugador_x + 5, jugador_y + 20, ANCHO_PROYECTIL, ALTO_PROYECTIL),
        "surface": None  # O una imagen si tenés sprite para el láser
    })
    proyectiles.append({
        "rect": pygame.Rect(jugador_x + 43, jugador_y + 20, ANCHO_PROYECTIL, ALTO_PROYECTIL),
        "surface": None
    })

def actualizar_proyectiles(ventana, proyectiles):
    for p in proyectiles[:]:
        p["rect"].y -= 7
        pygame.draw.rect(ventana, COLOR_PROYECTIL, p["rect"])  # O usás p["surface"] si tenés sprite
        if p["rect"].bottom < 0:
            proyectiles.remove(p)

#Color proyectil
COLOR_PROYECTIL = (150, 0, 255)
ANCHO_PROYECTIL = 3
ALTO_PROYECTIL = 10

