import pygame
import constantes
from sonido import iniciar_administrador_sonido
from clases_objetos import *
from clases_criaturas import *

def inicializar_todo():
    """
    Inicializa todos los elementos fundamentales del juego: pantalla, reloj, fondos, botones, fuentes, sonidos y fondo del nivel.

    Returns:
    -------
    tuple: contiene screen, reloj, fondo, botones, fuentes, administrador_de_sonido, imagen_nivel
    """
    screen = inicializar_juego()
    reloj = pygame.time.Clock()
    fondo = cargar_fondos()
    botones = crear_botones()
    fuentes = cargar_fuentes()
    administrador_de_sonido = iniciar_administrador_sonido()
    imagen_nivel = pygame.image.load(r"assets/nivel.png")
    return screen, reloj, fondo, botones, fuentes, administrador_de_sonido, imagen_nivel

def configurar_eventos():
    """
    Configura los eventos temporizados del juego, como la aparición de zombies y soles.

    Returns:
    -------
    tuple: constantes que representan los identificadores de eventos personalizados (USEREVENT + n)
    """
    APARICION_ZOMBIE = pygame.USEREVENT
    APARICION_OLEADA = pygame.USEREVENT + 1
    APARICION_SOLES = pygame.USEREVENT + 2
    APARICION_SOLESGIRASOL = pygame.USEREVENT + 3

    pygame.time.set_timer(APARICION_ZOMBIE, constantes.TIEMPO_APARICION)
    pygame.time.set_timer(APARICION_OLEADA, constantes.TIEMPO_OLEADA)
    pygame.time.set_timer(APARICION_SOLES, constantes.TIEMPO_APARICION_SOL)
    pygame.time.set_timer(APARICION_SOLESGIRASOL, 23000)

    return APARICION_ZOMBIE, APARICION_OLEADA, APARICION_SOLES, APARICION_SOLESGIRASOL

def inicializar_juego():
    """
    Inicializa el entorno de pygame, la ventana principal y el ícono del juego.

    Returns:
    -------
    pygame.Surface: pantalla principal del juego.
    """
    pygame.init()
    screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    pygame.display.set_caption("Plants vs. Zombies")
    icono = pygame.image.load(r"assets//icon.png")
    pygame.display.set_icon(icono)
    return screen

def cargar_fondos():
    """
    Carga y escala los distintos fondos usados en el juego.

    Returns:
    -------
    dict: contiene imágenes escaladas para interfaz, menú de inicio, menú de salida, fondo de Crazy Dave, fondo del mapa, y pantalla de derrota.
    """
    return {
        "interfaz": pygame.transform.scale(pygame.image.load(r'assets\interfaz.play.png'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "play": pygame.transform.scale(pygame.image.load(r'assets\Fondo_color.jpg'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "exit": pygame.transform.scale(pygame.image.load(r'assets\Fondo_colorexit.jpg'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "dave": pygame.transform.scale(pygame.image.load(r'assets\Crazydave.jpg'), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "background": pygame.transform.scale(pygame.image.load(r"assets//map.jpeg").convert(), (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)),
        "perdiste": pygame.transform.scale(pygame.image.load(r"assets/ZombiesWon.png"), (925, 770))
    }

def crear_botones():
    """
    Crea los rectángulos interactivos usados como botones en el menú.

    Returns:
    -------
    dict: contiene pygame.Rect para los botones de jugar, salir y avanzar diálogo con Dave.
    """
    return {
        "jugar": pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 210, 300, 100),
        "salir": pygame.Rect(constantes.ANCHO_VENTANA / 2 + 25, constantes.ALTO_VENTANA/ 2 - 85, 300, 110),
        "dave": pygame.Rect(constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA, 1000, 1000)
    }

def cargar_fuentes():
    """
    Carga las fuentes tipográficas usadas en el HUD del juego.

    Returns:
    -------
    dict: contiene fuentes pygame con nombres clave "numero" y "sol"
    """
    return {
        "numero": pygame.font.SysFont('ZombieControl.ttf', 95),
        "sol": pygame.font.SysFont("arial", 20)
    }

def definir_preview():
    """
    Define un diccionario con imágenes semitransparentes usadas para previsualizar plantas antes de colocarlas.

    Returns:
    -------
    dict: contiene claves con el nombre de la planta y valores con una lista [imagen, offset_x, offset_y]
    """
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
    
def definir_cortapastos(administrador_de_sonido):
    """
    Define una lista con todas las cortapastos [[Cortapasto], [Cortapasto],...]

    Inputs:
    -----
    administrador_de_sonido: variable clase Administrador_de_sonido


    Returns:
    ----
    cortapastos_col[Filas][Columnas]: Una lista con todas las cortapastos almacenadas.
    """
    cortapastos_col = []
    cortapastos_col += [
        [
            Cortapasto(
                constantes.COMIENZO_PASTO_X - constantes.CELDA_ANCHO - 20,
                constantes.COMIENZO_PASTO_Y + constantes.CELDA_ALTO * fil,
                cortapastos_col,
                administrador_de_sonido,
            )
        ]
        for fil in range(5)
    ]
    for cortapasto_id in cortapastos_col:
        grupo_cortapastos.add(cortapasto_id)
    return cortapastos_col

def definir_semillas(administrador_de_sonido):
    """
    Crea las variables con todas las semillas (clase Semillas) seleccionables y las añade a su respectivo grupo.

    Inputs:
    ------
    administrador_de_sonido: una variable de clase Administrador_de_sonido la cual posteriormente se almacena en cada variable clase Semillas.


    Returns:
    ------
    diccionario_semillas: un diccionario {"item": semilla}. Se usa en varias funciones para comparar la clave del diccionario y ver que planta esta seleccionada.
    """

    s_girasol = Semillas(
        413,
        10,
        r"assets\semillas\semillas_girasol.png",
        administrador_de_sonido,
        "girasol",
        50,
        constantes.COOLDOWN_PLANTAS["girasol"],
    )
    s_lanzaguisantes = Semillas(
        476,
        10,
        r"assets//semillas//semillas_lanzaguisantes.png",
        administrador_de_sonido,
        "lanzaguisantes",
        100,
        constantes.COOLDOWN_PLANTAS["lanzaguisantes"],
    )
    s_nuez = Semillas(
        539,
        10,
        r"assets//semillas//semillas_nuez.png",
        administrador_de_sonido,
        "nuez",
        50,
        constantes.COOLDOWN_PLANTAS["nuez"],
    )
    s_petacereza = Semillas(
        602,
        10,
        r"assets\semillas\semilla_petacereza.png",
        administrador_de_sonido,
        "petacereza",
        150,
        constantes.COOLDOWN_PLANTAS["petacereza"],
    )
    s_papapum = Semillas(
        665,
        10,
        r"assets\papapum\semilla_papapum_.png",
        administrador_de_sonido,
        "papapum",
        25,
        constantes.COOLDOWN_PLANTAS["papapum"],
    )
    s_hielaguisantes = Semillas(
        728,
        10,
        r"assets//semillas//semillas_hielaguisantes.png",
        administrador_de_sonido,
        "hielaguisantes",
        175,
        constantes.COOLDOWN_PLANTAS["hielaguisantes"],
    )
    s_lanzaguisantes.add(grupo_semillas)
    s_girasol.add(grupo_semillas)
    s_nuez.add(grupo_semillas)
    s_petacereza.add(grupo_semillas)
    s_papapum.add(grupo_semillas)
    s_hielaguisantes.add(grupo_semillas)
    diccionario_semillas = {
        "girasol": s_girasol,
        "lanzaguisantes": s_lanzaguisantes,
        "nuez": s_nuez,
        "petacereza": s_petacereza,
        "papapum": s_papapum,
        "hielaguisantes": s_hielaguisantes,
    }
    return diccionario_semillas

def creacion_zombies(
    nivel_dificultad: int, zombies_a_spawnear: list[tuple], administrador_de_sonido) -> int:
    """Genera zombies para spawnear en funcion del nivel de dificultad y el tiempo de aparicion
    
    Inputs: 
    ------
    Nivel_dificultad (int): nivel de dificultad del juego
    zombies_a_spawnear (list): lista que acumula los zombies ya creados en espera para spawnear
    administrador_de_sonido: administrador que maneja la reproduccion de efectos de sonido
    
    Return: 
    ------
    nivel_dificultad (int): el nivel de dificultad incrementado en 1 luego de crear los nuevos zombies
    """

    if constantes.SONIDO_INICIO:
        administrador_de_sonido.reproducir_sonido("zombies_coming")
        constantes.SONIDO_INICIO = False
    if (
        nivel_dificultad % constantes.NV_AUMENTO_SPAWN
    ) == 0 and nivel_dificultad >= constantes.NV_AUMENTO_SPAWN:
        constantes.CANT_APARICION += 1

    if nivel_dificultad == constantes.NV_SPAWN_CONO:
        zombies_a_spawnear.append(
            (random.randint(0, 4), "cono", constantes.VIDA_ZOMBIES["cono"])
        )

    if (
        nivel_dificultad % 2 == 0
        and constantes.NV_SPAWN_CONO
        <= nivel_dificultad
        <= constantes.NV_SPAWN_BALDE + 4
    ):
        # Aumentamos gradualmente la probabilidad de aparición de los zombies cono
        constantes.TIPOS_ZOMBIES.append("cono")

    if nivel_dificultad == constantes.NV_SPAWN_BALDE and constantes.CONTADOR_NV_BALDE == 0:
        lista_ubis = [0, 1, 2, 3, 4]
        ubi1 = random.choice(lista_ubis)
        ubi2 = random.choice(lista_ubis)
        zombies_a_spawnear.append((ubi1, "cono", constantes.VIDA_ZOMBIES["cono"]))
        zombies_a_spawnear.append((ubi2, "balde", constantes.VIDA_ZOMBIES["balde"]))
        constantes.CONTADOR_NV_BALDE += 1

    if nivel_dificultad >= constantes.NV_SPAWN_BALDE and (nivel_dificultad % 2) == 0:
        constantes.TIPOS_ZOMBIES.append("balde")

    for i in range(constantes.CANT_APARICION):
        pos_random = random.randint(0, 4)
        tipo_zb = random.choice(constantes.TIPOS_ZOMBIES)
        vida = constantes.VIDA_ZOMBIES[tipo_zb]
        zombies_a_spawnear.append((pos_random, tipo_zb, vida))

    if constantes.TIEMPO_APARICION == constantes.ESPERA_INICIAL:
        constantes.TIEMPO_APARICION = constantes.TIEMPO_GENERACION_ZOMBIE
    elif constantes.TIEMPO_APARICION >= 6000:
        constantes.TIEMPO_APARICION -= 400
    nivel_dificultad += 1
    return nivel_dificultad


def creacion_oleada(nivel_dificultad: int, zombies_a_spawnear: list[tuple]) -> None:
    """Genera una oleada extra de zombies cuando el nivel es multiplo de NV_OLEADA. Ademas, incrementa
    el numero de zombies que se generaran en la proxima oleada
    
    Inputs:
    ------
    nivel_dificultad (int): nivel actual del juego.
    zombies_a_spawnear (list): lista que acumula los zombies creados pero no colocados.

    """
    # if nivel_dificultad % constantes.NV_OLEADA == 0:
    for n in range(constantes.OLEADA_CANT_ZB):
        pos_random = random.randint(0, 4)
        tipo_zb = random.choice(constantes.TIPOS_ZOMBIES)
        vida = constantes.VIDA_ZOMBIES[tipo_zb]
        zombies_a_spawnear.append((pos_random, tipo_zb, vida))
    constantes.OLEADA_CANT_ZB += 2


def spawnear_zombies_pendientes(zombies_a_spawnear:list[tuple], delay_spawn_zombie: int, grupo_zombies: "pygame.sprite.Group", administrador_de_sonido) -> int:
    """Spawnea el siguiente zombie en cola cuando ha pasado suficiente tiempo desde el último spawn.

    Verifica si hay zombies pendientes y si ya transcurrió el tiempo de espera entre spawns (COOLDOWN_ZOMBIES), extrae un zombie de la 
    lista, crea su instancia y lo agrega al grupo de zombies que se dibujan y actualizan en pantalla.

    Inputs:
    ------
    zombies_a_spawnear (list): lista que acumula los zombies pendientes por spawnear.
    delay_spawn_zombie (int): último tiempo en milisegundos en que se spawneó un zombie.
    grupo_zombies (pygame.sprite.Group): grupo al que se añaden los nuevos zombies.
    administrador_de_sonido: administrador que maneja los efectos de sonido.

    Returns:
        int: tiempo actual en milisegundos que servirá como nuevo delay para el próximo spawn.
    """
    
    tiempo_actual = pygame.time.get_ticks()
    if zombies_a_spawnear and (tiempo_actual - delay_spawn_zombie > constantes.COOLDOWN_ZOMBIES):
        fila, tipo, vida = zombies_a_spawnear.pop(0)
        nuevo_zombie = Enemigos(
            constantes.ANCHO_VENTANA,
            constantes.COLUMNAS_ZOMBIE[fila],
            tipo,
            vida,
            administrador_de_sonido,)
        nuevo_zombie.add(grupo_zombies)
        delay_spawn_zombie = tiempo_actual
    return delay_spawn_zombie