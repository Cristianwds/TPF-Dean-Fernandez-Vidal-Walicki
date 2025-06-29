import pygame
from pygame import mixer
import constantes
import random
from funciones import *
from sonido import *
from clases_criaturas import *
from clases_objetos import *

def pantalla_inicio(screen, boton_jugar, boton_salir, fondo_interfaz_play, fondo_interfaz_exit, fondo_interfaz):
    """
    Muestra la pantalla de inicio con efectos visuales al pasar el mouse sobre los botones.

    Inputs:
    -------
    screen: superficie de pygame donde se dibuja la interfaz
    boton_jugar: rectángulo que representa el área del botón 'Jugar'
    boton_salir: rectángulo que representa el área del botón 'Salir'
    fondo_interfaz_play: imagen a mostrar si el mouse está sobre 'Jugar'
    fondo_interfaz_exit: imagen a mostrar si el mouse está sobre 'Salir'
    fondo_interfaz: imagen por defecto de la pantalla de inicio
    """
    pos_mouse = pygame.mouse.get_pos()
    if boton_jugar.collidepoint(pos_mouse):
        screen.blit(fondo_interfaz_play, (0, 0))
    elif boton_salir.collidepoint(pos_mouse):
        screen.blit(fondo_interfaz_exit, (0, 0))
    else:
        screen.blit(fondo_interfaz, (0, 0))
    pygame.display.update()

def ejecutar_pantalla_inicio(screen, botones, fondo, administrador_de_sonido):
    """
    Ejecuta la lógica de la pantalla de inicio, reproduce sonidos y maneja eventos del usuario.

    Inputs:
    -------
    screen: superficie de pygame donde se dibuja la interfaz
    botones: diccionario con las rects de los botones 'jugar' y 'salir'
    fondo: diccionario con las imágenes de fondo para cada estado del menú
    administrador_de_sonido: instancia del reproductor de sonido

    Returns:
    --------
    str: el estado actual del juego tras procesar la entrada del usuario
         ('inicio', 'dave' o 'salir')
    """
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
    """
    Ejecuta la secuencia de introducción del personaje Dave y reproduce sonidos correspondientes.

    Inputs:
    -------
    screen: superficie de pygame donde se dibuja la interfaz
    fondo_dave: imagen de fondo para la escena de Dave
    administrador_de_sonido: instancia del reproductor de sonido
    discurso: nombre del archivo de sonido del discurso actual de Dave

    Returns:
    --------
    tuple: (estado del juego: 'dave', 'juego' o 'salir', 
            discurso: nombre del sonido en reproducción)
    """
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


def perder(traslucido, grupo_zombies, screen, vivo, reproductor_de_sonido, contador):
    """
    Determina si el jugador ha perdido y muestra la pantalla de derrota si corresponde.

    Inputs:
    -------
    traslucido: nivel de opacidad de la pantalla negra superpuesta
    grupo_zombies: grupo de sprites de zombies en el juego
    screen: superficie de pygame donde se dibuja la interfaz
    vivo: bool que indica si el jugador sigue en juego
    reproductor_de_sonido: instancia del reproductor de sonido
    contador: contador para evitar múltiples reproducciones de sonido

    Returns:
    --------
    tuple: (traslucidez actualizada, estado de vida del jugador, contador actualizado)
    """
    for zombie in grupo_zombies:
        if zombie.hitbox.x <= 260:
            vivo = False
    if vivo == False:
        perdiste = pygame.image.load(r"assets/ZombiesWon.png")
        perdiste = pygame.transform.scale(perdiste, (740, 616))
        perdida = pygame.Surface((1040, 650), pygame.SRCALPHA)
        perdida.fill((0, 0, 0, traslucido))
        ahora = pygame.time.get_ticks()
        screen.blit(perdida, (0, 0))
        screen.blit(perdiste, (190, 28))
        if contador == 0:
            reproductor_de_sonido.detener_reproduccion("musica_nivel_dia")
            reproductor_de_sonido.reproducir_sonido("perder", 0, True)
            contador += 1
        if not (reproductor_de_sonido.canales_sonidos_ocupados["perder"].get_busy()):
            reproductor_de_sonido.detener_todos()
        if ahora > 600 and traslucido < 254:
            traslucido += 1
            ahora = pygame.time.get_ticks()
            perdida.fill((0, 0, 0, traslucido))
    traslucidez = traslucido
    return traslucidez, vivo, contador

