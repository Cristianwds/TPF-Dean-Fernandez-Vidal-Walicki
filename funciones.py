import pygame
import constantes
from pygame import mixer
import clases as cl

def dibujar_grilla(screen, celdas_rects):
    for fila in celdas_rects:
        for rect in fila:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # color blanco, borde de 1 píxel


def eliminar(lista:list, id_obj:int) -> None:
    """
    Recibe la lista en la que está guardada el objeto y el id del objeto a eliminar para eliminarlo de la lista.
    """
    for filas in lista[:]:
        for objetos in filas[:]:
            if objetos != 0 and objetos != None:
                if id_obj == objetos.id:
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
    

def plantar(grilla_entidades:list, seleccion_planta:str, grilla_x:int, grilla_y:int):
    if seleccion_planta == "lanzaguisantes":
        nueva_planta = cl.lanzaguisantes((grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,(grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20, grilla_entidades) #En la pos de la planta se pasa de numero de grilla a pixeles.
    elif seleccion_planta == "girasol":
        nueva_planta = cl.Girasol((grilla_x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(grilla_y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, grilla_entidades)
    elif seleccion_planta == "nuez":
        nueva_planta = cl.Nuez((grilla_x * constantes.CELDA_ANCHO)+ constantes.COMIENZO_PASTO_X- 15,(grilla_y * constantes.CELDA_ALTO)+ constantes.COMIENZO_PASTO_Y+ 20, grilla_entidades)
    seleccion_planta = False
    grilla_entidades[grilla_y][grilla_x] = nueva_planta
    cl.grupo_plantas.add(nueva_planta)
    pygame.mixer.Sound(
        r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_plantar.ogg"
    ).play()
    return seleccion_planta


def excavar(grilla_entidades:list, grilla_x:int, grilla_y:int, seleccion_planta: str, pala):
    if (isinstance(grilla_entidades[grilla_y][grilla_x], cl.Plantas)):
        pala.sonido.play()
        # grilla_entidades[grilla_y][grilla_x].kill()
        eliminar(grilla_entidades, grilla_entidades[grilla_y][grilla_x].id)
        seleccion_planta = False
    elif seleccion_planta == "pala":
        seleccion_planta = False
    return seleccion_planta

def perder(traslucido, grupo_zombies, screen, vivo):
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
        if ahora > 600 and traslucido < 254:
            traslucido += 1
            ahora = pygame.time.get_ticks()
            perdida.fill((0, 0, 0, traslucido))
    traslucidez = traslucido
    return traslucidez, vivo