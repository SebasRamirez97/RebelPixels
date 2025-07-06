import pygame

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

def generar_diccionario(nave,mascara_nave,posicion_nave):
    diccionario_nave = {
            "posicion": posicion_nave,
            "sprite_nave": nave,
            "mask_nave": mascara_nave
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


