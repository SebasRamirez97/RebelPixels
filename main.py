import pygame

from scripts.enemigos import crear_conjunto_mascaras as e_mask
from scripts.enemigos import imagenes_enemigos as e_image
from scripts.enemigos import poscicion_poligonica as poligono
from scripts.enemigos import varios_escuadrones as varios_squads
from scripts.escenarios import escenario_1 as esc_1
from scripts.jugador import imagen_jugador as p_image
from scripts.jugador import procesar_movimiento
from scripts.jugador import mascara_jugador as p_mask

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


jugador_x = 400 #posicion del jugador
jugador_y = 500
VELOCIDAD_JUGADOR = 5
jugador_sprite = p_image()

#ESCENARIO 1
y_inicial_squad_a = -100
y_inicial_squad_b = 0
fase_a = "entrada"
fase_b ="entrada"
escuadrones_posiciones_a = varios_squads(3, caza, caza_mask, (150, y_inicial_squad_a), 50, 200)
escuadrones_posiciones_b = varios_squads(3, caza, caza_mask, (150, y_inicial_squad_b), 50, 200)
disparos_enemigos_a = []
disparos_enemigos_b =[]

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
    
    
    #movimiento jugador
    jugador_x, jugador_y = procesar_movimiento(jugador_x, jugador_y, VELOCIDAD_JUGADOR)
    ventana.blit(jugador_sprite, (jugador_x, jugador_y))
    #ESCENARIO 1
    aux_x += VELOCIDAD_X
    if aux_x  > 200 or aux_x < 2:
        VELOCIDAD_X = -VELOCIDAD_X 
    y_inicial_squad_a += 1
    y_inicial_squad_b += 1
    escuadrones_posiciones_a , fase_a , nuevos_disparos_a = esc_1(3, caza, caza_mask, (150, y_inicial_squad_a),(150,100), 50, 200,ventana,
                                          VELOCIDAD_X,jugador_x,jugador_y,jugador_mask,escuadrones_posiciones_a,fase_a,disparos_enemigos_a)
    
    disparos_actualizados_a = []

    for disparo_a in nuevos_disparos_a:
        nueva_y_a = disparo_a["posicion"][1] + disparo_a["velocidad"]
        nueva_pos_a = (disparo_a["posicion"][0], nueva_y_a)

    # Dibujarlo
        pygame.draw.rect(ventana, (255, 0, 0), (*nueva_pos_a, 4, 10))  # Simple proyectil rojo

        # Mantener si sigue en pantalla
        if nueva_y_a < ventana.get_height():
            disparos_actualizados_a.append({**disparo_a, "posicion": nueva_pos_a})

    disparos_enemigos_a = disparos_actualizados_a
    
    escuadrones_posiciones_b , fase_b , nuevos_disparos_b = esc_1(3, caza, caza_mask, (150, y_inicial_squad_b),(150,200), 50, 200,ventana,
                                          VELOCIDAD_X,jugador_x,jugador_y,jugador_mask,escuadrones_posiciones_b,fase_b,disparos_enemigos_b)
    disparos_actualizados_b = []

    for disparo_b in nuevos_disparos_b:
        nueva_y_b = disparo_b["posicion"][1] + disparo_b["velocidad"]
        nueva_pos = (disparo_b["posicion"][0], nueva_y_b)

    # Dibujarlo
        pygame.draw.rect(ventana, (255, 0, 0), (*nueva_pos, 4, 10))  # Simple proyectil rojo

        # Mantener si sigue en pantalla
        if nueva_y_b < ventana.get_height():
            disparos_actualizados_b.append({**disparo_b, "posicion": nueva_pos})

    disparos_enemigos_b = disparos_actualizados_b
    
    #ventana.blit(p_image(),(400-25.6,300-25.6))#pegado de jugador en el fondo
    
    

    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

