import pygame

sonido_danio = None
sonido_explosion = None
sonido_disparo = None

def cargar_sonidos():
    global sonido_danio, sonido_explosion, sonido_disparo
    sonido_danio = pygame.mixer.Sound("assets/soundeffects/impacto_jugador.wav")
    sonido_explosion = pygame.mixer.Sound("assets/soundeffects/explosion_enemigo.wav")
    

    sonido_danio.set_volume(0.6)
    sonido_explosion.set_volume(0.7)

def reproducir_danio():
    if sonido_danio:
        sonido_danio.play()

def reproducir_explosion():
    if sonido_explosion:
        sonido_explosion.play()

def iniciar_musica():
    pygame.mixer.music.load("assets/music/arcade.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)