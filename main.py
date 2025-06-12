import pygame
from pygame import mixer
import constantes
import random
from clases import *
from funciones import *

pygame.init()

reloj = pygame.time.Clock()
mixer.music.load(r"assets/Musica/[Day Stage].mp3")
mixer.music.play(-1)

# Definicion de pantalla
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

# Titulo e Ícono
pygame.display.set_caption("Plants vs. Zombies")
icono = pygame.image.load(r"assets//icon.png")
pygame.display.set_icon(icono)

# Interfaz del juego

fondo_interfaz = pygame.image.load(r'assets\interfaz.play.png')
fondo_interfaz = pygame.transform.scale(fondo_interfaz, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

boton_jugar = pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 210, 300, 100)
boton_salir = pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 85, 300, 110)

# Botones para chequear (PLAY Y EXIT)

# font_inicio = pygame.font.SysFont('arial',30 )
# font_titulo = pygame.font.SysFont('arial', 75)
# texto_boton_jugar = font_inicio.render('', True, (0,0,0))
# texto_boton_salir = font_inicio.render('', True, (255,255,255))

def dibujar_texto(texto, fuente, color, x, y):
    superficie_texto = fuente.render(texto, True, color)
    screen.blit(superficie_texto, (x, y))

def pantalla_inicio():
    screen.blit(fondo_interfaz, (0,0))
    #dibujar_texto(' Plantas vs zombies', font_titulo, (255,255,255), constantes.ANCHO_VENTANA / 2 - 280 , constantes.ALTO_VENTANA / 2 - 200)
    #pygame.draw.rect(screen, (0,0,0,0), boton_jugar)
    #pygame.draw.rect(screen, (0,0,0,0), boton_salir)
    #screen.blit(texto_boton_jugar, (boton_jugar.x + 190, boton_jugar.y -120))
    #screen.blit(texto_boton_salir, (boton_salir.x + 200, boton_salir.y - 90))
    pygame.display.update()


# Fondo de pantalla del juego
background = pygame.image.load(r"assets//map.jpeg").convert()
background = pygame.transform.scale(
    background, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)
)
barra = pygame.image.load(r"assets/barra.png")
barra = pygame.transform.scale(barra, (540,100))

perdiste = pygame.image.load(r"assets/ZombiesWon.png")
perdiste = pygame.transform.scale(perdiste, (925,770))

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


cuad = pygame.Surface((80, 90), pygame.SRCALPHA)
cuad.fill((255, 255, 255, 128))
cuadpos = [constantes.COMIENZO_PASTO_X, constantes.COMIENZO_PASTO_Y]

# Lista posiciones
pos_zombie = [165, 255, 345, 435, 525]

# Evento aparicion de zombies
APARICION_ZOMBIE = pygame.USEREVENT
pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)

# Defino semillas
s_girasol = Semillas(380, 10, r"assets\semillas\semillas_girasol.png", "girasol")
s_lanzaguisantes = Semillas(440, 10, r"assets//semillas//semillas_lanzaguisantes.png", "lanzaguisantes")
s_nuez = Semillas(500, 10, r"assets//semillas//semillas_nuez.png", "nuez")
s_lanzaguisantes.add(grupo_semillas)
s_girasol.add(grupo_semillas)
s_nuez.add(grupo_semillas)
# Defino las cortapastos
cortapastos_col = []
cortapastos_col += [
    [
        Cortapasto(
            constantes.COMIENZO_PASTO_X - constantes.CELDA_ANCHO - 20,
            constantes.COMIENZO_PASTO_Y + constantes.CELDA_ALTO * fil,
            cortapastos_col,
        )
    ]
    for fil in range(5)
]
for cortapasto_id in cortapastos_col:
    grupo_cortapastos.add(cortapasto_id)

seleccion_planta = False
#  x, y, imagen, vida, velocidad
run = True
mostrar_inicio = True 
while run:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio  = False
                if boton_salir.collidepoint(event.pos):
                    run = False 
    else:
        # reloj.tick(constantes.FPS)
        # screen.fill(constantes.COLOR_BG) #VAMOS A LLNAR EL FONDO CON EL COLOR BG

        # Dibujar fondo con imagen de grilla
        # screen.blit(background, (0,0))

        screen.blit(background, (0, 0))  # Fondo
        if seleccion_planta != False:
            screen.blit(cuad, cuadpos)
        # dibujar_grilla(screen, grilla_rects) #Esta funcion dibuja la grilla, comentar para que no se dibuje

        grupo_plantas.update()
        grupo_plantas.draw(screen)
        grupo_proyectiles.update()
        grupo_proyectiles.draw(screen)
        screen.blit(barra, (300, 0))
        grupo_semillas.draw(screen)
        grupo_cortapastos.draw(screen)
        grupo_cortapastos.update()

        if cuadpos[0] <= constantes.COMIENZO_PASTO_X:
            cuadpos[0], columna = constantes.COMIENZO_PASTO_X, 0
        if cuadpos[1] <= constantes.COMIENZO_PASTO_Y:
            cuadpos[1], fila = constantes.COMIENZO_PASTO_Y, 0
        if cuadpos[0] >= constantes.XMAX:
            cuadpos[0], columna = constantes.XMAX, 8
        if cuadpos[1] >= constantes.YMAX:
            cuadpos[1], fila = constantes.YMAX, 4

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
                        if seleccion_planta != False:
                            nueva_planta = lanzaguisantes(cuadpos[0] - 15, cuadpos[1] + 20)
                            grilla_entidades[fila][columna] = nueva_planta
                            grupo_plantas.add(nueva_planta)
                elif event.key == pygame.K_1:
                    seleccion_planta = "lanzaguisantes"
                elif event.key == pygame.K_2:
                    seleccion_planta = "girasol"
                elif event.key == pygame.K_3:
                    seleccion_planta = "nuez"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Poner plantas con el click
                if (constantes.COMIENZO_PASTO_X < x < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y < constantes.FIN_PASTO_Y):
                    x = (x - constantes.COMIENZO_PASTO_X) // constantes.CELDA_ANCHO #Devuelve el nro de casilla en x
                    cuadpos[0] = constantes.COMIENZO_PASTO_X + (x * constantes.CELDA_ANCHO)
                    y = (y - constantes.COMIENZO_PASTO_Y) // constantes.CELDA_ALTO #Devuelve el nro de casilla en y
                    cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y * constantes.CELDA_ALTO)
                    if grilla_entidades[y][x] == 0:
                        if seleccion_planta != False:
                            if seleccion_planta == "lanzaguisantes":
                                nueva_planta = lanzaguisantes((x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,(y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20, grilla_entidades) #En la pos de la planta se pasa de numero de grilla a pixeles.
                            elif seleccion_planta == "girasol":
                                nueva_planta = Girasol((x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, grilla_entidades)
                            elif seleccion_planta == "nuez":
                                nueva_planta = Nuez((x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, grilla_entidades)
                            seleccion_planta = False
                            grilla_entidades[y][x] = nueva_planta
                            grupo_plantas.add(nueva_planta)
                            pygame.mixer.Sound(
                                r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_plantar.ogg"
                            ).play()
                else: #Este else puede cambiarse por un elif con las dimensiones del rectangulo donde estan las semillas x ejemplo.
                    grupo_semillas.update(event)
                    for semillas in grupo_semillas:
                        if semillas.clicked:
                            seleccion_planta = semillas.item

            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if (constantes.COMIENZO_PASTO_X < x < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y < constantes.FIN_PASTO_Y):
                    x = (x - constantes.COMIENZO_PASTO_X) // constantes.CELDA_ANCHO #Devuelve el nro de casilla en x
                    cuadpos[0] = constantes.COMIENZO_PASTO_X + (x * constantes.CELDA_ANCHO)
                    y = (y - constantes.COMIENZO_PASTO_Y) // constantes.CELDA_ALTO #Devuelve el nro de casilla en y
                    cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y * constantes.CELDA_ALTO)

            # Cada cierto tiempo spawnean zombies
            elif event.type == APARICION_ZOMBIE:
                pos_aleatoria = random.randint(0, 4)
                tipo= random.choice(constantes.TIPOS_ZOMBIES)
                nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, pos_zombie[pos_aleatoria], tipo, constantes.VIDA_ZOMBIES[tipo])
                nuevo_zombie.add(grupo_zombies)

        grupo_zombies.update()
        grupo_zombies.draw(screen)

        for zombie in grupo_zombies:
            if zombie.hitbox.x <= 260:
                screen.blit(perdiste, (100,25))

        pygame.display.update()
    reloj.tick(60)

pygame.quit()
