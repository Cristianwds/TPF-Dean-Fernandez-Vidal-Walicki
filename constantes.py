import os
import copy

# Dimensiones de ventana
ANCHO_VENTANA = 1040
ALTO_VENTANA = 650
FPS = 60

# Grilla del césped
COMIENZO_PASTO_X = 322
FIN_PASTO_X = 1020
COMIENZO_PASTO_Y = 120
FIN_PASTO_Y = 570
CELDA_ANCHO = 78
CELDA_ALTO = 90
XMAX = 946
YMAX = 480


# Estética y visuales
BLANCO_TRANSLUCIDO = (255, 255, 255, 255)
LARGO_BARRA = 490
ALTO_BARRA = 100

# Soles
VALOR_SOL = 25
CONTADOR_SOLES = 50
TIEMPO_APARICION_SOL = 10000  # milisegundos
VELOCIDAD_SOL = 1.5
ALTURAS = [135, 165, 200, 230, 255, 300, 325, 345, 370, 400, 435]

# Zombies
VELOCIDAD_ZOMBIE = 0.3
DAÑO_ZOMBIE = 100
VELOCIDAD_ATAQUE_ZOMBIE = 1000
VEL_ANIM_ZOMBIE = 30
VEL_ANIM_ATQ_CONO = 120
VIDA_ZOMBIES = {
    "normal": 181,
    "cono": 551,
    "balde": 1281
}
DIF_POS_ZOMBIE = 55
COLUMNAS_ZOMBIE = [COMIENZO_PASTO_Y + CELDA_ALTO * fil + DIF_POS_ZOMBIE for fil in range(5)]

TIPOS_ZOMBIES = ["normal"]
Cant_frames = {
    "normal": [
        len(os.listdir(r"assets\zombies\normal\caminata")),
        len(os.listdir(r"assets\zombies\normal\ataque"))
    ],
    "cono": [
        len(os.listdir(r"assets\zombies\cono\caminata")),
        len(os.listdir(r"assets\zombies\cono\ataque"))
    ],
    "balde": [
        len(os.listdir(r"assets\zombies\balde\caminata")),
        len(os.listdir(r"assets\zombies\balde\ataque"))
    ]
}

# Dificultad del juego
ESPERA_INICIAL = 27000
TIEMPO_APARICION = copy.deepcopy(ESPERA_INICIAL)
TIEMPO_GENERACION_ZOMBIE = 18000
CANT_APARICION = 1
OLEADA_CANT_ZB = 3
NV_AUMENTO_SPAWN = 6
NV_SPAWN_CONO = 5
NV_SPAWN_BALDE = 12
NV_OLEADA = 8

# Plantas
VELOCIDAD_PROYECTIL = 10
VEL_ANIM_LG = {
    False: 17,
    True: 32
}
CANT_FRAMES_PLANTAS = {
    "girasol": len(os.listdir(r"assets\girasol")),
    "lanzaguisante": len(os.listdir(r"assets\lanzaguisante")),
    "nuez": len(os.listdir(r"assets\nuez")),
    "hielaguisantes": len(os.listdir(r"assets\hielaguisante"))
}
COOLDOWN_PLANTAS = {
    "lanzaguisantes": 7500,
    "nuez": 30000,
    "girasol": 7500,
    "petacereza": 25000,
    "papapum": 10000,
    "hielaguisantes": 7500
}

# Sonido
SONIDO_INICIO = True
COOLDOWN_ZOMBIES = 2000
