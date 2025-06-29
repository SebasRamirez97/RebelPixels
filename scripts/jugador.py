import pygame

def imagen_jugador():
    xwing = pygame.image.load("RebelPixels/assets/sprites/jugador.png")
    xwing = pygame.transform.scale_by(xwing, 0.07)
    return xwing