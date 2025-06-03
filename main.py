import pygame
import time
import constantes
import clases as cl

inicio= time.time()
pygame.init()

# Definicion de pantalla, título e ícono
modo_pantalla = True
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.LARGO_VENTANA))

pygame.display.set_caption("Plants vs. Zombies")
icono = pygame.image.load("assets//icon.png")
pygame.display.set_icon(icono)
background = pygame.image.load("assets//map.jpeg").convert()
background = pygame.transform.scale(background, (constantes.ANCHO_VENTANA, constantes.LARGO_VENTANA))

run= True


# Grilla de entidades y grilla de rects.
grilla_rects = [[pygame.Rect(constantes.grass_start_x + col * constantes.celda_ancho, constantes.grass_start_y + fil *constantes.celda_alto,constantes.celda_ancho, constantes.celda_alto) for col in range(9)] for fil in range(5)] #Grilla[fila][columna]
grilla_entidades = [[0 for x in range(9)] for y in range(5)]


while run:

    screen.blit(background, (0,0)) # Fondo

    cl.dibujar_grilla(screen, grilla_rects)#Esta funcion dibuja la grilla, comentar para que no se dibuje

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
        elif event.type== pygame.KEYDOWN:
            if event.key== pygame.K_ESCAPE:
                run= False
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
    pygame.display.update()

pygame.quit()
final= time.time()
print(f"Tiempo transcurrido: {final-inicio:.2f} segundos")
