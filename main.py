import pygame
from pygame import mixer
import constantes
import random
from funciones import *
from sonido import *
from clases_criaturas import *
from clases_objetos import *
from funciones_jugabilidad import *
from inicializacion import *

screen, reloj, fondo, botones, fuentes, administrador_de_sonido, imagen_nivel = inicializar_todo()

contador_soles = [50]
contador_para_perder = 0

# Grilla de entidades y grilla de rects.
grilla_rects = [[pygame.Rect(constantes.COMIENZO_PASTO_X + col * constantes.CELDA_ANCHO,constantes.COMIENZO_PASTO_Y + fil * constantes.CELDA_ALTO,constantes.CELDA_ANCHO,constantes.CELDA_ALTO,)for col in range(9)]for fil in range(5)]  # Grilla[fila][columna]
grilla_entidades = [[0 for x in range(9)] for y in range(5)]
fila, columna = 0, 0  # indices para moverse por la matriz

cuad = pygame.Surface((80, 90), pygame.SRCALPHA)
cuad.fill((255, 255, 255, 128))
cuadpos = [constantes.COMIENZO_PASTO_X, constantes.COMIENZO_PASTO_Y]

traslucido = 5
vivo = True

APARICION_ZOMBIE, APARICION_OLEADA, APARICION_SOLES, APARICION_SOLESGIRASOL = configurar_eventos()
nivel_dificultad = 0
delay_spawn_zombie= 0
zombies_a_spawnear = []

# Defino semillas
dic_semillas = definir_semillas(administrador_de_sonido)
# Defino las cortapastos
cortapastos_col = definir_cortapastos(administrador_de_sonido)

#defino la pala
pala = Pala(administrador_de_sonido)
grupo_pala.add(pala)


preview_dict = definir_preview()

seleccion_planta = False
#  x, y, imagen, vida, velocidad
run = True
discurso_dave = False
estado_juego = "inicio"

while run:
    if estado_juego == "inicio":
        estado_juego = ejecutar_pantalla_inicio(screen, botones, fondo, administrador_de_sonido)

    elif estado_juego == "dave":
        estado_juego, discurso_dave = ejecutar_pantalla_dave(screen, fondo["dave"], administrador_de_sonido, discurso_dave)
    
    elif estado_juego == "salir":
        run = False

    elif estado_juego == "juego":

        screen.blit(fondo["background"], (0, 0))  # Fondo

        for planta in grupo_plantas:
            if isinstance(planta, Girasol):
                nuevo_sol = planta.update()
                if nuevo_sol: # Verifica si el girasol devolvió un nuevo sol para generar.
                    grupo_sol.add(nuevo_sol)

        updates_constantes(grilla_entidades)
        dibujos_constantes(screen)

        
        x, y = pygame.mouse.get_pos()
        #Pala que acompaña el mouse si esta seleccionada.
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
                #Si se presiona el click derecho se deselecciona lo que este seleccionado.
                elif event.button == 3:
                    seleccion_planta = False
                        
            # Cada cierto tiempo spawnean soles
            elif event.type == APARICION_SOLES:
                nuevo_sol = Sol(random.randint(350, constantes.ANCHO_VENTANA - 100),-50, random.choice(constantes.ALTURAS), administrador_de_sonido)
                nuevo_sol.add(grupo_sol)
            
            # Cada cierto tiempo se generan zombies
            elif event.type == APARICION_ZOMBIE:
                nivel_dificultad = creacion_zombies(nivel_dificultad, zombies_a_spawnear, administrador_de_sonido)
                # Modifico el tiempo de retraso del evento
                pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)

            elif event.type == APARICION_OLEADA:
                creacion_oleada(nivel_dificultad, zombies_a_spawnear)
        
        #Funcion para spawnear a los zombies
        delay_spawn_zombie = spawnear_zombies_pendientes(zombies_a_spawnear, delay_spawn_zombie, grupo_zombies, administrador_de_sonido)
        


        # Impresion de numeros

        impresion_nivel = fuentes["numero"].render(str(nivel_dificultad), True, (140, 255, 70))
        screen.blit(impresion_nivel, (223, 40))

        if contador_soles[0] == 0:
            posicion_contadorsol = (353, 72)
        elif contador_soles[0] < 100:
            posicion_contadorsol = (347, 72)
        elif contador_soles[0] >= 100:
            posicion_contadorsol = (342, 72)
        
        impresion_cantsol = fuentes["sol"].render(str(contador_soles[0]), True, (0, 0, 0))
        screen.blit(impresion_cantsol, posicion_contadorsol)
        screen.blit(imagen_nivel, (20, 30))
        traslucido, vivo, contador_para_perder = perder(traslucido, grupo_zombies, screen, vivo, administrador_de_sonido, contador_para_perder)

        pygame.display.update()
    reloj.tick(constantes.FPS)

pygame.quit()