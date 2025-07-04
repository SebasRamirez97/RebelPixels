from scripts.enemigos import entrada_varios_escuadrones as entrada_escuadrones
from scripts.enemigos import batalla_varios_escuadrones as batalla_escuadrones

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