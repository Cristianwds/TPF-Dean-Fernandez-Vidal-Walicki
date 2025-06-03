import pygame

class Criaturas():
    def __init__(self, x, y, imagen):
        self.forma= pygame.Rect(0,0, 30, 40) #Ultimos dos numeros son ancho y alto
        self.forma.center= (x, y)
        self.pos_x= x
        self.pos_y= y
        self.imagen= imagen
    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)

class Enemigos(Criaturas):
    def __init__(self, x, y, imagen, velocidad):
        super().__init__(x, y, imagen)
        self.velocidad= velocidad
    def get_velocidad(self):
        return self.velocidad
    def mod_velocidad(self, num):
        self.velocidad = num
    def movimiento(self):
        self.pos_x -= self.velocidad
        self.forma.center = (self.pos_x, self.pos_y)