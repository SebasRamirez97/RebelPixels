import pygame
from .funciones_comunes import cargar_imagen as carga

def imagenes_enemigos():
    caza = carga("RebelPixels/assets/sprites/caza.png" , 0.07)
    bombardero = carga("RebelPixels/assets/sprites/bombardero.png" , 0.08)
    fragata = carga("RebelPixels/assets/sprites/fragata.png" , 0.12)
    carrier = carga("RebelPixels/assets/sprites/carrier.png" , 0.07)
    nodriza = carga("RebelPixels/assets/sprites/nodriza.png" , 0.07)
    return [caza, bombardero, fragata, carrier, nodriza]