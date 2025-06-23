import pygame
from pygame import mixer
import constantes
import random
from clases import *
from funciones import *

pygame.init()

contador_soles = [50]
contador_para_perder = 0
administrador_de_sonido = iniciar_administrador_sonido()

reloj = pygame.time.Clock()


# Definicion de pantalla
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

# Titulo e Ícono
pygame.display.set_caption("Plants vs. Zombies")
icono = pygame.image.load(r"assets//icon.png")
pygame.display.set_icon(icono)

# Interfaz del juego

fondo_interfaz = pygame.image.load(r'assets\interfaz.play.png')
fondo_interfaz = pygame.transform.scale(fondo_interfaz, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

fondo_interfaz_play = pygame.image.load(r'assets\Fondo_color.jpg')
fondo_interfaz_play = pygame.transform.scale(fondo_interfaz_play, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

fondo_interfaz_exit = pygame.image.load(r'assets\Fondo_colorexit.jpg')
fondo_interfaz_exit = pygame.transform.scale(fondo_interfaz_exit, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

fondo_crazydave = pygame.image.load(r'assets\Crazydave.jpg')
fondo_crazydave = pygame.transform.scale(fondo_crazydave, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
boton_fondodave = pygame.Rect(constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA, 1000, 1000)

boton_jugar = pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 210, 300, 100)
boton_salir = pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 85, 300, 110)

# Botones para chequear (PLAY Y EXIT)

#font_inicio = pygame.font.SysFont('arial',30 )
#font_titulo = pygame.font.SysFont('arial', 75)
#texto_boton_jugar = font_inicio.render('', True, (0,0,0))
#texto_boton_salir = font_inicio.render('', True, (255,255,255))


# Impresion nivel dificultad
fuente_numero = pygame.font.SysFont('ZombieControl.ttf', 95)
imagen_nivel = pygame.image.load(r"assets\nivel.png")

# Impresion cantidad de soles
fuente_cantsol = pygame.font.SysFont("arial", 20)

# Fondo de pantalla del juego
background = pygame.image.load(r"assets//map.jpeg").convert()
background = pygame.transform.scale(background, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
contador_soles2 = contador_soles[0]

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
delay_spawn_zombie= 0
zombies_a_spawnear = []
APARICION_OLEADA = pygame.USEREVENT + 1

#Evento de aparicion de soles
APARICION_SOLES = pygame.USEREVENT + 2
pygame.time.set_timer(APARICION_SOLES, constantes.TIEMPO_APARICION_SOL)

APARICION_SOLESGIRASOL = pygame.USEREVENT + 3
pygame.time.set_timer(APARICION_SOLESGIRASOL, 23000)


# Defino semillas
dic_semillas = definir_semillas(administrador_de_sonido)
# Defino las cortapastos
cortapastos_col = definir_cortapastos(administrador_de_sonido)

#defino la pala
pala = Pala(administrador_de_sonido)
grupo_pala.add(pala)


preview_dict = {
    "lanzaguisantes": [pygame.image.load(r"assets\lanzaguisante\frame_0.png"),-15,-34],
    "girasol": [pygame.image.load(r"assets\girasol\frame_1.png"),-3,-12],
    "nuez": [pygame.image.load(r"assets\nuez\frame_0.png"),1,-5],
    "petacereza": [pygame.image.load(r"assets\petacereza\gif\frame_1.png"), 0 , 0],
    "papapum" : [pygame.image.load(r"assets\papapum\papapum_activado\frame_2.png"), -10, 0],
    "hielaguisantes": [pygame.image.load(r"assets\hielaguisante\frame_0.png"),-68,-52]
}
for values in preview_dict.values():
    values[0].set_alpha(128)

seleccion_planta = False
#  x, y, imagen, vida, velocidad
run = True
mostrar_inicio = True 
mostrar_dave = False
discurso_inspirador_de_dave = False
while run:
    if mostrar_inicio:
        pantalla_inicio(screen, boton_jugar,boton_salir, fondo_interfaz_play, fondo_interfaz_exit, fondo_interfaz)
        administrador_de_sonido.reproducir_sonido("musica_menu_principal", -1, True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio  = False
                    mostrar_dave = True
                    administrador_de_sonido.detener_reproduccion(
                        "musica_menu_principal")
                    administrador_de_sonido.reproducir_sonido("botones")
                if boton_salir.collidepoint(event.pos):
                    administrador_de_sonido.reproducir_sonido("botones")
                    run = False 
    elif mostrar_dave:
        discurso_inspirador_de_dave = dave(screen,fondo_crazydave, administrador_de_sonido, discurso_inspirador_de_dave)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  
                administrador_de_sonido.detener_reproduccion(discurso_inspirador_de_dave)
                administrador_de_sonido.reproducir_sonido("webiwabo")
                mostrar_dave = False
                administrador_de_sonido.reproducir_sonido("musica_nivel_dia", -1, True)

    elif not mostrar_inicio and not mostrar_dave:
        #dibujar_texto(boton_contadorsoles, None, (255,255,255), constantes.ANCHO_VENTANA / 2 - 280 , constantes.ALTO_VENTANA / 2 - 200)
        # reloj.tick(constantes.FPS)
        # screen.fill(constantes.COLOR_BG) #VAMOS A LLNAR EL FONDO CON EL COLOR BG

        # Dibujar fondo con imagen de grilla
        # screen.blit(background, (0,0))

        screen.blit(background, (0, 0))  # Fondo
        # dibujar_grilla(screen, grilla_rects) #Esta funcion dibuja la grilla, comentar para que no se dibuje

        for planta in grupo_plantas:
            if isinstance(planta, Girasol):
                nuevo_sol = planta.update()
                if nuevo_sol: # Verifica si el girasol devolvió un nuevo sol para generar.
                    grupo_sol.add(nuevo_sol)

        updates_constantes(grilla_entidades)
        dibujos_constantes(screen)
        

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

        previsualizacion(x,y,preview_dict,seleccion_planta,grilla_entidades,screen,cuadpos,cuad)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    # Poner plantas con el click
                    if (constantes.COMIENZO_PASTO_X < x < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y < constantes.FIN_PASTO_Y):
                        x,y = de_pixeles_a_grilla(x,y)
                        cuadpos[0] = constantes.COMIENZO_PASTO_X + (x * constantes.CELDA_ANCHO)
                        cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y * constantes.CELDA_ALTO)
                        if grilla_entidades[y][x] == 0 and seleccion_planta != False and seleccion_planta != "pala":
                            # tiempo_colocacion = pygame.time.get_ticks()
                            # if seleccion_planta in constantes.COOLDOWN_PLANTAS:
                            #     if tiempo_colocacion - ultima_colocacion[seleccion_planta] >= constantes.COOLDOWN_PLANTAS[seleccion_planta]:
                            #         ultima_colocacion[seleccion_planta] = tiempo_colocacion
                                    # print(f"Se aplico el cooldown para la planta {seleccion_planta}")
                            seleccion_planta = plantar(grilla_entidades, seleccion_planta, x, y, administrador_de_sonido, contador_soles, dic_semillas)
                        elif (seleccion_planta == "pala"):
                            seleccion_planta = pala.excavar(grilla_entidades, x, y, seleccion_planta)
                    #Funcionamiento de la seleccion de semillas
                    elif (370 < x < 841 and 10 < y < 100):
                        grupo_semillas.update(event, contador_soles)
                        for semillas in grupo_semillas:
                            if semillas.clicked:
                                seleccion_planta = semillas.item
                        
                    #Seleccion de pala
                    elif 860 < x < 931 and 10 < y < 81:
                        grupo_pala.update(event)
                        if pala.clicked:
                            seleccion_planta = "pala"

                    for sol in grupo_sol:
                        if sol.rect.collidepoint(event.pos): # Verifica que el sol sea recogible y chequea si el click se hizo en la misma posicion del rect del sol
                            contador_soles[0] += sol.recolectar() 
                elif event.button == 3:
                    seleccion_planta = False
                        
            # Cada cierto tiempo spawnean soles
            elif event.type == APARICION_SOLES:
                nuevo_sol = Sol(random.randint(350, constantes.ANCHO_VENTANA - 100),-50, random.choice(constantes.ALTURAS), administrador_de_sonido)
                nuevo_sol.add(grupo_sol)
            
            # Cada cierto tiempo se generan zombies
            elif event.type == APARICION_ZOMBIE:#
                nivel_dificultad = creacion_zombies(nivel_dificultad, zombies_a_spawnear, administrador_de_sonido)
                # Modifico el tiempo de retraso del evento
                pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)

            elif event.type == APARICION_OLEADA:
                creacion_oleada(nivel_dificultad, zombies_a_spawnear)
        
        #Funcion para spawnear a los zombies
        delay_spawn_zombie = spawnear_zombies_pendientes(zombies_a_spawnear, delay_spawn_zombie, grupo_zombies, administrador_de_sonido)
        
        # if zombies_a_spawnear:
        #     tiempo_actual = pygame.time.get_ticks()
        #     if tiempo_actual - delay_spawn_zombie > 1750:
        #         fila, tipo, vida = zombies_a_spawnear.pop(0)
        #         nuevo_zombie = Enemigos(constantes.ANCHO_VENTANA, constantes.COLUMNAS_ZOMBIE[fila], tipo, vida, administrador_de_sonido)
        #         nuevo_zombie.add(grupo_zombies)
        #         delay_spawn_zombie = tiempo_actual

        


        # Impresion de numeros

        impresion_nivel = fuente_numero.render(str(nivel_dificultad), True, (140, 255, 70))
        screen.blit(impresion_nivel, (223, 40))

        if contador_soles[0] == 0:
            posicion_contadorsol = (353, 72)
        elif contador_soles[0] < 100:
            posicion_contadorsol = (347, 72)
        elif contador_soles[0] >= 100:
            posicion_contadorsol = (342, 72)
        
        impresion_cantsol = fuente_cantsol.render(str(contador_soles[0]), True, (0, 0, 0))
        screen.blit(impresion_cantsol, posicion_contadorsol)
        screen.blit(imagen_nivel, (20, 30))
        traslucido, vivo, contador_para_perder = perder(traslucido, grupo_zombies, screen, vivo, administrador_de_sonido, contador_para_perder)
        # Impresion de pos del mouse para futuras pruebas
        # posicion = pygame.mouse.get_pos()
        # print(posicion)

        pygame.display.update()
    reloj.tick(constantes.FPS)

pygame.quit()