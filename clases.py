import pygame
import constantes

class Criaturas(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, vida):
        super().__init__()
        self.pos_x= x
        self.pos_y= y
        self.imagen= pygame.image.load(imagen).convert_alpha()
        self.forma= self.imagen.get_rect(center=[x, y])
        self.vida= vida
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            self.kill()


class Enemigos(Criaturas):
    def __init__(self, x, y, imagen, vida, velocidad):
        super().__init__(x, y, imagen, vida)
        self.velocidad= velocidad
    def mod_velocidad(self, nueva_vel):
        self.velocidad = nueva_vel
    def movimiento(self):
        self.pos_x -= self.velocidad
        self.forma.center = (self.pos_x, self.pos_y)

class Plantas(Criaturas):
    def __init__(self, x, y, imagen, vida, cooldown, costo):
        super().__init__(x, y, imagen, vida)
        self.cooldown= cooldown
        self.costo= costo


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y, daño):
        super().__init__()
        self.x= x
        self.y= y
        self.imagen= pygame.image.load(imagen).convert_alpha()
        self.daño= daño
        self.forma= self.imagen.get_rect(center=[x, y])
    def update(self):
        self.rect.x += constantes.VELOCIDAD_PROYECTIL
        if self.rect.right > constantes.ANCHO_VENTANA:
            self.kill()

