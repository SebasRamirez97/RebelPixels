import pygame 
import sys
from main import iniciar_juego
from ranking import mostrar_ranking

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("assets/music/menu.mp3") 
pygame.mixer.music.set_volume(0.5)  # Ajustá volumen
pygame.mixer.music.play(-1)  # Reproduce en loop infinito

sonido_click = pygame.mixer.Sound("assets/soundeffects/click.wav")
sonido_click.set_volume(0.10)

#configuracion de la pantalla
ancho , alto = 800 , 600
ventana = pygame.display.set_mode((ancho , alto))
pygame.display.set_caption("menu pixel")

#color
negro = (0, 0, 0)
rojo = (255, 0, 0)

#fuente
fuente = pygame.font.SysFont("Arial", 50)

#botones
botones = [
    {"texto": "Jugar", "rect": pygame.Rect(300, 150, 200, 60)},
    {"texto": "Ranking", "rect": pygame.Rect(300, 230, 200, 60)},
    {"texto": "Créditos", "rect": pygame.Rect(300, 310, 200, 60)},
    {"texto": "Salir", "rect": pygame.Rect(300, 390, 200, 60)}
]


corriendo = True

def dib_menu():
    fondo = pygame.image.load("assets/backgrounds/Fondo menu.png")
    #ventana.fill(negro)
    fondo = pygame.transform.scale(fondo, (800, 600)) 
    ventana.blit(fondo,(0,0))
    for boton in botones:
        pygame.draw.rect(ventana, (255,255,255), boton["rect"]) #dibuja un rect a cada boton
        texto = fuente.render(boton["texto"], True, negro) #renderiza el text del boton en blanco
        texto_rect = texto.get_rect(center=boton["rect"].center) #obtiene la posicion del centro del rect
        ventana.blit(texto, texto_rect) # Dibuja el texto en la pantalla
    
    pygame.display.update() #actualiza la pantalla
    
    
def mostrar_ranking_en_menu(ventana, fuente):
    datos = mostrar_ranking("ranking.json")

    ventana.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 30)
    titulo = fuente.render("🏆 RANKING", True, (255, 215, 0))
    ventana.blit(titulo, (280, 50))

    for i, (nombre, puntaje) in enumerate(datos[:5]):
        texto = fuente.render(f"{i+1}. {nombre}: {puntaje}", True, (255, 255, 255))
        ventana.blit(texto, (250, 120 + i * 50))

    mensaje = fuente.render("ESC para volver", True, (200, 200, 200))
    ventana.blit(mensaje, (230, 450))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                esperando = False    
    
def mostrar_creditos(ventana, fuente):
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                corriendo = False

        ventana.fill((0, 0, 0))
        fuente = pygame.font.SysFont(None, 30)
        titulo = fuente.render("🎬 CRÉDITOS", True, (255, 215, 0))
        linea1 = fuente.render("Programación: Bruno; Sebastian; Yamila.", True, (255, 255, 255))
        linea2 = fuente.render("Música y FX: Librería pixabay.com", True, (200, 200, 200))
        linea3 = fuente.render("Arte: Sprites personalizados y libres", True, (200, 200, 200))
        salir = fuente.render("Presioná ESC para volver", True, (150, 150, 150))

        ventana.blit(titulo, (250, 80))
        ventana.blit(linea1, (200, 150))
        ventana.blit(linea2, (200, 200))
        ventana.blit(linea3, (200, 250))
        ventana.blit(salir, (200, 400))

        pygame.display.flip()   
def ejecutar_menu():
    corriendo = True
    while corriendo:
        dib_menu() #llama a la funcion

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False #si se cierra la ventana se termna el bucle

            if evento.type == pygame.MOUSEBUTTONDOWN: # Si se presiona el mouse
                    pos = pygame.mouse.get_pos() # Obtiene la posición del mouse donde se hizo clic
                    print(pos)
                    for boton in botones:
                        if boton["rect"].collidepoint(pos): # Si el clic fue dentro del rectángulo del botón
                            print("Clic en:", boton["texto"])
                            if boton["texto"] == "Jugar":
                                print("Iniciando el juego...")
                                iniciar_juego()
                            elif boton["texto"] == "Ranking":
                                mostrar_ranking_en_menu(ventana, fuente)
                            elif boton["texto"] == "Créditos":
                                mostrar_creditos(ventana, fuente)
                            elif boton["texto"] == "Salir":
                                corriendo = False

    # Se cierra correctamente PyGame liberando los recursos usados.
if __name__ == "__main__":
    ejecutar_menu()
    pygame.quit()




