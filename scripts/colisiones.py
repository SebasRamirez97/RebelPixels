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


def detectar_colisiones_vertices(jugador_x,jugador_y,mascara_jugador, vertices, nave_central_dict, distancia, rotacion, vidas,ultimo_golpe,cooldown_ms, escala=0.12):
    tiempo_actual = pygame.time.get_ticks()
        
    if tiempo_actual - ultimo_golpe < cooldown_ms:
            return vidas, ultimo_golpe
    
    for vertice in vertices:
        if vertice["estado"]=="activo":
            i = vertice["indice"]
            angulo = 2 * math.pi * i / len(vertices) + rotacion
            x = nave_central_dict["posicion"][0] + distancia * math.cos(angulo) + (1024 * escala) / 4
            y = nave_central_dict["posicion"][1] + distancia * math.sin(angulo) + (1024 * escala) / 4
            vertice["posicion"] = (x,y)
            pos = (x, y)
            offset_vertice = (int(pos[0] - jugador_x), int(pos[1] - jugador_y))

            
            if mascara_jugador.overlap(vertice["mask_nave"], offset_vertice):
                vidas-=1
                ultimo_golpe = tiempo_actual
                break
    offset_nave_central =  (int(nave_central_dict["posicion"][0] - jugador_x), int(nave_central_dict["posicion"][1]- jugador_y))
    
    if mascara_jugador.overlap(nave_central_dict["mask_nave"], offset_nave_central):
            vidas-=1
            ultimo_golpe = tiempo_actual
            
    
    return vidas, ultimo_golpe



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

