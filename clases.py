import pygame
import constantes

grupo_plantas = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
grupo_zombies = pygame.sprite.Group()
class Criaturas(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, vida):
        super().__init__()
        self.pos_x = x
        self.pos_y = y

        if isinstance(imagen, str):
            self.image = pygame.image.load(imagen).convert_alpha()
        else:
            self.image = imagen  # Ya es una Surface

        self.rect = self.image.get_rect(center=[self.pos_x, self.pos_y])
        self.vida = vida
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
    def update(self):
        self.pos_x -= self.velocidad
        self.rect.center = (self.pos_x, self.pos_y)

class Plantas(Criaturas):
    def __init__(self, x, y, imagen, vida, cooldown, costo):
        super().__init__(x, y, imagen, vida)
        self.cooldown= cooldown
        self.costo= costo
    
class lanzaguisantes(Plantas):
    def __init__(self, x, y, vida=300, cooldown=7500, costo=100):
        self.frames = [pygame.image.load(f"assets\\lanzaguisante\\frame_{i}.png").convert_alpha() for i in range(48)]
        self.indice_frames = 0
        self.image = self.frames[self.indice_frames]
        self.costo = costo
        self.cooldown = cooldown
        self.vida = vida
        self.rect = self.image.get_rect()
        self.pos_x = x
        self.pos_y = y
        self.cool_time = pygame.time.get_ticks()
        self.ultimo_disparo = pygame.time.get_ticks()
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion = 18  # milisegundos por frame
        self.rect = self.image.get_rect(midleft= (x,y))
        Plantas.__init__(self, x, y, self.image, vida, cooldown, costo)


    def update(self):
        # Animación
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = ahora
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]

        if ahora - self.ultimo_disparo >= 1500:
            self.ultimo_disparo = ahora
            guisante = Proyectil(f"assets\\lanzaguisante\\pea.png", self.rect.x, self.rect.y, 20)
            grupo_proyectiles.add(guisante)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y, daño):
        super().__init__()
        self.x= x
        self.y= y
        self.image= pygame.image.load(imagen).convert_alpha()
        self.daño= daño
        self.rect= self.image.get_rect(center=[x, y])

    def update(self):
        self.rect.x += constantes.VELOCIDAD_PROYECTIL
        if self.rect.right > constantes.ANCHO_VENTANA:
            self.kill()


def dibujar_grilla(screen, celdas_rects):
    for fila in celdas_rects:
        for rect in fila:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # color blanco, borde de 1 píxel
