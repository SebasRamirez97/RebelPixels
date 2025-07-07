import math
import pygame

def detectar_colisiones(jugador_x,jugador_y,mascara_jugador,vidas, escuadrones_a, escuadrones_b,ultimo_golpe,cooldown_ms):
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_golpe < cooldown_ms:
        return vidas, ultimo_golpe
    for escuadron in escuadrones_a + escuadrones_b:
        for nave in escuadron:
            offset = (int(nave["posicion"][0] - jugador_x), int(nave["posicion"][1] - jugador_y))

            if mascara_jugador.overlap(nave["mask_nave"], offset):
                vidas -= 1
    return vidas, ultimo_golpe


def detectar_colisiones_vertices(proyectiles, vertices, nave_central_dict, distancia, rotacion, escala=0.12):
    enemigos_destruidos = 0
    proyectiles_a_remover = []
    ancho, alto = int(1024 * escala), int(1024 * escala)

    for proyectil in proyectiles[:]:
        rect_proj = proyectil["rect"]

        for vertice in vertices:
            if vertice["viva"]:
                i = vertice["indice"]
                angulo = 2 * math.pi * i / len(vertices) + rotacion
                x = nave_central_dict["posicion"][0] + distancia * math.cos(angulo) + ancho / 4
                y = nave_central_dict["posicion"][1] + distancia * math.sin(angulo) + alto / 4
                rect_enemigo = pygame.Rect(x, y, 48, 48)  

                if rect_proj.colliderect(rect_enemigo):
                    vertice["viva"] = False
                    enemigos_destruidos += 1
                    proyectiles_a_remover.append(proyectil)
                    break  

    for p in proyectiles_a_remover:
        if p in proyectiles:
            proyectiles.remove(p)

    return enemigos_destruidos


def detectar_colision_con_jugador(disparos, jugador_x, jugador_y, jugador_sprite, vidas, ultimo_golpe,
                                cooldown_ms, sonido_impacto=None):
    tiempo_actual = pygame.time.get_ticks()
    rect_jugador = pygame.Rect(jugador_x, jugador_y, jugador_sprite.get_width(), jugador_sprite.get_height())

    if tiempo_actual - ultimo_golpe > cooldown_ms:
        for disparo in disparos:
            rect_laser = pygame.Rect(disparo["posicion"][0], disparo["posicion"][1], 4, 10)
            if rect_laser.colliderect(rect_jugador):
                vidas -= 1
                ultimo_golpe = tiempo_actual
                disparo["posicion"] = (-100, -100)

                print("¡El jugador recibió daño! Vidas:", vidas)

                if sonido_impacto:
                    sonido_impacto()

                if vidas <= 0:
                    print("¡Game Over!")
                    return vidas, False, ultimo_golpe

                break  # Evitás múltiples impactos seguidos
    return vidas, True, ultimo_golpe

