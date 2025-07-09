# 🎮 RebelPixels

**RebelPixels** es un juego de disparos en 2D con estética retro y alma rebelde. Enfrentate a escuadrones enemigos, esquivá lluvias de proyectiles, y defendé la galaxia con pura habilidad y reflejos. Diseñado con amor, código modular y una obsesión por la jugabilidad justa.

---

## 🚀 Características

- ✨ Estilo pixel art con ambientación espacial
- 🧠 IA enemiga con trayectorias dinámicas y formaciones personalizadas
- 🎯 Sistema de colisiones preciso con máscaras y offsets
- 🔫 Múltiples tipos de disparos y enemigos
- 🛠️ Arquitectura modular y escalable
- 🎵 Música y efectos de sonido integrados
- 🏆 Ranking de puntuaciones persistente
- ⏸️ Pausa, mute y controles intuitivos

---

## 🎮 Controles

| Tecla | Acción                        |
|------:|-------------------------------|
| `← →`     | Mover horizontalmente     |
| `↑ ↓`     | Mover verticalmente       |
| `ESPACIO` | Disparar                  |
| `P`       | Pausar el juego           |
| `M`       | Activar/desactivar sonido |
| `ESC`     | Volver al menú            |

---

## 🧩 Estructura del Proyecto
```markdown
RebelPixels
|-- README.md
|
|-- assets
|   |-- backgrounds
|   |   `-- Fondo menu.png
|   |-- music
|   |   |-- juego.mp3
|   |   `-- menu.mp3
|   |-- soundeffects
|   |   |-- click.wav
|   |   |-- explosion_enemigo.wav
|   |   `-- impacto_jugador.wav
|   `-- sprites
|       |-- bombardero.png
|       |-- carrier.png
|       |-- caza.png
|       |-- fondo.png
|       |-- fragata.png
|       |-- jugador.png
|       `-- nodriza.png
|-- main.py
|-- menu.py
|-- ranking.json
|-- ranking.py
|-- requirements.txt
`-- scripts
    |-- colisiones.py
    |-- disparos.py
    |-- enemigos.py
    |-- escenarios.py
    |-- funciones_comunes.py
    |-- jugador.py
    `-- sonido.py


## 🛠️ Requisitos

- Python 3.10 o superior
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

---

## ▶️ Cómo jugar

1. Cloná el repositorio o descargalo como ZIP.
2. Asegurate de tener instaladas las dependencias.

```bash
pip install -r requirements.txt

3. Ejecutá el menú:

```bash
python menu.py

---

## 📜 Créditos

Desarrollado por **Sebastián**, con pasión por el código limpio, la jugabilidad justa y los píxeles rebeldes.

---

## 🛸 ¿Por qué es el mejor juego de la historia?

Porque no solo dispara píxeles... dispara pasión, precisión y propósito.