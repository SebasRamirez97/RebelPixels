import pygame

def cargar_imagen(direccion, escala):
    imagen = pygame.image.load(direccion)
    imagen = pygame.transform.scale_by(imagen, escala)
    return imagen

def crear_mascara(superficie):
    mascara_superficie = pygame.mask.from_surface(superficie)

    return mascara_superficie