import pygame
from ranking import cargar_ranking, guardar_ranking, actualizar_ranking, mostrar_ranking

def cargar_imagen(direccion, escala):
    imagen = pygame.image.load(direccion)
    imagen = pygame.transform.scale_by(imagen, escala)
    return imagen

def crear_mascara(superficie):
    mascara_superficie = pygame.mask.from_surface(superficie)

    return mascara_superficie


def mostrar_puntuacion(superficie, fuente, puntuacion, color=(255, 255, 255), posicion=(10, 20)):
    texto = fuente.render(f"Puntaje: {puntuacion}", True, color)
    superficie.blit(texto, posicion)
    

def enemigos_destruidos(superficie, fuente, cantidad, color=(255, 255, 255), posicion=(10, 50)):
    texto = fuente.render(f"Enemigos destruidos: {cantidad}", True, color)
    superficie.blit(texto, posicion)

def mostrar_vidas(ventana, font, vidas):
    texto = font.render(f"Vidas: {vidas}", True, (255, 0, 0))
    ventana.blit(texto, (10, 570))  

    
def mostrar_pantalla_pausa(superficie, fuente, mensaje="PAUSA - Presioná 'P' para continuar", 
                        color=(255, 255, 255), centro=(400, 300)):
    texto = fuente.render(mensaje, True, color)
    recto = texto.get_rect(center=centro)
    superficie.blit(texto, recto)
    pygame.display.flip()        

def generar_diccionario(nave, mascara_nave, posicion_nave):
    diccionario_nave = {
        "posicion": posicion_nave,
        "sprite_nave": nave,
        "mask_nave": mascara_nave,
        "vida": 100,
        "velocidad": 0,
        "destino": None,
        "estado": "destruido",
        #Para poligono
        "indice": 0,
        "kamikaze": 0,
        "ultimo_tick": 0,
        "rafaga": False,
        "disparos_rafaga": 0,
        #Para Carrier
        "lista_naves": [],
        "lista_destinos":[],
        "direccion": (0, 0)
    }
    return diccionario_nave

def mostrar_pantalla_gameover(ventana, font, score):
    ventana.fill((0, 0, 0))
    texto_gameover = font.render("¡GAME OVER!", True, (255, 0, 0))
    texto_score = font.render(f"Puntuación final: {score}", True, (200, 200, 0))
    texto_reintentar = font.render("Presioná ENTER para reiniciar o ESC para salir", True, (255, 255, 255))

    ventana.blit(texto_gameover, (ventana.get_width()//2 - texto_gameover.get_width()//2, 200))
    ventana.blit(texto_score, (ventana.get_width()//2 - texto_score.get_width()//2, 260))
    ventana.blit(texto_reintentar, (ventana.get_width()//2 - texto_reintentar.get_width()//2, 340))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def generar_diccionario(nave, mascara_nave, posicion_nave):
    diccionario_nave = {
        "posicion": posicion_nave,
        "sprite_nave": nave,
        "mask_nave": mascara_nave,
        "vida": 100,
        "lista_naves": [],
        "lista_destinos":[],
        "ultimo_tick": 0,
        "direccion": (0, 0),
        "velocidad": 0,
        "kamikaze": 0,
        "destino": None,
        "estado": "destruido"
    }
    return diccionario_nave

def pedir_nombre(ventana, font, max_caracteres=12):
    nombre = ""
    ingresando = True

    while ingresando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre.strip() != "":
                    ingresando = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < max_caracteres and event.unicode.isprintable():
                    nombre += event.unicode

        ventana.fill((0, 0, 0))
        texto = font.render("Ingrese su nombre: " + nombre + "_", True, (255, 255, 255))
        ventana.blit(texto, (100, 250))
        pygame.display.flip()

    return nombre.strip()

def procesar_gameover(ventana, font, puntaje_jugador):

    mostrar_pantalla_gameover(ventana, font, puntaje_jugador)
    pygame.display.flip()
    pygame.time.delay(1000)

    nombre = pedir_nombre(ventana, font)
    if not nombre:
        return False  

    actualizar_ranking("ranking.json", nombre, puntaje_jugador)
    top5 = mostrar_ranking("ranking.json")
    
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Nueva partida
                elif event.key == pygame.K_ESCAPE:
                    return False  # Salir

        
        ventana.fill((0, 0, 0))
        titulo = font.render("TOP 5 PUNTAJES", True, (255, 215, 0))
        ventana.blit(titulo, (250, 50))
        for i, (nombre_r, score_r) in enumerate(top5):
            texto = font.render(f"{i+1}. {nombre_r}: {score_r}", True, (255, 255, 255))
            ventana.blit(texto, (250, 100 + i * 40))

        mensaje = font.render("ENTER: Nueva partida | ESC: Salir", True, (200, 200, 200))
        ventana.blit(mensaje, (150, 400))

        pygame.display.flip()
        