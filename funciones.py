import pygame
import constantes
from pygame import mixer
import clases as cl

def dibujar_grilla(screen, celdas_rects):
    for fila in celdas_rects:
        for rect in fila:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # color blanco, borde de 1 píxel

def iniciar_administrador_sonido():
    """
    diccionario_sonidos = {"nombre_sonido": "ruta_sonido"}
    """
    administrador_de_sonido = cl.Administrador_de_sonido()
    diccionario_sonidos = {
        "musica_menu_principal": r"assets\Musica\[Main Menu].mp3",
        "musica_nivel_dia": r"assets\Musica\[Day Stage].mp3",
        "hit1": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit1.ogg",
        "hit2": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit2.mp3",
        "hit3": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit3.ogg",
        "semilla_seleccionar": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_seleccion.ogg",
        "semilla_plantar": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_plantar.ogg",
        "zombie_masticar": r"assets\zombies\zombie_masticando.ogg",
        "zombie_tragar": r"assets\zombies\zombie_tragando_planta.ogg",
        "cortapastos_activar": r"assets\cortapasto\cortapastos_activa.ogg",
        "pala_sonido": r"assets\pala\pala_sonido.mp3",
        "petacereza_explosion": r"assets\petacereza\petacereza_explosion_sonido.ogg",
        "perder": r"assets\Musica\[You Lost].mp3",
        "botones": r"assets\boton_inicio.mp3"
    }
    for nombre_sonido, ruta_sonido in diccionario_sonidos.items():
        administrador_de_sonido.cargar_sonido(ruta_sonido, nombre_sonido)

    return administrador_de_sonido

def definir_semillas(administrador_de_sonido):
    s_girasol = cl.Semillas(380, 10, r"assets\semillas\semillas_girasol.png", administrador_de_sonido, "girasol", 50)
    s_lanzaguisantes = cl.Semillas(440, 10, r"assets//semillas//semillas_lanzaguisantes.png", administrador_de_sonido, "lanzaguisantes", 100)
    s_nuez = cl.Semillas(500, 10, r"assets//semillas//semillas_nuez.png", administrador_de_sonido, "nuez", 50)
    s_petacereza = cl.Semillas(560,10,r"assets\semillas\semilla_petacereza.png",administrador_de_sonido, "petacereza", 150)
    s_papapum = cl.Semillas(620, 10, r"assets\papapum\semilla_papapum_.png", administrador_de_sonido, "papapum", 25)
    s_hielaguisantes = cl.Semillas(680, 10, r"assets//semillas//semillas_hielaguisantes.png", administrador_de_sonido, "hielaguisantes", 175)
    s_lanzaguisantes.add(cl.grupo_semillas)
    s_girasol.add(cl.grupo_semillas)
    s_nuez.add(cl.grupo_semillas)
    s_petacereza.add(cl.grupo_semillas)
    s_papapum.add(cl.grupo_semillas)
    s_hielaguisantes.add(cl.grupo_semillas)

def definir_cortapastos(administrador_de_sonido):
    cortapastos_col = []
    cortapastos_col += [[cl.Cortapasto(constantes.COMIENZO_PASTO_X - constantes.CELDA_ANCHO - 20,constantes.COMIENZO_PASTO_Y + constantes.CELDA_ALTO * fil,cortapastos_col, administrador_de_sonido)]for fil in range(5)]
    for cortapasto_id in cortapastos_col:
        cl.grupo_cortapastos.add(cortapasto_id)
    return cortapastos_col

def updates_constantes(grilla_entidades:list):
    cl.grupo_plantas.update()
    cl.grupo_cortapastos.update()
    cl.grupo_zombies.update()
    cl.grupo_proyectiles.update()
    cl.grupo_deplegables.update(grilla_entidades)
    cl.grupo_sol.update()
    
def dibujos_constantes(screen):
    barra = pygame.image.load(r"assets/barra.png")
    barra = pygame.transform.scale(barra, (constantes.LARGO_BARRA, constantes.ALTO_BARRA))
    cl.grupo_plantas.draw(screen)
    cl.grupo_cortapastos.draw(screen)
    cl.grupo_zombies.draw(screen)
    cl.grupo_proyectiles.draw(screen)
    cl.grupo_sol.draw(screen)
    screen.blit(barra, (300, 0))
    cl.grupo_semillas.draw(screen)
    cl.grupo_pala.draw(screen)
    cl.grupo_deplegables.draw(screen)


def previsualizacion(x_pixels, y_pixels, preview_dict, seleccion_planta, grilla_entidades, screen, cuadpos, cuad):
    if (constantes.COMIENZO_PASTO_X < x_pixels < constantes.FIN_PASTO_X and constantes.COMIENZO_PASTO_Y < y_pixels < constantes.FIN_PASTO_Y):
            
        x_grilla,y_grilla = de_pixeles_a_grilla(x_pixels,y_pixels)
        cuadpos[0] = constantes.COMIENZO_PASTO_X + (x_grilla * constantes.CELDA_ANCHO)
        cuadpos[1] = constantes.COMIENZO_PASTO_Y + (y_grilla * constantes.CELDA_ALTO)
        
        if seleccion_planta != False:
            if seleccion_planta != "pala" and not (isinstance(grilla_entidades[y_grilla][x_grilla], (cl.Plantas, cl.Petacereza))):
                screen.blit(preview_dict[seleccion_planta][0],(cuadpos[0] + preview_dict[seleccion_planta][1], cuadpos[1] + preview_dict[seleccion_planta][2]),)
                screen.blit(cuad, cuadpos)
            elif seleccion_planta == "pala":
                screen.blit(cuad, cuadpos)


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
    

def plantar(grilla_entidades:list, seleccion_planta:str, grilla_x:int, grilla_y:int, reproductor_de_sonido,contador):
    global contador_soles
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
    elif seleccion_planta == "hielaguisantes":
        nueva_planta = cl.lanzaguisantes((grilla_x * constantes.CELDA_ANCHO) + constantes.COMIENZO_PASTO_X - 68,(grilla_y * constantes.CELDA_ALTO) + constantes.COMIENZO_PASTO_Y + 28, grilla_entidades, reproductor_de_sonido, 175, True)
    seleccion_planta = False
    if contador[0] < nueva_planta.costo:
        nueva_planta = 0
    else:
        contador[0] -= nueva_planta.costo
        grilla_entidades[grilla_y][grilla_x] = nueva_planta
        if isinstance(nueva_planta, cl.Plantas):
            cl.grupo_plantas.add(nueva_planta)
        else:
            cl.grupo_deplegables.add(nueva_planta)
        reproductor_de_sonido.reproducir_sonido("semilla_plantar")
    return seleccion_planta


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