import math
import random
import pygame

from .funciones_comunes import cargar_imagen as carga
from .funciones_comunes import crear_mascara as mascara
from .funciones_comunes import generar_diccionario as diccionario
from .colisiones import detectar_colisiones
from .disparos import crear_disparo
from scripts import sonido

def imagenes_enemigos():
    caza = carga("assets/sprites/caza.png" , 0.07)
    bombardero = carga("assets/sprites/bombardero.png" , 0.07)
    fragata = carga("assets/sprites/fragata.png" , 0.12)
    carrier = carga("assets/sprites/carrier.png" , 0.15)
    nodriza = carga("assets/sprites/nodriza.png" , 0.12)
    return [caza, bombardero, fragata, carrier, nodriza]

def crear_conjunto_mascaras(lista_superficies):
    lista_mascaras = []
    for superficie in lista_superficies:
        mask = mascara(superficie)
        lista_mascaras.append(mask)

    return lista_mascaras

def modificador_cordenada(pos_inicial,x,y):
    a = pos_inicial[0] + x
    b = pos_inicial[1] + y

    return (a,b)

def escuadron(nave,mask_nave,pos_lider, distancia,vuelta):
    
    lista_diccionarios_naves = []
    formacion = [
    pos_lider,
    modificador_cordenada(pos_lider,distancia *-1, distancia *-1),
    modificador_cordenada(pos_lider,distancia, distancia *-1),
    modificador_cordenada(pos_lider,distancia *2, distancia *-2)]

    for posicion in formacion:
        diccionario_nave = diccionario(nave,mask_nave,posicion)
        diccionario_nave["estado"] = "activo"
        diccionario_nave["vida"] = 100* vuelta
        diccionario_nave["puntaje"] = 100* vuelta
        lista_diccionarios_naves.append(diccionario_nave)
        
    return lista_diccionarios_naves
            
def varios_escuadrones(cantidad,nave,mask_nave,pos_lider,distancia_naves,distancia_esquad,vuelta):
    lista_escuadrones = []
    for i in range(cantidad):
        base = (pos_lider[0]+i*distancia_esquad,pos_lider[1])
        escuadron_pos = escuadron(nave,mask_nave,base,distancia_naves,vuelta)
        lista_escuadrones.append(escuadron_pos)

    return lista_escuadrones

def entrada_varios_escuadrones(cantidad,nave,mask_nave,pos_inicial,pos_final,distancia_naves,distancia_squad,ventana,vuelta):
    
    fase = "entrada"
    escuadrones_posiciones = varios_escuadrones(cantidad,nave,mask_nave, pos_inicial, distancia_naves, distancia_squad,vuelta)

    for escuadron in escuadrones_posiciones:
        for nave_enemiga in escuadron:
            ventana.blit(nave_enemiga["sprite_nave"], nave_enemiga["posicion"])

    if pos_inicial[1] >= pos_final[1]:
        fase = "batalla"
        escuadrones_posiciones = varios_escuadrones(cantidad, nave, mask_nave, pos_final, distancia_naves, distancia_squad,vuelta)
    
    diccionario_situacion = {
        "fase" : fase,
        "lista_escuadrones" : escuadrones_posiciones
    }
    return diccionario_situacion

def batalla_varios_escuadrones(lista_escuadrones,velocidad_x,jugador_x,jugador_y,jugador_mask,disparos_jugador,puntaje_jugador,ventana,disparos_enemigos,contador_enemigos):
    nuevos_escuadrones = []
    for escuadron in lista_escuadrones:
        escuadron_vivo = []
        for nave in escuadron:

            nave["posicion"] = (nave["posicion"][0] + velocidad_x, nave["posicion"][1])
            
            if random.randint(1, 180) == 1:  # 1 en 180 chance
                
                disparo1 = crear_disparo("laser", nave["posicion"][0] + 14, nave["posicion"][1] + 50,jugador_x,jugador_y)
                disparo2 = crear_disparo("laser", nave["posicion"][0] + 46, nave["posicion"][1] + 50,jugador_x,jugador_y)
                
                disparos_enemigos.extend([disparo1, disparo2])
            for disparo in disparos_jugador[:]:
                if disparo["rect"].colliderect(pygame.Rect(nave["posicion"][0], nave["posicion"][1], 60, 60)):
                    nave["vida"] -= 5
                    disparos_jugador.remove(disparo)
                    break
                    
                
            offset = (int(nave["posicion"][0] - jugador_x), int(nave["posicion"][1] - jugador_y))

            if jugador_mask.overlap(nave["mask_nave"], offset):
                nave["vida"] -= 10

            if nave["vida"] <= 0:
                print("💥 Nave destruida")
                nave["estado"] = "destruido"
                puntaje_jugador += nave["puntaje"]
                contador_enemigos +=1
                sonido.reproducir_explosion()
            else:
                ventana.blit(nave["sprite_nave"], nave["posicion"])
                escuadron_vivo.append(nave)

        nuevos_escuadrones.append(escuadron_vivo)
    return nuevos_escuadrones , disparos_enemigos , puntaje_jugador,contador_enemigos

def formacion_poligonica(nave_central,escala,mask_nave_central, pos_nave_central, nave_vertice,mask_nave_vertice,cantidad,distancia,rotacion,vuelta):
    
    diccionario_nave_central = diccionario(nave_central,mask_nave_central,pos_nave_central)
    diccionario_nave_central["estado"] = "activo"
    diccionario_nave_central["vida"] = 200 * vuelta
    diccionario_nave_central["puntaje"] = 400
    diccionario_nave_central["rafaga"] = False
    lista_diccionarios_poligomica = [diccionario_nave_central]
    
    for i in range(cantidad):
        angulo = 2 * math.pi * i / cantidad + rotacion
        x = pos_nave_central[0]  + distancia * math.cos(angulo) + (1024 * escala)/4
        y = pos_nave_central[1]  + distancia * math.sin(angulo) + (1024 * escala)/4
        pos_nave_vertice = (x,y)
        diccionario_nave_vertice = diccionario(nave_vertice,mask_nave_vertice,pos_nave_vertice)
        diccionario_nave_vertice["estado"] = "activo"
        diccionario_nave_vertice["vida"] = 1 * vuelta
        diccionario_nave_vertice["puntaje"] = 200
        diccionario_nave_vertice["indice"] = i
        lista_diccionarios_poligomica.append(diccionario_nave_vertice)
    
    return lista_diccionarios_poligomica

def entrada_poligonica(nave_central, escala, mask_nave_central, pos_inicial_nave_central,
                       pos_final_nave_central, nave_vertice, mask_nave_vertice,
                       cantidad, distancia, rotacion, ventana,vuelta):
    
    fase = "entrada"
    posicion_central_poligonica = pos_inicial_nave_central

    naves_poligomicas = formacion_poligonica(
        nave_central, escala, mask_nave_central, posicion_central_poligonica,
        nave_vertice, mask_nave_vertice, cantidad, distancia, rotacion, vuelta
    )

    for nave in naves_poligomicas:
        ventana.blit(nave["sprite_nave"], nave["posicion"])

    if (pos_inicial_nave_central >= pos_final_nave_central):
        fase = "batalla"
        posicion_central_poligonica = pos_final_nave_central

    nave_central_dict = naves_poligomicas[0]
    vertices = naves_poligomicas[1:]
    diccionario_situacion = {
        "fase": fase,
        "nave_central": nave_central_dict,
        "vertices": vertices
        
    }
    return diccionario_situacion

def batalla_poligomica(nave_central_dict,disparos_central, vertices_estado, escala, nave_vertice_sprite, mask_nave_vertice,
                       distancia, rotacion, velocidad_x, velocidad_y,
                       jugador_x, jugador_y, jugador_mask,disparos_jugador,puntaje_jugador, ventana,contador_enemigos):
    
    # Mover nave central
    pos_central = nave_central_dict["posicion"]
    nueva_pos_central = (pos_central[0] + velocidad_x, pos_central[1] + velocidad_y)
    nave_central_dict["posicion"] = nueva_pos_central

    # Dibujar nave central
    if nave_central_dict["estado"] == "activo":
        ventana.blit(nave_central_dict["sprite_nave"], nave_central_dict["posicion"])

    # Dibujar vértices vivos
    for vertice in vertices_estado:
        if vertice["estado"]=="activo":
            i = vertice["indice"]
            angulo = 2 * math.pi * i / len(vertices_estado) + rotacion
            x = nave_central_dict["posicion"][0] + distancia * math.cos(angulo) + (1024 * escala) / 4
            y = nave_central_dict["posicion"][1] + distancia * math.sin(angulo) + (1024 * escala) / 4
            vertice["posicion"] = (x,y)
            pos = (x, y)
            offset = (int(pos[0] - jugador_x), int(pos[1] - jugador_y))

            for disparo in disparos_jugador[:]:
                if disparo["rect"].colliderect(pygame.Rect(vertice["posicion"][0], vertice["posicion"][1], 60, 60)):
                    vertice["vida"] -= 5
                    disparos_jugador.remove(disparo)
                    break
            
            if jugador_mask.overlap(mask_nave_vertice, offset):
                vertice["vida"] -=10
                
            if vertice["vida"] <= 0:
                vertice["estado"] = "destruido"
                puntaje_jugador += vertice["puntaje"]
                contador_enemigos +=1
                sonido.reproducir_explosion()
            else:
                ventana.blit(nave_vertice_sprite, pos)

    vertices_vivos = 0
    for vertice in vertices_estado:
        if vertice["estado"] == "activo":
            vertices_vivos += 1
    
    if nave_central_dict["estado"] == "activo" and vertices_vivos == 0 and velocidad_x == 5:
        tiempo_actual = pygame.time.get_ticks()

        if not nave_central_dict["rafaga"]:
            if tiempo_actual - nave_central_dict["ultimo_tick"] > 1500:  # cada 1.5 segundos
                nave_central_dict["rafaga"] = True
                nave_central_dict["disparos_rafaga"] = 0
                nave_central_dict["ultimo_tick"] = tiempo_actual

# Si hay una ráfaga activa, disparar 3 veces con intervalo
        if nave_central_dict["rafaga"]:
            if tiempo_actual - nave_central_dict["ultimo_tick"] > 200:  # intervalo entre disparos
                disparos_central.extend(crear_disparo("triple", nave_central_dict["posicion"][0] + 14, nave_central_dict["posicion"][1] + 50, jugador_x, jugador_y+60))
                disparos_central.extend(crear_disparo("triple", nave_central_dict["posicion"][0] + 46, nave_central_dict["posicion"][1] + 50, jugador_x, jugador_y+60))
                

                nave_central_dict["disparos_rafaga"] += 1
                nave_central_dict["ultimo_tick"] = tiempo_actual

            if nave_central_dict["disparos_rafaga"] >= 3:
                nave_central_dict["rafaga"] = False

        for disparo in disparos_jugador[:]:
            if disparo["rect"].colliderect(pygame.Rect(nave_central_dict["posicion"][0], nave_central_dict["posicion"][1], 125, 125)):
                nave_central_dict["vida"] -= 5
                disparos_jugador.remove(disparo)
                break
        offset_central = ( nave_central_dict["posicion"][0]- jugador_x), (nave_central_dict["posicion"][1] - jugador_y)    
        
        if jugador_mask.overlap(nave_central_dict["mask_nave"], offset_central):
            nave_central_dict["vida"] -= 5
        
        if nave_central_dict["vida"]<= 0:
            nave_central_dict["estado"] = "destruido"
            puntaje_jugador += nave_central_dict["puntaje"]
            contador_enemigos += 1
            sonido.reproducir_explosion()
        else:
            ventana.blit(nave_central_dict["sprite_nave"], nave_central_dict["posicion"])



    return nave_central_dict, vertices_estado, disparos_central, puntaje_jugador,contador_enemigos,vertices_vivos,nave_central_dict["estado"]

def trayectoria_cuadrada(posicion, direccion_actual, x_min, x_max, y_min, y_max):
    x, y = posicion
    velocidad_x = 0
    velocidad_y = 0

    if direccion_actual == "derecha":
        velocidad_x = 5
        velocidad_y = 0
        if x >= x_max:
            direccion_actual = "abajo"

    elif direccion_actual == "abajo":
        velocidad_x = 0
        velocidad_y = 5
        if y >= y_max:
            direccion_actual = "izquierda"

    elif direccion_actual == "izquierda":
        velocidad_x = -5
        velocidad_y = 0
        if x <= x_min:
            direccion_actual = "arriba"

    elif direccion_actual == "arriba":
        velocidad_x = 0
        velocidad_y = -5
        if y <= y_min:
            direccion_actual = "derecha"

    else:
        # Por si dirección_actual tiene un valor inesperado
        velocidad_x = 0
        velocidad_y = 0
        direccion_actual = "derecha"

    return velocidad_x, velocidad_y, direccion_actual

def entrada_carrier(carrier,mask_carrier,pos_inicial_carrier,pos_final_carrier,ventana):
    
    fase = "entrada"
    ventana.blit(carrier,pos_inicial_carrier)
    pos_actual = pos_inicial_carrier
    
    if pos_inicial_carrier[1] >= pos_final_carrier[1]:
        fase = "batalla"
        pos_actual = pos_final_carrier

    diccionario_carrier = diccionario(carrier,mask_carrier,pos_actual)
    diccionario_carrier["estado"] = "activo"
    diccionario_carrier["vida"] = 600*vuelta
    diccionario_carrier["puntaje"] = 700*vuelta
    
    diccionario_carrier_situacion = {
        "fase": fase,
        "carrier": diccionario_carrier
    }

    return diccionario_carrier_situacion

def desplegar_nave(pos_inicial, destino,nave,mask_nave,vuelta):
    
    diccionario_nave = diccionario(nave, mask_nave, pos_inicial)
    diccionario_nave["vida"] = 300*vuelta
    diccionario_nave["puntaje"] = 50*vuelta
    diccionario_nave["velocidad"] = 2
    diccionario_nave["destino"] = destino  # para saber cuándo detenerse
    diccionario_nave["estado"] = "activo"
    # Calcular dirección normalizada hacia el destino
    dx = destino[0] - pos_inicial[0]
    dy = destino[1] - pos_inicial[1]
    distancia = math.hypot(dx, dy)
    if distancia == 0:
        direccion = (0, 1)
        diccionario_nave["estado"] = "detenida"
    else:
        direccion = (dx / distancia, dy / distancia)

    diccionario_nave["direccion"] = direccion
    return diccionario_nave

def crear_formacion_v(centro_carrier, cantidad, nave, mask_nave):
    formacion = []
    destinos = []
    
    for i in range(cantidad):
        offset_x = (i - cantidad // 2) * 60
        offset_y = -abs(i - cantidad // 2) * 20
        destino = modificador_cordenada(centro_carrier, offset_x, offset_y+100)
        diccionario_nave = desplegar_nave(centro_carrier, destino, nave, mask_nave)
        formacion.append(diccionario_nave)
        destinos.append(destino)
    return formacion, destinos

def batalla_carrier(diccionario_carrier, tick_actual, nave_tropa, nave_tropa_mask, cooldown,disparos_enemigos,jugador_x,jugador_y,jugador_mask,disparos_jugador,puntaje_jugador,ventana,vuelta,contador_enemigos):
    # Dibujar el carrier
    sprite_carrier = diccionario_carrier["sprite_nave"]
    x_carrier, y_carrier = diccionario_carrier["posicion"]

    for disparo in disparos_jugador[:]:
            if disparo["rect"].colliderect(pygame.Rect(x_carrier, y_carrier, 160, 160)):
                diccionario_carrier["vida"] -= 5
                disparos_jugador.remove(disparo)
                break
     
    offset_carrier = (int(x - jugador_x), int(y - jugador_y))

    if jugador_mask.overlap(nave["mask_nave"], offset_nave):
        diccionario_carrier["vida"] -=10
    
    if diccionario_carrier["vida"] == 0:
        diccionario_carrier["estado"] = "destruido"
        puntaje_jugador += diccionadio_carrier["puntaje"]
        contador_enemigos += 1
        sonido.reproducir_explosion()
    else:
        ventana.blit(sprite_carrier, (x_carrier, y_carrier))

    # Verificar qué cazas siguen activas
    naves_activas = []
    destinos_ocupados = []

    for nave in diccionario_carrier["lista_naves"]:
        if nave["estado"] in ("activo", "detenida"):
            naves_activas.append(nave)
            destinos_ocupados.append(nave["destino"])

    diccionario_carrier["lista_naves"] = naves_activas

    # Detectar destinos libres
    destinos_disponibles = []
    for destino in diccionario_carrier["formacion_destinos"]:
        if destino not in destinos_ocupados:
            destinos_disponibles.append(destino)

    # Reponer si hay espacio y pasó el cooldown
    if destinos_disponibles and tick_actual - diccionario_carrier["ultimo_tick"] >= cooldown and carrier["estado"] == "activo":
        destino = destinos_disponibles[0]
        centro = (x_carrier + sprite_carrier.get_width() // 4 + 3, y_carrier + sprite_carrier.get_height()//4)
        nueva_nave = desplegar_nave(centro, destino, nave_tropa, nave_tropa_mask,vuelta)
        diccionario_carrier["lista_naves"].append(nueva_nave)
        diccionario_carrier["ultimo_tick"] = tick_actual

    # Mover y dibujar las cazas activas
    for nave in diccionario_carrier["lista_naves"]:
        if nave["estado"] == "activo":
            dx, dy = nave["direccion"]
            nueva_pos = modificador_cordenada(nave["posicion"], dx * nave["velocidad"], dy * nave["velocidad"])
            nave["posicion"] = nueva_pos

            # Verificar si llegó al destino (con tolerancia)
            px, py = nueva_pos
            destino_x, destino_y = nave["destino"]
            distancia = math.hypot(destino_x - px, destino_y - py)

            if distancia < 1.0:
                nave["posicion"] = (destino_x, destino_y)
                nave["direccion"] = (0, 0)
                nave["estado"] = "detenida"

        ventana.blit(nave["sprite_nave"], nave["posicion"])
    #disparos y colisiones
    
    for nave in diccionario_carrier["lista_naves"]:
        if random.randint(1, 100) == 1 and nave["estado"] == "detenida":  # 1 en 180 chance
            disparo1 = crear_disparo("misil", nave["posicion"][0] + 14, nave["posicion"][1] + 50,jugador_x,jugador_y)
            disparo2 = crear_disparo("misil", nave["posicion"][0] + 46, nave["posicion"][1] + 50,jugador_x,jugador_y)
                
            disparos_enemigos.extend([disparo1, disparo2])

        for disparo in disparos_jugador[:]:
            if disparo["rect"].colliderect(pygame.Rect(nave["posicion"][0], nave["posicion"][1], 60, 60)):
                nave["vida"] -= 5
                disparos_jugador.remove(disparo)
                break
                
        offset_nave = (int(nave["posicion"][0] - jugador_x), int(nave["posicion"][1] - jugador_y))

        if jugador_mask.overlap(nave["mask_nave"], offset_nave):
            nave["vida"] -=10
        if nave["vida" == 0:
            print("💥 Nave destruida")
            nave["estado"] = "destruida"
            puntaje_jugador += nave["puntaje"]
            contador_enemigos += 1
            sonido.reproducir_explosion()
            # Acá podrías agregar explosión o sonido
    
            
    return diccionario_carrier, disparos_enemigos, puntaje_jugador, contador_enemigos
