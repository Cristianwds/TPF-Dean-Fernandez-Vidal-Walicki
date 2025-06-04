import pygame
import constantes

grupo_plantas = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
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
    
class lanzaguisantes(Plantas):
    def __init__(self, x, y, imagen, vida=300, cooldown=7500, costo=100):
        super().__init__(x, y, imagen, vida, cooldown, costo)
        self.costo = costo
        self.cooldown
        self.vida = vida
        self.imagen = pygame.image.load(imagen)
        self.forma = self.imagen.get_rect()
        self.pos_x = x
        self.pos_y = y
        self.cool_time = pygame.time.get_ticks()
        self.ultimo_disparo = pygame.time.get_ticks()

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot >= 1500:
                self.last_shot = now
                guisante = Proyectil("imagen bala", self.rect.x, self.rect.y, 20)
                grupo_proyectiles.add(guisante)


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


def dibujar_grilla(screen, celdas_rects):
    for fila in celdas_rects:
        for rect in fila:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # color blanco, borde de 1 píxel
