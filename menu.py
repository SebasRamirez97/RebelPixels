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
    ventana.fill(negro) 
    for boton in botones:
        pygame.draw.rect(ventana, rojo, boton["rect"]) #dibuja un rect a cada boton
        texto = fuente.render(boton["texto"], True, negro) #renderiza el text del boton en blanco
        texto_rect = texto.get_rect(center=boton["rect"].center) #obtiene la posicion del centro del rect
        ventana.blit(texto, texto_rect) # Dibuja el texto en la pantalla
    pygame.display.update() #actualiza la pantalla
    
    
def mostrar_ranking_en_menu(ventana, fuente):
    datos = mostrar_ranking("ranking.json")

    ventana.fill((0, 0, 0))
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
    
    

while corriendo:
    dib_menu() #llama a la funcion

    for evento in pygame.event.get():
        if evento.type == pygame.quit:
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
                            print("Mostrando los créditos...")
                            # Acá podemos llamar a la función de créditos
                        elif boton["texto"] == "Salir":
                            corriendo = False

pygame.quit() # Se cierra correctamente PyGame liberando los recursos usados.
        



