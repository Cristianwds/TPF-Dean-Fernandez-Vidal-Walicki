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
background = pygame.transform.scale(background, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
barra = pygame.image.load(r"assets/barra.png")
barra = pygame.transform.scale(barra, (constantes.LARGO_BARRA, constantes.ALTO_BARRA))

perdiste = pygame.image.load(r"assets/ZombiesWon.png")
perdiste = pygame.transform.scale(perdiste, (925,770))

# Grilla de entidades y grilla de rects.
grilla_rects = [[pygame.Rect(constantes.COMIENZO_PASTO_X + col * constantes.CELDA_ANCHO,constantes.COMIENZO_PASTO_Y + fil * constantes.CELDA_ALTO,constantes.CELDA_ANCHO,constantes.CELDA_ALTO,)for col in range(9)]for fil in range(5)]  # Grilla[fila][columna]
grilla_entidades = [[0 for x in range(9)] for y in range(5)]
fila, columna = 0, 0  # indices para moverse por la matriz


cuad = pygame.Surface((80, 90), pygame.SRCALPHA)
cuad.fill((255, 255, 255, 128))
cuadpos = [constantes.COMIENZO_PASTO_X, constantes.COMIENZO_PASTO_Y]

traslucido = 5
vivo = True
# Evento aparicion de zombies
APARICION_ZOMBIE = pygame.USEREVENT
pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)
nivel_dificultad = 0

APARICION_OLEADA = pygame.USEREVENT + 1

##Evento de aparicion de soles
#APARICION_SOLES = pygame.USEREVENT
#pygame.time.set_timer(APARICION_SOLES, constantes.TIEMPO_APARICION_SOL)

# Defino semillas
s_girasol = Semillas(380, 10, r"assets\semillas\semillas_girasol.png", "girasol")
s_lanzaguisantes = Semillas(440, 10, r"assets//semillas//semillas_lanzaguisantes.png", "lanzaguisantes")
s_nuez = Semillas(500, 10, r"assets//semillas//semillas_nuez.png", "nuez")
s_lanzaguisantes.add(grupo_semillas)
s_girasol.add(grupo_semillas)
s_nuez.add(grupo_semillas)
# Defino las cortapastos
cortapastos_col = []
cortapastos_col += [[Cortapasto(constantes.COMIENZO_PASTO_X - constantes.CELDA_ANCHO - 20,constantes.COMIENZO_PASTO_Y + constantes.CELDA_ALTO * fil,cortapastos_col,)]for fil in range(5)]
for cortapasto_id in cortapastos_col:
    grupo_cortapastos.add(cortapasto_id)


#defino la pala
pala = Pala()
grupo_pala.add(pala)

#Este diccionario es para las previews, se puede llegar a cambiar por una alternativa mejor.
preview_dict = {
    "lanzaguisantes": [pygame.image.load(r"assets\lanzaguisante\frame_0.png"),-15,-34],
    "girasol": [pygame.image.load(r"assets\girasol\frame_1.png"),-3,-12],
    "nuez": [pygame.image.load(r"assets\nuez\frame_0.png"),1,-5],
}
for values in preview_dict.values():
    values[0].set_alpha(128)


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
        # dibujar_grilla(screen, grilla_rects) #Esta funcion dibuja la grilla, comentar para que no se dibuje

        grupo_plantas.update()
        grupo_plantas.draw(screen)
        grupo_cortapastos.draw(screen)
        grupo_cortapastos.update()
        grupo_zombies.update()
        grupo_zombies.draw(screen)
        grupo_proyectiles.update()
        grupo_proyectiles.draw(screen)
        screen.blit(barra, (300, 0))
        grupo_semillas.draw(screen)
        grupo_pala.draw(screen)
        
# CAMBIAR ESTA PARTE PORQUE HAY UN ERROR DE QUE SE VA DE LA GRILLA"""""
        if cuadpos[0] <= constantes.COMIENZO_PASTO_X:
            cuadpos[0], columna = constantes.COMIENZO_PASTO_X, 0
        if cuadpos[1] <= constantes.COMIENZO_PASTO_Y:
            cuadpos[1], fila = constantes.COMIENZO_PASTO_Y, 0
        if cuadpos[0] >= constantes.XMAX:
            cuadpos[0], columna = constantes.XMAX, 8
        if cuadpos[1] >= constantes.YMAX:
            cuadpos[1], fila = constantes.YMAX, 4


# Esta parte del code muestra la planta previsualizada en la grilla, el rect de previsualización en la grilla y llama a la función para dibujar la pala.
        
        
        x, y = pygame.mouse.get_pos()
        if seleccion_planta == "pala":
            pala.dibujar_cursor(x, y, screen)
        if (constantes.COMIENZO_PASTO_X < x < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y < constantes.FIN_PASTO_Y):
            x,y = de_pixeles_a_grilla(x,y)
            cuadpos[0] = constantes.COMIENZO_PASTO_X + (x * constantes.CELDA_ANCHO)
            cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y * constantes.CELDA_ALTO)
            
            if seleccion_planta != False:
                if seleccion_planta != "pala" and not (isinstance(grilla_entidades[y][x], Plantas)):
                    screen.blit(preview_dict[seleccion_planta][0],(cuadpos[0] + preview_dict[seleccion_planta][1], cuadpos[1] + preview_dict[seleccion_planta][2]),)
                    screen.blit(cuad, cuadpos)
                elif seleccion_planta == "pala":
                    screen.blit(cuad, cuadpos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Poner plantas con el click
                if (constantes.COMIENZO_PASTO_X < x < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y < constantes.FIN_PASTO_Y):
                    x,y = de_pixeles_a_grilla(x,y)
                    cuadpos[0] = constantes.COMIENZO_PASTO_X + (x * constantes.CELDA_ANCHO)
                    cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y * constantes.CELDA_ALTO)
                    if grilla_entidades[y][x] == 0 and seleccion_planta != False and seleccion_planta != "pala":
                        seleccion_planta = plantar(grilla_entidades, seleccion_planta, x, y)
                    elif (seleccion_planta == "pala"):
                        seleccion_planta = excavar(grilla_entidades, x, y, seleccion_planta, pala)
                #Funcionamiento de la seleccion de semillas
                elif (370 < x < 841 and 10 < y < 100):
                    grupo_semillas.update(event)
                    for semillas in grupo_semillas:
                        if semillas.clicked:
                            seleccion_planta = semillas.item
                #Seleccion de pala
                elif 860 < x < 931 and 10 < y < 81:
                    grupo_pala.update(event)
                    if pala.clicked:
                        seleccion_planta = "pala"


            # Cada cierto tiempo spawnean zombies
            elif event.type == APARICION_ZOMBIE:
                
                pos_aleatoria = random.randint(0, 4)
                tipo= random.choice(constantes.TIPOS_ZOMBIES)

                if (nivel_dificultad % 8) == 0 and nivel_dificultad >= 8:
                    constantes.CANT_APARICION += 1

                if nivel_dificultad == 10:
                    constantes.TIPOS_ZOMBIES.append("cono")
                    nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, constantes.COLUMNAS_ZOMBIE[pos_aleatoria], "cono", constantes.VIDA_ZOMBIES["cono"])
                    nuevo_zombie.add(grupo_zombies)
                
                if nivel_dificultad % 2 == 0 and nivel_dificultad >= 12 and nivel_dificultad <= 24:
                    #Aumentamos la probabilidad de que aparezcan zombies cono
                    constantes.TIPOS_ZOMBIES.append("cono")
                    
                if nivel_dificultad == 20:
                    constantes.TIPOS_ZOMBIES.append("balde")
                    nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, constantes.COLUMNAS_ZOMBIE[pos_aleatoria], "cono", constantes.VIDA_ZOMBIES["cono"])
                    nuevo_zombie.add(grupo_zombies)
                    nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, constantes.COLUMNAS_ZOMBIE[pos_aleatoria], "balde", constantes.VIDA_ZOMBIES["balde"])
                    nuevo_zombie.add(grupo_zombies)
                
                if nivel_dificultad >= 21 and (nivel_dificultad % 2) != 0:
                    constantes.TIPOS_ZOMBIES.append("balde")

                for i in range(constantes.CANT_APARICION):
                    pos_random = random.randint(0, 4)
                    tipo_zb = random.choice(constantes.TIPOS_ZOMBIES)
                    nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, constantes.COLUMNAS_ZOMBIE[pos_random], tipo, constantes.VIDA_ZOMBIES[tipo_zb])
                    nuevo_zombie.add(grupo_zombies)

                nivel_dificultad += 1

                if constantes.TIEMPO_APARICION >= 2000:
                    constantes.TIEMPO_APARICION -= 500
            ## Cada cierto tiempo spawnean soles
            #elif event.type == APARICION_SOLES:
            #    caida_aleatoria = random.randint(0,8)

            elif event.type == APARICION_OLEADA:

                if nivel_dificultad % 10 == 0:
                    for n in range(constantes.OLEADA_CANT_ZB):
                        pos_random = random.randint(0, 4)
                        tipo_zb = random.choice(constantes.TIPOS_ZOMBIES)
                        nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, constantes.COLUMNAS_ZOMBIE[pos_random], tipo, constantes.VIDA_ZOMBIES[tipo_zb])
                        nuevo_zombie.add(grupo_zombies)
                    constantes.OLEADA_CANT_ZB += 3



        traslucido, vivo = perder(traslucido, grupo_zombies, screen, vivo)

        pygame.display.update()
    reloj.tick(60)

pygame.quit()
