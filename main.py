import pygame
import math
from scripts import enemigos 
from scripts.jugador import imagen_jugador as p_image
from scripts.enemigos import imagenes_enemigos as e_image
from scripts.enemigos import poscicion_poligonica as poligono
from scripts.enemigos import varios_escuadrones as multi_squad
from scripts.jugador import procesar_movimiento

pygame.init()

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ventana controlada")
(caza, bombardero, fragata, carrier, nodriza) = e_image()

# Fondo de pantalla
fondo = pygame.image.load("assets/sprites/fondo.png")
fondo = pygame.transform.scale(fondo, (800, 600))


jugador_x = 400 #posicion del jugador
jugador_y = 500
VELOCIDAD_JUGADOR = 5
jugador_sprite = p_image()


corriendo = True
aux_x = 0
aux_y = 0
rot = 0
VELOCIDAD_X = 2
#VELOCIDAD_Y = 2
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
            
    # Acá se refresca la pantalla en cada ciclo, no por cada evento
    ventana.fill((50, 50, 50))  # Fondo gris
    
    # Dibuja el fondo sobre la ventana        
    ventana.blit(fondo, (0, 0))  
    
    #Movimientos enemigos
    aux_x += VELOCIDAD_X
    #aux_y += VELOCIDAD_Y
    #if aux_y == 150:
    if aux_x  > 100 or aux_x <-100:
        VELOCIDAD_X = -VELOCIDAD_X 
    
    #movimiento jugador
    jugador_x, jugador_y = procesar_movimiento(jugador_x, jugador_y, VELOCIDAD_JUGADOR)

    
    multi_squad(3,caza,(150+aux_x,150),50,200,ventana)
    rot += 0.05
    poligono(fragata,0.12,(400+aux_x,300),caza,5,ventana,150,rot)
    #ventana.blit(p_image(),(400-25.6,300-25.6))#pegado de jugador en el fondo
    
    ventana.blit(jugador_sprite, (jugador_x, jugador_y))

    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

