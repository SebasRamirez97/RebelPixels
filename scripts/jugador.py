import pygame
from .funciones_comunes import cargar_imagen as carga

def imagen_jugador():
    xwing = carga("RebelPixels/assets/sprites/jugador.png" , 0.05)
    return xwing