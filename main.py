import pygame

pygame.init()

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ventana controlada")
cajita = pygame.surface((100,100))


corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Acá se refresca la pantalla en cada ciclo, no por cada evento
        ventana.fill((0, 0, 0))  # Fondo negro
    cajita.fill((255,0,0))
    pygame.display.update()
    
    

pygame.quit()

#es una prueba

print("Esto es una prueba")

print("Pureba 2- toma 2")