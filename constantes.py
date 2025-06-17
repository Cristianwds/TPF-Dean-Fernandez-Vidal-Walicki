import os

ANCHO_VENTANA = 1040
ALTO_VENTANA = 650
VELOCIDAD_PROYECTIL = 10
BLANCO_TRANSLUCIDO = (255, 255, 255, 255)
TIEMPO_APARICION = 15000  # Milisegundos
CANT_APARICION = 1
OLEADA_CANT_ZB= 3
# Para la grilla
COMIENZO_PASTO_X = 322
FIN_PASTO_X = 1020

FPS = 60

COMIENZO_PASTO_Y = 120
FIN_PASTO_Y = 570

CELDA_ALTO = 90
CELDA_ANCHO = 78

LARGO_BARRA = 490
ALTO_BARRA = 100
DIF_POS_ZOMBIE = 55
COLUMNAS_ZOMBIE = [COMIENZO_PASTO_Y + CELDA_ALTO * fil + DIF_POS_ZOMBIE for fil in range(5)]
VELOCIDAD_ZOMBIE = 0.3
DAÑO_ZOMBIE = 100
VELOCIDAD_ATAQUE_ZOMBIE= 1000
VIDA_ZOMBIES= {"normal": 181, "cono": 551, "balde": 1281}

VEL_ANIM_ZOMBIE= 30
VEL_ANIM_LG= {False: 17, True: 32}
VALOR_SOL = 25

CONTADOR_SOLES = 50
TIEMPO_APARICION_SOL = 2000 #Milisegundos
ALTURAS = [135, 165, 200, 230, 255, 300, 325, 345, 370, 400, 435]
VELOCIDAD_SOL = 2

YMAX = 480
XMAX = 946

TIPOS_ZOMBIES = ["normal"]
Cant_frames= {"normal": [len(os.listdir(r"assets\zombies\normal\caminata")), len(os.listdir(r"assets\zombies\normal\ataque"))],
              "cono": [len(os.listdir(r"assets\zombies\cono\caminata")), len(os.listdir(r"assets\zombies\cono\ataque"))], 
              "balde":[len(os.listdir(r"assets\zombies\balde\caminata")), len(os.listdir(r"assets\zombies\balde\ataque"))]}

CANT_FRAMES_PLANTAS= {"girasol": len(os.listdir(r"assets\girasol")), 
                     "lanzaguisante": len(os.listdir(r"assets\lanzaguisante")), 
                     "nuez": len(os.listdir(r"assets\nuez")),
                     "hielaguisantes": len(os.listdir(r"assets\hielaguisante"))}