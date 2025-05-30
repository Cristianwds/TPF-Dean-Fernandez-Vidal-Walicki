import pygame
import time
import variables

inicio= time.time()
pygame.init()
print("Hola mundo")

#screen_info= pygame.display.get_desktop_sizes()
#print(screen_info)
modo_pantalla= True
screen= pygame.display.set_mode((variables.ANCHO_VENTANA, variables.LARGO_VENTANA))
pygame.display.set_caption("assets//Plants vs. Zombies")
icono= pygame.image.load("buenicono.png")
pygame.display.set_icon(icono)

run= True

while run:
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
