import pygame
from scripts import enemigos 
from scripts.jugador import imagen_jugador as p_image
from scripts.enemigos import imagenes_enemigos as e_image


pygame.init()

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ventana controlada")



corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Acá se refresca la pantalla en cada ciclo, no por cada evento
    ventana.fill((50, 50, 50))  # Fondo gris
    ventana.blit(p_image(),(360,500))#pegado de jugador en el fondo
    x0 = 300
    x1 = 280
    x2 = 230

    for i in range(0,3):    
        ventana.blit(e_image()[0],(x0,200))
        ventana.blit(e_image()[1],(x1,150))
        x0 += 50
        x1 += 70
    for i in range(0,2):
        ventana.blit(e_image()[2],(x2,50))
        x2 += 190
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    

pygame.quit()

