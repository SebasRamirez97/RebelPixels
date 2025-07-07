import pygame

from scripts.enemigos import crear_conjunto_mascaras as e_mask
from scripts.enemigos import imagenes_enemigos as e_image
from scripts.disparos import actualizar_y_dibujar_disparos
from scripts.enemigos import varios_escuadrones as varios_squads
from scripts.enemigos import trayectoria_cuadrada as cuadrada
from scripts.escenarios import escenario_1 as esc_1
from scripts.escenarios import escenario_2 as esc_2
from scripts.escenarios import escenario_3 as esc_3
from scripts.jugador import imagen_jugador as p_image
from scripts.jugador import procesar_movimiento
from scripts.jugador import mascara_jugador as p_mask
from scripts.jugador import disparar, actualizar_proyectiles
from scripts.funciones_comunes import mostrar_puntuacion, enemigos_destruidos
from scripts.funciones_comunes import mostrar_pantalla_pausa, mostrar_vidas
from scripts.funciones_comunes import mostrar_pantalla_gameover
from scripts.colisiones import detectar_colisiones, detectar_colisiones_vertices, detectar_colision_con_jugador

pygame.init()
pygame.mixer.init()

from scripts import sonido

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ventana controlada")

sonido.cargar_sonidos()
#sonido.iniciar_musica()
sonido_activado = True # Control de volumen

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
vidas = 3
ultimo_golpe = 0
cooldown_ms = 1000

font = pygame.font.Font(None, 26)

#posicion del jugador
jugador_x = 400 
jugador_y = 500
VELOCIDAD_JUGADOR = 5
jugador_sprite = p_image()

proyectiles = []
proyectiles_jugador = []
vuelta = 1
puntaje_jugador = 0
contador_enemigos = 0
escenario = 1

#ESCENARIO 1
y_inicial_squad_a = -100
y_inicial_squad_b = 0
fase_a = "entrada"
fase_b ="entrada"
escuadrones_posiciones_a = varios_squads(3, caza, caza_mask, (150, y_inicial_squad_a), 50, 200,vuelta)
escuadrones_posiciones_b = varios_squads(3, caza, caza_mask, (150, y_inicial_squad_b), 50, 200,vuelta)
disparos_enemigos_a = []
disparos_enemigos_b =[]

#ESCENARIO 2
fase_a_pol = "entrada"
nave_central_dict_a = None
vertices_estado_a = []
y_inicial_pol_a = -480
pos_central_a = (70,y_inicial_pol_a)
direccion_actual_a = "Derecha"
rot_a = 0
velocidad_x_a = 0
velocidad_y_a = 0
disparos_central_a = []

fase_b_pol = "entrada"
nave_central_dict_b = None
vertices_estado_b = []
y_inicial_pol_b = -210
pos_central_b = (600,y_inicial_pol_b)
direccion_actual_b = "Derecha"
rot_b = 0
velocidad_x_b = 0
velocidad_y_b = 0
disparos_central_b = []

# ESCENARIO 3
fase_carrier_a = "entrada"
y_inicial_carrier_a = -20
dict_carrier_a = None
cooldown_carrier_a = 1000
disparos_enemigos_a = []

# ESCENARIO 3
fase_carrier_b = "entrada"
y_inicial_carrier_b = -20
dict_carrier_b = None
cooldown_carrier_b = 1000
disparos_enemigos_b = []

pausa = False
corriendo = True
aux_x = 0
aux_y = 0
rot = 0
VELOCIDAD_X = 2

reloj = pygame.time.Clock()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False           
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
            pausa = not pausa

    if pausa:
        mostrar_pantalla_pausa(ventana, font)
        reloj.tick(60)
        continue
    
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_m:
            sonido_activado = not sonido_activado  # Alternar entre True y False

            if sonido_activado:
                pygame.mixer.music.set_volume(0.5)
                print("🔊 Sonido activado")
            else:
                pygame.mixer.music.set_volume(0)
                print("🔇 Sonido silenciado")    

    # Acá se refresca la pantalla en cada ciclo, no por cada evento
    ventana.fill((50, 50, 50))  # Fondo gris
    
    # Dibuja el fondo sobre la ventana        
    ventana.blit(fondo, (0, 0))  

    mostrar_puntuacion(ventana, font, puntaje_jugador)
    enemigos_destruidos(ventana, font, contador_enemigos)
    mostrar_vidas(ventana, font, vidas)
    
    #movimiento jugador
    jugador_x, jugador_y = procesar_movimiento(jugador_x, jugador_y, VELOCIDAD_JUGADOR)
    
    #Acrualizar y Dibujar proyectiles
    actualizar_proyectiles(ventana, proyectiles_jugador)
    
    ##Colisiones con enemigos escenario 1
    vidas,ultimo_golpe = detectar_colisiones(jugador_x,jugador_y,jugador_mask,vidas, escuadrones_posiciones_a, escuadrones_posiciones_b,ultimo_golpe,cooldown_ms)
    #contador_enemigos += destruidos
    #score += destruidos * 100
    #if destruidos > 0 and sonido_activado:
    #    sonido.reproducir_explosion()
#
    ##Colisiones con enemigos y naves escenario 2
    #if fase_a_pol == "batalla":
    #    destruidos_a = detectar_colisiones_vertices(proyectiles_jugador, vertices_estado_a, nave_central_dict_a, 120, rot_a)
    #    contador_enemigos += destruidos_a
    #    score += destruidos_a * 100
    #    if destruidos_a > 0 and sonido_activado:
    #        sonido.reproducir_explosion()    

    ##if fase_b_pol == "batalla":
     #   destruidos_b = destruidos_b = detectar_colisiones_vertices(proyectiles_jugador, vertices_estado_b, nave_central_dict_b, 120, rot_b)
     #   contador_enemigos += destruidos_b
     #   score += destruidos_b * 100
     #   if destruidos_b > 0 and sonido_activado:
     #       sonido.reproducir_explosion()
    
    # Movimiento de disparo
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        disparar(jugador_x, jugador_y, proyectiles_jugador) 
    
    if pygame.time.get_ticks() - ultimo_golpe < 1000:
        herido = jugador_sprite.copy()
        herido.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
        ventana.blit(herido, (jugador_x, jugador_y))
    else:
        ventana.blit(jugador_sprite, (jugador_x, jugador_y))
    
    match escenario
        case 1:
            #ESCENARIO 1
            aux_x += VELOCIDAD_X
            if aux_x  > 150 or aux_x < 2:
                VELOCIDAD_X = -VELOCIDAD_X

            #Escuadron A
            y_inicial_squad_a += 1
            escuadrones_posiciones_a , fase_a , nuevos_disparos_a, puntaje_jugador, contador_enemigos = esc_1(3, caza, caza_mask, (150, y_inicial_squad_a),(150,100), 50, 200,ventana,
            VELOCIDAD_X,jugador_x,jugador_y,jugador_mask,proyectiles_jugador,puntaje_jugador,escuadrones_posiciones_a,fase_a,disparos_enemigos_a,vuelta,contador_enemigos)
    
            disparos_enemigos_a = actualizar_y_dibujar_disparos(nuevos_disparos_a, ventana)

            #Escuadron B
            y_inicial_squad_b += 1
            escuadrones_posiciones_b , fase_b , nuevos_disparos_b,puntaje_jugador,contador_enemigos = esc_1(3, caza, caza_mask, (150, y_inicial_squad_b),(150,200), 50, 200,ventana,
                                                                                                    VELOCIDAD_X,jugador_x,jugador_y,jugador_mask,proyectiles_jugador,puntaje_jugador,escuadrones_posiciones_b,fase_b,disparos_enemigos_b,vuelta,contador_enemigos)

            disparos_enemigos_b = actualizar_y_dibujar_disparos(nuevos_disparos_b, ventana)
    
            if(not any(escuadrones_posiciones_a)and not any(escuadrones_posiciones_b)):
                escenario = 2
        
        case 2:
            #ESCENARIO 2
            
            velocidad_x_a, velocidad_y_a, direccion_actual_a = cuadrada(pos_central_a,direccion_actual_a,70,600,100,370)
            y_inicial_pol_a += 2
            rot_a += 0.05
    
            pos_central_a, fase_a_pol, nave_central_dict_a, vertices_estado_a, nuevos_disparos_central_a,puntaje_jugador,contador_enemigos,vertices_vivos_a,estado_central_a = esc_2(
            fase_a_pol, nave_central_dict_a,disparos_central_a, vertices_estado_a,
            fragata, 0.12, fragata_mask, (70,y_inicial_pol_a),
            (70,100), caza, caza_mask, 6,
            120, rot_a, velocidad_x_a, velocidad_y_a,
            jugador_x, jugador_y, jugador_mask,proyectiles_jugador,puntaje_jugador, ventana,vuelta,contador_enemigos)  
    
            disparos_central_a = actualizar_y_dibujar_disparos(nuevos_disparos_central_a, ventana)   
    
            velocidad_x_b, velocidad_y_b, direccion_actual_b = cuadrada(pos_central_b,direccion_actual_b,70,600,100,370)
            y_inicial_pol_b += 2
            rot_b += 0.05
            pos_central_b, fase_b_pol, nave_central_dict_b, vertices_estado_b, nuevos_disparos_central_b,puntaje_jugador,contador_enemigos,vertices_vivos_b,estado_central_b = esc_2(
            fase_b_pol, nave_central_dict_b,disparos_central_b, vertices_estado_b,
            fragata, 0.12, fragata_mask, (600,y_inicial_pol_b),
            (600,370), caza, caza_mask, 6,
            120, rot_b, velocidad_x_b, velocidad_y_b,
            jugador_x, jugador_y, jugador_mask,proyectiles_jugador,puntaje_jugador, ventana, vuelta,contador_enemigos)
         
            disparos_central_b = actualizar_y_dibujar_disparos(nuevos_disparos_central_b, ventana)
            if estado_central_a == "destruido" and estado_central_b == "destruido" and  (vertices_vivos_a + vertices_vivos_b) == 0:
                fase_a_pol = "entrada"
                fase_b_pol = "entrada"
                y_inicial_pol_a = 0
                y_inicial_pol_b = 0
                rot_a = 0
                rot_b = 0
                nave_central_dict_a = {}  
                nave_central_dict_b = {}
                vertices_estado_a = []
                vertices_estado_b = []
                #PENDIENTE CREAR FUNCION RESET_POLIGONICA EN ENEMIGOS
                escenario = 3
            
        case 3:
            #ESCENARIO 3
            tick_actual = pygame.time.get_ticks()
            
            #CARRIER A
            y_inicial_carrier_a += 2
            fase_carrier_a, dict_carrier_a, nuevos_disparos_a= esc_3(fase_carrier_a,dict_carrier_a,carrier,carrier_mask,(100, y_inicial_carrier_a),(100, 100),jugador_x,jugador_y,jugador_mask,ventana,tick_actual,bombardero,bombardero_mask,5,cooldown_carrier_a,disparos_enemigos_a)
            disparos_enemigos_a = actualizar_y_dibujar_disparos(nuevos_disparos_a, ventana)
        
            #CARRIER B
            y_inicial_carrier_b += 2
            fase_carrier_b, dict_carrier_b, nuevos_disparos_b= esc_3(fase_carrier_b,dict_carrier_b,carrier,carrier_mask,(546.6, y_inicial_carrier_b),(546.6, 100),jugador_x,jugador_y,jugador_mask,ventana,tick_actual,bombardero,bombardero_mask,5,cooldown_carrier_b,disparos_enemigos_b)
            disparos_enemigos_b = actualizar_y_dibujar_disparos(nuevos_disparos_b, ventana)
    
    vidas, corriendo, ultimo_golpe = detectar_colision_con_jugador(disparos_enemigos_a + disparos_enemigos_b,
    jugador_x, jugador_y, jugador_sprite, vidas, ultimo_golpe, 1000, sonido.reproducir_danio if sonido_activado else None)

    vidas, corriendo, ultimo_golpe = detectar_colision_con_jugador(disparos_central_a + disparos_central_b,
    jugador_x, jugador_y, jugador_sprite, vidas, ultimo_golpe, 1000, sonido.reproducir_danio if sonido_activado else None)
    
    if vidas <= 0:
        mostrar_pantalla_gameover(ventana, font, score)

        # Reiniciar variables recién después de ENTER
        vidas = 3
        score = 0
        contador_enemigos = 0
        jugador_x, jugador_y = 400, 500
        proyectiles_jugador.clear()
        escuadrones_posiciones_a.clear()
        escuadrones_posiciones_b.clear()
        fase_a_pol = "espera"
        fase_b_pol = "espera"
        ultimo_golpe = pygame.time.get_ticks()


    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
