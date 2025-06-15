import pygame
import constantes
from pygame import mixer
import clases as cl

def dibujar_grilla(screen, celdas_rects):
    for fila in celdas_rects:
        for rect in fila:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # color blanco, borde de 1 píxel


def eliminar(lista:list, id_obj:int, clase) -> None:
    """
    Recibe la lista en la que está guardada el objeto y el id del objeto a eliminar para eliminarlo de la lista.
    """
    for filas in lista[:]:
        for objetos in filas[:]:
            if objetos != 0 and objetos != None:
                if id_obj == objetos.id and isinstance(objetos, clase):
                    fila_index = lista.index(filas)
                    columna_index = filas.index(objetos)
                    lista[fila_index][columna_index] = 0
                    objetos.kill()


def de_pixeles_a_grilla(pixeles_x:int, pixeles_y:int) -> tuple:
    """
    Recibe x,y en pixeles y retorna su posición en la grilla de pasto (5x9). Es necesario que el valor ingresado este entre las dimensiones de la grilla en pixeles
    
    raises:
    ------
    ValueError si el valor se va de los límites en pixeles de la grilla.
    """
    if constantes.COMIENZO_PASTO_X<pixeles_x<constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y<pixeles_y<constantes.FIN_PASTO_Y:
        columnas = (pixeles_x - constantes.COMIENZO_PASTO_X) // constantes.CELDA_ANCHO
        filas = (pixeles_y - constantes.COMIENZO_PASTO_Y) // constantes.CELDA_ALTO
        return columnas, filas
    else:
        raise(ValueError)
    

def plantar(grilla_entidades:list, seleccion_planta:str, grilla_x:int, grilla_y:int, reproductor_de_sonido):
    if seleccion_planta == "lanzaguisantes":
        nueva_planta = cl.lanzaguisantes((grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,(grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20, grilla_entidades, reproductor_de_sonido) #En la pos de la planta se pasa de numero de grilla a pixeles.
    elif seleccion_planta == "girasol":
        nueva_planta = cl.Girasol((grilla_x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(grilla_y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, grilla_entidades, reproductor_de_sonido)
    elif seleccion_planta == "nuez":
        nueva_planta = cl.Nuez((grilla_x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(grilla_y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, grilla_entidades, reproductor_de_sonido)
    elif seleccion_planta == "petacereza":
        nueva_planta = cl.Petacereza((grilla_x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(grilla_y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, reproductor_de_sonido)
    elif seleccion_planta == "papapum":
        nueva_planta = cl.Papapum((grilla_x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(grilla_y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20,grilla_entidades, reproductor_de_sonido)
    seleccion_planta = False
    grilla_entidades[grilla_y][grilla_x] = nueva_planta
    if isinstance(nueva_planta, cl.Plantas):
        cl.grupo_plantas.add(nueva_planta)
    else:
        cl.grupo_deplegables.add(nueva_planta)
    reproductor_de_sonido.reproducir_sonido("semilla_plantar")
    return seleccion_planta


def iniciar_administrador_sonido(diccionario_sonidos:dict):
    """
    diccionario_sonidos = {"nombre_sonido": "ruta_sonido"}
    """
    administrador_de_sonido = cl.Administrador_de_sonido()

    for nombre_sonido, ruta_sonido in diccionario_sonidos.items():
        administrador_de_sonido.cargar_sonido(ruta_sonido, nombre_sonido)

    return administrador_de_sonido


def perder(traslucido, grupo_zombies, screen, vivo, reproductor_de_sonido, contador):
    for zombie in grupo_zombies:
        if zombie.hitbox.x <= 260:
            vivo = False
    if vivo == False:
        perdiste = pygame.image.load(r"assets/ZombiesWon.png")
        perdiste = pygame.transform.scale(perdiste, (740,616))
        perdida = pygame.Surface((1040, 650), pygame.SRCALPHA)
        perdida.fill((0, 0, 0, traslucido))
        ahora = pygame.time.get_ticks()
        screen.blit(perdida, (0,0))
        screen.blit(perdiste, (190,28))
        if contador == 0:
            reproductor_de_sonido.detener_reproduccion("musica_nivel_dia")
            reproductor_de_sonido.reproducir_sonido("perder", 0, True)
            contador += 1
        if ahora > 600 and traslucido < 254:
            traslucido += 1
            ahora = pygame.time.get_ticks()
            perdida.fill((0, 0, 0, traslucido))
    traslucidez = traslucido
    return traslucidez, vivo, contador