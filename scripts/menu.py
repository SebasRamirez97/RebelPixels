import pygame 
import sys

pygame.init()



#configuracion de la pantalla
ancho , alto = 800 , 600
ventana = pygame.display.set_mode((ancho , alto))
pygame.display.set_caption("menu pixel")

#color
gris = (200, 200, 200)
blanco = (255, 255, 255)

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
    ventana.fill(gris) #dib la pantalla de gris
    for boton in botones:
        pygame.draw.rect(ventana, blanco, boton["rect"]) #dibuja un rect a cada boton
        texto = fuente.render(boton["texto"], True, gris) #renderiza el text del boton en blanco
        texto_rect = texto.get_rect(center=boton["rect"].center) #obtiene la posicion del centro del rect
        ventana.blit(texto, texto_rect) # Dibuja el texto en la pantalla
    pygame.display.update() #actualiza la pantalla

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
                            # Acá podemos llamar a la función de juego
                        elif boton["texto"] == "Ranking":
                            print("Mostrando el ranking...")
                            # Acá podemos llamar a la función de ranking
                        elif boton["texto"] == "Créditos":
                            print("Mostrando los créditos...")
                            # Acá podemos llamar a la función de créditos
                        elif boton["texto"] == "Salir":
                            corriendo = False

pygame.quit() # Se cierra correctamente PyGame liberando los recursos usados.
        




    
    


