import pygame

def cargar_imagen(direccion, escala):
    imagen = pygame.image.load(direccion)
    imagen = pygame.transform.scale_by(imagen, escala)
    return imagen

def crear_mascara(superficie):
    mascara_superficie = pygame.mask.from_surface(superficie)

    return mascara_superficie


def mostrar_puntuacion(superficie, fuente, puntuacion, color=(255, 255, 255), posicion=(10, 20)):
    texto = fuente.render(f"Puntaje: {puntuacion}", True, color)
    superficie.blit(texto, posicion)
    

def enemigos_destruidos(superficie, fuente, cantidad, color=(255, 255, 255), posicion=(10, 50)):
    texto = fuente.render(f"Enemigos destruidos: {cantidad}", True, color)
    superficie.blit(texto, posicion)
    
        