import pygame
import math
def crear_disparo(tipo, x, y, objetivo_x=None, objetivo_y=None):
    match tipo:
        case "laser":
            return {
                "posicion": (x, y),
                "velocidad": 7,
                "color": (255, 0, 0),
                "ancho": 4,
                "alto": 10,
                "tipo": "laser"
                    }
        case "misil":
            if objetivo_x is not None and objetivo_y is not None:
                dx = objetivo_x - x
                dy = objetivo_y - y
                distancia = math.hypot(dx, dy)
                if distancia == 0:
                    direccion = (0, 1)
                else:
                    direccion = (dx / distancia, dy / distancia)

                return {
                    "posicion": (x, y),
                    "direccion": direccion,
                    "velocidad": 3,
                    "color": (255, 165, 0),
                    "ancho": 2,
                    "alto": 16,
                    "tipo": "misil"
                }
    # Podés agregar más tipos acá
        case "triple":
            
            direccion_derecha = (math.cos(math.radians(45)), math.sin(math.radians(45)))
            direccion_izquierda =(math.cos(math.radians(135)), math.sin(math.radians(135)))
            dicionario_triple = [{
                "posicion": (x, y),
                "direccion": direccion_derecha,
                "velocidad": 5,
                "color": (255, 255, 255),
                "ancho": 4,
                "alto": 10,
                "tipo": "default"},
                {
                "posicion": (x, y),
                "direccion": direccion_izquierda,
                "velocidad": 5,
                "color": (255, 255, 255),
                "ancho": 4,
                "alto": 10,
                "tipo": "default"},
                {
                "posicion": (x, y),
                "velocidad": 5,
                "color": (255, 255, 255),
                "ancho": 4,
                "alto": 10,
                "tipo": "default"}
                ]
            return dicionario_triple
            
    
def actualizar_y_dibujar_disparos(lista_disparos, ventana):
    disparos_actualizados = []

    for disparo in lista_disparos:
        x, y = disparo["posicion"]

        if "direccion" in disparo:
            dx, dy = disparo["direccion"]
            x += dx * disparo["velocidad"]
            y += dy * disparo["velocidad"]
        else:
            y += disparo["velocidad"]

        nueva_pos = (x, y)

        pygame.draw.rect(
            ventana,
            disparo.get("color", (255, 0, 0)),
            (x, y, disparo.get("ancho", 4), disparo.get("alto", 10))
        )

        if 0 <= x <= ventana.get_width() and 0 <= y <= ventana.get_height():
            nuevo_disparo = disparo.copy()
            nuevo_disparo["posicion"] = nueva_pos
            disparos_actualizados.append(nuevo_disparo)

    return disparos_actualizados