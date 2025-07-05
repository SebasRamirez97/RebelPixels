from scripts.enemigos import entrada_varios_escuadrones as entrada_escuadrones
from scripts.enemigos import batalla_varios_escuadrones as batalla_escuadrones
from scripts.enemigos import entrada_poligonica 
from scripts.enemigos import batalla_poligomica
from scripts.enemigos import inicializar_vertices_poligono as inicializar_vertices

def escenario_1(cantidad,nave,mask_nave,pos_inicial,pos_final,distancia_naves,distancia_squad,ventana,
                velocidad_x,jugador_x,jugador_y,jugador_mask,escuadrones_posiciones,fase,disparos):
    disparos_nuevos = []
    if fase == "entrada":

        situacion = entrada_escuadrones(cantidad, nave, mask_nave, pos_inicial,pos_final, distancia_naves, distancia_squad,ventana)
        fase = situacion["fase"]
        escuadrones_posiciones = situacion["escuadrones_posiciones"]
    elif fase == "batalla":
        
        nuevos_escuadrones = batalla_escuadrones(escuadrones_posiciones,velocidad_x,jugador_x,jugador_y,jugador_mask,ventana,disparos)
        
        escuadrones_posiciones, disparos_nuevos = nuevos_escuadrones


    return escuadrones_posiciones , fase, disparos_nuevos

def escenario_2(fase, nave_central_dict, vertices_estado,
                nave_central_sprite, escala, mask_nave_central, nave_central_pos_inicial,
                nave_central_pos_final, nave_vertice_sprite, mask_nave_vertice, cantidad,
                distancia, rotacion, velocidad_x, velocidad_y,
                jugador_x, jugador_y, jugador_mask, ventana):

    disparos_nuevos = []

    if fase == "entrada":
        situacion = entrada_poligonica(
            nave_central_sprite, escala, mask_nave_central,
            nave_central_pos_inicial, nave_central_pos_final,
            nave_vertice_sprite, mask_nave_vertice,
            cantidad, distancia, rotacion, ventana
        )
        fase = situacion["fase"]
        nave_central_dict = situacion["nave_central"]

        if fase == "batalla":
            vertices_estado = inicializar_vertices(cantidad)

    elif fase == "batalla":
        nave_central_dict, vertices_estado = batalla_poligomica(
            nave_central_dict, vertices_estado, escala,
            nave_vertice_sprite, mask_nave_vertice,
            distancia, rotacion, velocidad_x, velocidad_y,
            jugador_x, jugador_y, jugador_mask, ventana
        )

    return nave_central_dict["posicion"], fase, nave_central_dict, vertices_estado, disparos_nuevos

