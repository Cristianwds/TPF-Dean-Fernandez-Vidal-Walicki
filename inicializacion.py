import pygame
import constantes
from sonido import iniciar_administrador_sonido

def inicializar_todo():
    screen = inicializar_juego()
    reloj = pygame.time.Clock()
    fondo = cargar_fondos()
    botones = crear_botones()
    fuentes = cargar_fuentes()
    administrador_de_sonido = iniciar_administrador_sonido()
    imagen_nivel = pygame.image.load(r"assets/nivel.png")
    return screen, reloj, fondo, botones, fuentes, administrador_de_sonido, imagen_nivel

def configurar_eventos():
    APARICION_ZOMBIE = pygame.USEREVENT
    APARICION_OLEADA = pygame.USEREVENT + 1
    APARICION_SOLES = pygame.USEREVENT + 2
    APARICION_SOLESGIRASOL = pygame.USEREVENT + 3

    pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)
    pygame.time.set_timer(APARICION_SOLES, constantes.TIEMPO_APARICION_SOL)
    pygame.time.set_timer(APARICION_SOLESGIRASOL, 23000)

    return APARICION_ZOMBIE, APARICION_OLEADA, APARICION_SOLES, APARICION_SOLESGIRASOL

def inicializar_juego():
    pygame.init()
    screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    pygame.display.set_caption("Plants vs. Zombies")
    icono = pygame.image.load(r"assets//icon.png")
    pygame.display.set_icon(icono)
    return screen

def cargar_fondos():
    return {
        "interfaz": pygame.transform.scale(pygame.image.load(r'assets\interfaz.play.png'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "play": pygame.transform.scale(pygame.image.load(r'assets\Fondo_color.jpg'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "exit": pygame.transform.scale(pygame.image.load(r'assets\Fondo_colorexit.jpg'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "dave": pygame.transform.scale(pygame.image.load(r'assets\Crazydave.jpg'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "background": pygame.transform.scale(pygame.image.load(r"assets//map.jpeg").convert(), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "perdiste": pygame.transform.scale(pygame.image.load(r"assets/ZombiesWon.png"), (925, 770))
    }

def crear_botones():
    return {
        "jugar": pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 210, 300, 100),
        "salir": pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 85, 300, 110),
        "dave": pygame.Rect(constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA, 1000, 1000)
    }

def cargar_fuentes():
    return {
        "numero": pygame.font.SysFont('ZombieControl.ttf', 95),
        "sol": pygame.font.SysFont("arial", 20)
    }

def definir_preview():
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
    return preview_dict