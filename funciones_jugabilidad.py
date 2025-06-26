import pygame
from pygame import mixer
import constantes
import random
from funciones import *
from sonido import *
from clases_criaturas import *
from clases_objetos import *

def pantalla_inicio(
    screen,
    boton_jugar,
    boton_salir,
    fondo_interfaz_play,
    fondo_interfaz_exit,
    fondo_interfaz,
):
    """ """
    pos_mouse = pygame.mouse.get_pos()
    if boton_jugar.collidepoint(pos_mouse):
        screen.blit(fondo_interfaz_play, (0, 0))
    elif boton_salir.collidepoint(pos_mouse):
        screen.blit(fondo_interfaz_exit, (0, 0))
    else:
        screen.blit(fondo_interfaz, (0, 0))
    pygame.display.update()

def ejecutar_pantalla_inicio(screen, botones, fondo, administrador_de_sonido):
    pantalla_inicio(screen, botones["jugar"], botones["salir"], fondo["play"], fondo["exit"], fondo["interfaz"])
    administrador_de_sonido.reproducir_sonido("musica_menu_principal", -1, True)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botones["jugar"].collidepoint(event.pos):
                administrador_de_sonido.detener_reproduccion("musica_menu_principal")
                administrador_de_sonido.reproducir_sonido("botones")
                return "dave"
            if botones["salir"].collidepoint(event.pos):
                administrador_de_sonido.reproducir_sonido("botones")
                return "salir"
    return "inicio"

def ejecutar_pantalla_dave(screen, fondo_dave, administrador_de_sonido, discurso):
    discurso = dave(screen, fondo_dave, administrador_de_sonido, discurso)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "salir", discurso
        if event.type == pygame.MOUSEBUTTONDOWN:
            administrador_de_sonido.detener_reproduccion(discurso)
            administrador_de_sonido.reproducir_sonido("webiwabo")
            administrador_de_sonido.reproducir_sonido("musica_nivel_dia", -1, True)
            return "juego", discurso
    return "dave", discurso

