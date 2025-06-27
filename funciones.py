import pygame
import constantes
import random
from pygame import mixer
from sonido import *
from clases_criaturas import *
from clases_objetos import *

def updates_constantes(grilla_entidades: list) -> None:
    """
    Esta funcion se ejecuta constantemente en el while principal del main. Se encarga de actualizar todas las clases.

    Inputs:
    ------
    grilla_entidades[filas][columnas]: es la lista, definida en main, donde estan todas las plantas.
    """
    grupo_plantas.update()
    grupo_cortapastos.update()
    grupo_zombies.update()
    grupo_proyectiles.update()
    grupo_deplegables.update(grilla_entidades)
    grupo_sol.update()


def dibujos_constantes(screen):
    """
    Esta funcion se encarga de dibujar todos los assets en pantalla. Se ejecuta constantemente en el while principal en main.

    Inputs:
    -----
    screen: la variable pygame.display principal, utilizada como pantalla.
    """
    barra = pygame.image.load(r"assets/barra.png")
    barra = pygame.transform.scale(
        barra, (constantes.LARGO_BARRA, constantes.ALTO_BARRA)
    )
    grupo_plantas.draw(screen)
    grupo_cortapastos.draw(screen)
    grupo_zombies.draw(screen)
    grupo_proyectiles.draw(screen)
    grupo_sol.draw(screen)
    screen.blit(barra, (310, 0))
    grupo_semillas.draw(screen)
    for semilla in grupo_semillas:
        semilla.dibujarcooldown(screen)
    grupo_pala.draw(screen)
    grupo_deplegables.draw(screen)


def previsualizacion(
    x_pixels,
    y_pixels,
    preview_dict,
    seleccion_planta,
    grilla_entidades,
    screen,
    cuadpos,
    cuad,
):
    """
    Se encarga de la previsualizacion cuando una planta esta seleccionada y se pasas el mouse por algun espacio del pasto.

    Inputs:
    ------
    x_pixels: la posicon en pixeles del eje x del mouse.
    y_pixels: la posicon en pixeles del eje y del mouse.
    preview_dict["item"][imagen_a_previsualizar]: un diccionario definidio en main que tiene las imagenes que se usan para previsualizar las plantas en la grilla.
    seleccion_planta: el item que se usa para identificar la planta seleccionada
    grilla_entidades: la grilla sobre la que se define cada clase de planta.
    screen: pygame.display principal que se usa como pantalla.
    cuadpos: la posicion del pygame.rect gris
    cuad: un pygame.rect gris con el tamaño de cada celda y una opacidad baja
    """
    if (
        constantes.COMIENZO_PASTO_X < x_pixels < constantes.FIN_PASTO_X
        and constantes.COMIENZO_PASTO_Y < y_pixels < constantes.FIN_PASTO_Y
    ):

        x_grilla, y_grilla = de_pixeles_a_grilla(x_pixels, y_pixels)
        cuadpos[0] = constantes.COMIENZO_PASTO_X + (x_grilla * constantes.CELDA_ANCHO)
        cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y_grilla * constantes.CELDA_ALTO)

        if seleccion_planta != False:
            if seleccion_planta != "pala" and not (
                isinstance(
                    grilla_entidades[y_grilla][x_grilla], (Plantas, Petacereza)
                )
            ):
                screen.blit(
                    preview_dict[seleccion_planta][0],
                    (
                        cuadpos[0] + preview_dict[seleccion_planta][1],
                        cuadpos[1] + preview_dict[seleccion_planta][2],
                    ),
                )
                screen.blit(cuad, cuadpos)
            elif seleccion_planta == "pala":
                screen.blit(cuad, cuadpos)


def dave(screen, fondodave, administrador_de_sonido, discurso_inspirador_de_dave):
    """
    Muestra la escena de introducción con Dave y reproduce un sonido aleatorio.

    Parámetros:
    -----------
    screen : Pantalla principal.
    fondodave : Imagen de fondo con Dave.
    administrador_de_sonido : Objeto para controlar los efectos de sonido.
    discurso_inspirador_de_dave : Sonido actual del discurso o None para uno aleatorio.

    Retorna:
    --------
    str
        Nombre del discurso reproducido.
    """
    if not (discurso_inspirador_de_dave):
        discurso_inspirador_de_dave = random.choice(
            ["ovawabodabawabaobadabowadaba", "bwadawbabadfbaw", "budubuwedivadibo"]
        )
        administrador_de_sonido.reproducir_sonido(discurso_inspirador_de_dave, 0, -1)
    screen.blit(fondodave, (0, 0))
    pygame.display.update()
    return discurso_inspirador_de_dave

def de_pixeles_a_grilla(pixeles_x: int, pixeles_y: int) -> tuple:
    """
    Recibe x,y en pixeles y retorna su posición en la grilla de pasto (5x9). Es necesario que el valor ingresado este entre las dimensiones de la grilla en pixeles

    returns:
    -----
    columnas: la coordenada sobre la grilla de las columnas (x)
    filas: la coordenada sobre la grilla de las filas (y)

    raises:
    ------
    ValueError si el valor se va de los límites en pixeles de la grilla.
    """
    if (
        constantes.COMIENZO_PASTO_X < pixeles_x < constantes.FIN_PASTO_X
        and constantes.COMIENZO_PASTO_Y < pixeles_y < constantes.FIN_PASTO_Y
    ):
        columnas = (pixeles_x - constantes.COMIENZO_PASTO_X) // constantes.CELDA_ANCHO
        filas = (pixeles_y - constantes.COMIENZO_PASTO_Y) // constantes.CELDA_ALTO
        return columnas, filas
    else:
        raise (ValueError)

def eliminar(lista: list, id_obj: int, clase) -> None:
    """
    Recibe la lista en la que está guardada el objeto y el id del objeto a eliminar para eliminarlo de la lista de entidades y matarlo del grupo en el que esta almacenado.

    inputs:
    ------
    lista: es la lista de entidades de donde se desea eliminar la entidad.
    id_obj: es el id del objeto que se
    """
    for filas in lista[:]:
        for objetos in filas[:]:
            if objetos != 0 and objetos != None:
                if id_obj == objetos.id and isinstance(objetos, clase):
                    fila_index = lista.index(filas)
                    columna_index = filas.index(objetos)
                    lista[fila_index][columna_index] = 0
                    objetos.kill()


def plantar(
    grilla_entidades: list,
    seleccion_planta: str,
    grilla_x: int,
    grilla_y: int,
    reproductor_de_sonido,
    contador,
    gruposemillas,
) -> False:
    """
    La funcion encarnada de plantar las plantas sobre el pasto.

    Inputs:
    ------
    grilla_entidades: la grilla sobre la que están colocadas las plantas.
    seleccion_planta: el item de la planta seleccionada ("lanzaguisantes", "girasol", "nuez", "petacereza", "papapum" o "hielaguisantes")
    grilla_x: la columna sobre la que se posicionará la planta.
    grilla_y: la fila sobre la que se posicionará la planta.
    reproductor_de_sonido: variable de clase Administrador_de_sonido donde se reproducirán los sonidos de plantar.
    gruposemoillas: el grupo de pygame.Sprites destinado a esta clase.

    Returns:
    ------
    seleccion_planta: devuelve un False en la planta seleccionada para deseleccionar la planta.

    """
    if seleccion_planta == "lanzaguisantes":
        nueva_planta = lanzaguisantes(
            (grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,
            (grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20,
            grilla_entidades,
            reproductor_de_sonido,
        )  # En la pos de la planta se pasa de numero de grilla a pixeles.
    elif seleccion_planta == "girasol":
        nueva_planta = Girasol(
            (grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,
            (grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20,
            grilla_entidades,
            reproductor_de_sonido,
        )
    elif seleccion_planta == "nuez":
        nueva_planta = Nuez(
            (grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,
            (grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20,
            grilla_entidades,
            reproductor_de_sonido,
        )
    elif seleccion_planta == "petacereza":
        nueva_planta = Petacereza(
            (grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,
            (grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20,
            reproductor_de_sonido,
        )
    elif seleccion_planta == "papapum":
        nueva_planta = Papapum(
            (grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 15,
            (grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 20,
            grilla_entidades,
            reproductor_de_sonido,
        )
    elif seleccion_planta == "hielaguisantes":
        nueva_planta = lanzaguisantes(
            (grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 68,
            (grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 28,
            grilla_entidades,
            reproductor_de_sonido,
            175,
            True,
        )
    gruposemillas[seleccion_planta].tiempo = pygame.time.get_ticks()
    seleccion_planta = False
    if contador[0] < nueva_planta.costo:
        nueva_planta = 0
    else:
        contador[0] -= nueva_planta.costo
        grilla_entidades[grilla_y][grilla_x] = nueva_planta
        if isinstance(nueva_planta, Plantas):
            grupo_plantas.add(nueva_planta)
        else:
            grupo_deplegables.add(nueva_planta)
        reproductor_de_sonido.reproducir_sonido("semilla_plantar")
    return seleccion_planta