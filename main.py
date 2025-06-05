import pygame
import time
import constantes
import random
from clases import *
from funciones import *

inicio= time.time()
pygame.init()

# Definicion de pantalla
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.LARGO_VENTANA))

# Titulo e Ícono
pygame.display.set_caption("Plants vs. Zombies")
icono = pygame.image.load("assets//icon.png")
pygame.display.set_icon(icono)

# Fondo de pantalla del juego
background = pygame.image.load("assets//map.jpeg").convert()
background = pygame.transform.scale(background, (constantes.ANCHO_VENTANA, constantes.LARGO_VENTANA))

# Grilla de entidades y grilla de rects.
grilla_rects = [[pygame.Rect(constantes.grass_start_x + col * constantes.celda_ancho, constantes.grass_start_y + fil *constantes.celda_alto,constantes.celda_ancho, constantes.celda_alto) for col in range(9)] for fil in range(5)] #Grilla[fila][columna]
grilla_entidades = [[0 for x in range(9)] for y in range(5)]
fila, columna = 0, 0  # indices para moverse por la matriz
cuad = pygame.image.load("assets\\cuadrado.png")
cuadpos = [constantes.grass_start_x, constantes.grass_start_y]

# Lista posiciones
pos_zombie= [165, 255, 345, 435, 525]

# Evento aparicion de zombies
APARICION_ZOMBIE= pygame.USEREVENT
pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)

#  x, y, imagen, vida, velocidad
run= True
while run:

    screen.blit(background, (0,0)) # Fondo
    screen.blit(cuad, cuadpos)
    dibujar_grilla(screen, grilla_rects)#Esta funcion dibuja la grilla, comentar para que no se dibuje

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
        elif event.type== pygame.KEYDOWN:
            if event.key== pygame.K_ESCAPE:
                run= False
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            celdaclick = None
            for f in range(5):
                for c in range(9):
                    if grilla_rects[f][c].collidepoint(x,y):
                        celdaclick = (f,c)
                        break
                if celdaclick:
                    break
            if celdaclick:
                pass # Aca es donde se ponen los ifs para poner la planta seleccionada.
        
        #Cada cierto tiempo spawnean zombies
        elif event.type == APARICION_ZOMBIE:
            pos_aleatoria= random.randint(0, 4)
            nuevo_zombie= Enemigos(constantes.ANCHO_VENTANA, pos_zombie[pos_aleatoria], "assets//img_zombie.png", 40, 0.04)
            nuevo_zombie.add(grupo_zombies)

    grupo_zombies.update()
    grupo_zombies.draw(screen)
    pygame.display.update()

pygame.quit()
final= time.time()
print(f"Tiempo transcurrido: {final-inicio:.2f} segundos")
