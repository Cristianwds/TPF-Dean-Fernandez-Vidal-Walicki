import pygame

def dibujar_grilla(screen, celdas_rects):
    for fila in celdas_rects:
        for rect in fila:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # color blanco, borde de 1 píxel


def eliminar(lista, id_obj):
    for filas in lista:
        for objetos in filas[:]:
            if objetos != 0 and objetos != None:
                if id_obj == objetos.id:
                    filas.remove(objetos)
