import pygame
from scripts import enemigos 
from scripts.jugador import imagen_jugador as jimage

pygame.init()

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ventana controlada")



corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Acá se refresca la pantalla en cada ciclo, no por cada evento
    ventana.fill((50, 50, 50))  # Fondo negro
    ventana.blit(jimage(), (360,500))  
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    

pygame.quit()

