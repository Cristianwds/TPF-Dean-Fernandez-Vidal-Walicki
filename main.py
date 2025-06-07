import pygame
from pygame import mixer
import time
import constantes
import random
from clases import *
from funciones import *

pygame.init()
reloj = pygame.time.Clock()
mixer.music.load("assets/Musica/[Day Stage].mp3")
mixer.music.play(-1)

# Definicion de pantalla
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

# Titulo e Ícono
pygame.display.set_caption("Plants vs. Zombies")
icono = pygame.image.load("assets//icon.png")
pygame.display.set_icon(icono)

# Fondo de pantalla del juego
background = pygame.image.load("assets//map.jpeg").convert()
background = pygame.transform.scale(
    background, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)
)

# Grilla de entidades y grilla de rects.
grilla_rects = [
    [
        pygame.Rect(
            constantes.COMIENZO_PASTO_X + col * constantes.CELDA_ANCHO,
            constantes.COMIENZO_PASTO_Y + fil * constantes.CELDA_ALTO,
            constantes.CELDA_ANCHO,
            constantes.CELDA_ALTO,
        )
        for col in range(9)
    ]
    for fil in range(5)
]  # Grilla[fila][columna]
grilla_entidades = [[0 for x in range(9)] for y in range(5)]
fila, columna = 0, 0  # indices para moverse por la matriz
cuad = pygame.image.load("assets\\cuadrado.png")
cuadpos = [constantes.COMIENZO_PASTO_X, constantes.COMIENZO_PASTO_Y]

# Lista posiciones
pos_zombie = [165, 255, 345, 435, 525]

# Evento aparicion de zombies
APARICION_ZOMBIE = pygame.USEREVENT
pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)

#  x, y, imagen, vida, velocidad
run = True
while run:

    screen.blit(background, (0, 0))  # Fondo
    screen.blit(cuad, cuadpos)
    # dibujar_grilla(screen, grilla_rects)#Esta funcion dibuja la grilla, comentar para que no se dibuje

    grupo_plantas.update()
    grupo_plantas.draw(screen)
    grupo_proyectiles.update()
    grupo_proyectiles.draw(screen)

    xmin = 322
    ymin = 120
    ymax = ymin + (90 * 4)
    xmax = xmin + (78 * 8)
    if cuadpos[0] <= xmin:
        cuadpos[0], columna = xmin, 0
    if cuadpos[1] <= ymin:
        cuadpos[1], fila = ymin, 0
    if cuadpos[0] >= xmax:
        cuadpos[0], columna = xmax, 8
    if cuadpos[1] >= ymax:
        cuadpos[1], fila = ymax, 4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_a:
                cuadpos[0] -= 78
                columna -= 1
            elif event.key == pygame.K_d:
                cuadpos[0] += 78
                columna += 1
            elif event.key == pygame.K_w:
                cuadpos[1] -= 90
                fila -= 1
            elif event.key == pygame.K_s:
                cuadpos[1] += 90
                fila += 1
            elif event.key == pygame.K_e:
                if grilla_entidades[fila][columna] == 0:
                    nueva_planta = lanzaguisantes(cuadpos[0] - 15, cuadpos[1] + 20)
                    grilla_entidades[fila][columna] = nueva_planta
                    grupo_plantas.add(nueva_planta)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            #Poner plantas con el click
            if (constantes.COMIENZO_PASTO_X < x < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y < constantes.FIN_PASTO_Y):
                x = (x - constantes.COMIENZO_PASTO_X) // constantes.CELDA_ANCHO #Devuelve el nro de casilla en x
                y = (y - constantes.COMIENZO_PASTO_Y) // constantes.CELDA_ALTO #Devuelve el nro de casilla en y
                if grilla_entidades[y][x] == 0:
                    nueva_planta = lanzaguisantes((x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,(y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20) #En la pos de la planta se pasa de numero de grilla a pixeles.
                    grilla_entidades[y][x] = nueva_planta
                    grupo_plantas.add(nueva_planta)

        # Cada cierto tiempo spawnean zombies
        elif event.type == APARICION_ZOMBIE:
            pos_aleatoria = random.randint(0, 4)
            ubicacion_frames= [f"assets\\zombies\\cono\\caminata\\frame_{i}.png" for i in range(1, 60)]
            frame_actual= [pygame.image.load(frame).convert_alpha() for frame in ubicacion_frames]
            nuevo_zombie = Enemigos(
                constantes.ANCHO_VENTANA,
                pos_zombie[pos_aleatoria],
                frame_actual,
                181,
                constantes.VELOCIDAD_ZOMBIE,
            )
            nuevo_zombie.add(grupo_zombies)

    grupo_zombies.update()
    grupo_zombies.draw(screen)

    pygame.display.update()
    reloj.tick(60)

pygame.quit()
