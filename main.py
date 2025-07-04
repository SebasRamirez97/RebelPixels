import pygame

from scripts.enemigos import crear_conjunto_mascaras as e_mask
from scripts.enemigos import imagenes_enemigos as e_image
from scripts.enemigos import poscicion_poligonica as poligono
from scripts.enemigos import varios_escuadrones as varios_squads
from scripts.escenarios import escenario_1 as esc_1
from scripts.jugador import imagen_jugador as p_image
from scripts.jugador import procesar_movimiento
from scripts.jugador import mascara_jugador as p_mask
from scripts.jugador import disparar, actualizar_proyectiles
from scripts.funciones_comunes import mostrar_puntuacion, enemigos_destruidos

pygame.init()

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ventana controlada")
(caza, bombardero, fragata, carrier, nodriza) = e_image()
(caza, bombardero, fragata, carrier, nodriza) = e_image()
(caza_mask, bombardero_mask, fragata_mask, carrier_mask, nodriza_mask) = e_mask(e_image())
jugador_sprite = p_image()
jugador_mask = p_mask(jugador_sprite)


# Fondo de pantalla
fondo = pygame.image.load("assets/sprites/fondo.png")
fondo = pygame.transform.scale(fondo, (800, 600))

#ventana puntaje
score = 0
contador_enemigos = 0
font = pygame.font.Font(None, 26)

jugador_x = 400 #posicion del jugador
jugador_y = 500
VELOCIDAD_JUGADOR = 5
jugador_sprite = p_image()
#ESCENARIO 1
y_inicial_squad = 0
fase = "entrada"
escuadrones_posiciones = varios_squads(3, caza, caza_mask, (150, y_inicial_squad), 50, 200)

corriendo = True
aux_x = 0
aux_y = 0
rot = 0
VELOCIDAD_X = 2

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
            
    # Acá se refresca la pantalla en cada ciclo, no por cada evento
    ventana.fill((50, 50, 50))  # Fondo gris
    
    # Dibuja el fondo sobre la ventana        
    ventana.blit(fondo, (0, 0))  

    mostrar_puntuacion(ventana, font, score)
    enemigos_destruidos(ventana, font, contador_enemigos)
    
    #Dibujar proyectiles
    actualizar_proyectiles(ventana)

    #movimiento jugador
    jugador_x, jugador_y = procesar_movimiento(jugador_x, jugador_y, VELOCIDAD_JUGADOR)
    # Movimiento de disparo
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        disparar(jugador_x, jugador_y)


    #ESCENARIO 1
    aux_x += VELOCIDAD_X
    if aux_x  > 200 or aux_x < 2:
        VELOCIDAD_X = -VELOCIDAD_X 
    y_inicial_squad += 1
    
    escuadrones_posiciones , fase = esc_1(3, caza, caza_mask, (150, y_inicial_squad),(150,150), 50, 200,ventana,
                                        VELOCIDAD_X,jugador_x,jugador_y,jugador_mask,escuadrones_posiciones,fase)
    if not any(escuadrones_posiciones):
        print("Escenario 1 destruido")
    
    rot += 0.05
    poligono(fragata,0.12,(400+aux_x,300),caza,5,ventana,150,rot)
    #ventana.blit(p_image(),(400-25.6,300-25.6))#pegado de jugador en el fondo
    
    ventana.blit(jugador_sprite, (jugador_x, jugador_y))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

