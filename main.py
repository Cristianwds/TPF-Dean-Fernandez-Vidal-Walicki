import pygame
import time
import constantes

inicio= time.time()
pygame.init()

# Definicion de pantalla, título e ícono
modo_pantalla = True
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.LARGO_VENTANA))

pygame.display.set_caption("Plants vs. Zombies")
icono = pygame.image.load("assets//icon.png")
pygame.display.set_icon(icono)
background = pygame.image.load("assets//map.jpeg").convert()
background = pygame.transform.scale(background, (1040,650))

run= True

while run:

    screen.blit(background, (0,0)) # Fondo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
        if event.type== pygame.KEYDOWN:
            if event.key== pygame.K_ESCAPE:
                run= False
    pygame.display.update()

pygame.quit()
final= time.time()
print(f"Tiempo transcurrido: {final-inicio:.2f} segundos")
