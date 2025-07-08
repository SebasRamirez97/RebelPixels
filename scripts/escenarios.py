from scripts.enemigos import entrada_varios_escuadrones as entrada_escuadrones
from scripts.enemigos import batalla_varios_escuadrones as batalla_escuadrones
from scripts.enemigos import entrada_poligonica 
from scripts.enemigos import batalla_poligomica
from .enemigos import entrada_varios_escuadrones as entrada_escuadrones
from .enemigos import batalla_varios_escuadrones as batalla_escuadrones
from .enemigos import entrada_poligonica 
from .enemigos import batalla_poligomica
from .enemigos import entrada_carrier
from .enemigos import batalla_carrier
from .enemigos import crear_formacion_v
def escenario_1(cantidad,nave,mask_nave,pos_inicial,pos_final,distancia_naves,distancia_squad,ventana,
                velocidad_x,jugador_x,jugador_y,jugador_mask,proyectiles_jugador,puntaje_jugador,escuadrones_posiciones,fase,disparos,vuelta,contador_enemigos):
    disparos_nuevos = []
    if fase == "entrada":

        situacion = entrada_escuadrones(cantidad, nave, mask_nave, pos_inicial,pos_final, distancia_naves, distancia_squad,ventana,vuelta)
        fase = situacion["fase"]
        escuadrones_posiciones = situacion["lista_escuadrones"]
    elif fase == "batalla":
        
        nuevos_escuadrones = batalla_escuadrones(escuadrones_posiciones,velocidad_x,jugador_x,jugador_y,jugador_mask,proyectiles_jugador,puntaje_jugador,ventana,disparos,contador_enemigos)
        
        escuadrones_posiciones, disparos_nuevos ,puntaje_jugador,contador_enemigos= nuevos_escuadrones


    return escuadrones_posiciones , fase, disparos_nuevos, puntaje_jugador,contador_enemigos

def escenario_2(fase, nave_central_dict,disparos_central, vertices_estado,
                nave_central_sprite, escala, mask_nave_central, nave_central_pos_inicial,
                nave_central_pos_final, nave_vertice_sprite, mask_nave_vertice, cantidad,
                distancia, rotacion, velocidad_x, velocidad_y,
                jugador_x, jugador_y, jugador_mask,disparos_jugador,puntaje_jugador, ventana,vuelta,contador_enemigos,vertices_vivos):
    
    nuevos_disparos_central= []

    if fase == "entrada":
        situacion = entrada_poligonica(
            nave_central_sprite, escala, mask_nave_central,
            nave_central_pos_inicial, nave_central_pos_final,
            nave_vertice_sprite, mask_nave_vertice,
            cantidad, distancia, rotacion, ventana,vuelta
        )
        fase = situacion["fase"]
        nave_central_dict = situacion["nave_central"]

        if fase == "batalla":
            vertices_estado = situacion["vertices"]

    elif fase == "batalla":
        nave_central_dict, vertices_estado, nuevos_disparos_central,puntaje_jugador,contador_enemigos,vertices_vivos= batalla_poligomica(
            nave_central_dict,disparos_central, vertices_estado, escala,
            nave_vertice_sprite, mask_nave_vertice,
            distancia, rotacion, velocidad_x, velocidad_y,
            jugador_x, jugador_y, jugador_mask,disparos_jugador,puntaje_jugador, ventana,contador_enemigos
        )

    return nave_central_dict["posicion"], fase, nave_central_dict, vertices_estado, nuevos_disparos_central ,puntaje_jugador,contador_enemigos,vertices_vivos

def escenario_3(fase, dict_carrier, carrier, carrier_mask, pos_inicial, pos_final,
                jugador_x, jugador_y, jugador_mask,disparos_jugador,puntaje_jugador,ventana, tick_actual,
                nave_tropa, nave_tropa_mask,cantidad, cooldown,disparos_enemigos, vuelta,contador_enemigos):
    
    nuevos_disparos = []
    if fase == "entrada":
        situacion = entrada_carrier(carrier, carrier_mask, pos_inicial, pos_final, ventana,vuelta)
        nueva_fase = situacion["fase"]
        dict_carrier = situacion["carrier"]

        # Si cambia a batalla, generar formación inicial
        if nueva_fase == "batalla":
            sprite = dict_carrier["sprite_nave"]
            x, y = dict_carrier["posicion"]
            centro = (x + sprite.get_width() // 4 + 3, y + sprite.get_height()// 4)

            formacion, destinos = crear_formacion_v(centro, cantidad, nave_tropa, nave_tropa_mask,vuelta)
            dict_carrier["lista_naves"] = formacion
            dict_carrier["formacion_destinos"] = destinos

        fase = nueva_fase

    elif fase == "batalla":
        dict_carrier, nuevos_disparos,puntaje_jugador,contador_enemigos = batalla_carrier(dict_carrier, tick_actual,
                                       nave_tropa, nave_tropa_mask, cooldown,disparos_enemigos,jugador_x,jugador_y,jugador_mask,
                                       disparos_jugador,puntaje_jugador,ventana,vuelta,contador_enemigos)

    return fase, dict_carrier, nuevos_disparos, puntaje_jugador, contador_enemigos
