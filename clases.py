import pygame
import constantes
import random
from pygame import mixer

pygame.mixer.init()

grupo_plantas = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
grupo_zombies = pygame.sprite.Group()
class Criaturas(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, vida):
        super().__init__()
        self.pos_x = x
        self.pos_y = y
        self.image = imagen  # Si ya es una Surface
        self.rect = self.image.get_rect(center=[self.pos_x, self.pos_y])
        self.vida = vida
        
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            self.kill()
            return True

class Enemigos(Criaturas):
    def __init__(self, x, y, frames, vida, daño, velocidad= constantes.VELOCIDAD_ZOMBIE):
        super().__init__(x, y, frames[0], vida)
        self.velocidad = velocidad
        self.ultimo_frame = pygame.time.get_ticks()
        self.pos_x = float(x)  # para suavidad
        self.pos_y = y
        self.frames= frames
        self.indice_frame= 0
        self.daño= daño
        self.velocidad_animacion = constantes.VEL_ANIM_ZOMBIE  # milisegundos por frame
        # Redimensionar imagen si hace falta
        #self.image = pygame.transform.scale(self.image, (120, 140))  # opcional

        # Rect de dibujo
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y - 90))

        # Hitbox para colisiones
        self.hitbox = pygame.Rect(0, 0, 30, 60)
        self.hitbox.center = self.rect.center
        self.ultimo_ataque= pygame.time.get_ticks()
    def update(self):
        self.pos_x -= self.velocidad
        self.rect.x = int(self.pos_x)
        self.hitbox.center = self.rect.center
        self.hitbox.x += 5

        for planta in grupo_plantas:
            ahora = pygame.time.get_ticks()
            if self.hitbox.colliderect(planta.hitbox):
                self.velocidad= 0
                if ahora - self.ultimo_ataque >= constantes.VELOCIDAD_ATAQUE_ZOMBIE:
                    self.ultimo_ataque = ahora
                    #random.choice(self.impacto).play()
                    if planta.recibir_daño(self.daño):
                        self.velocidad = constantes.VELOCIDAD_ZOMBIE
                    
        
        tiempo_frame= pygame.time.get_ticks()
        #Cambia de frame cuando se actualiza
        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frame = (self.indice_frame + 1) % len(self.frames)  # Ciclar entre frames
            self.image = self.frames[self.indice_frame]  # Cambiar al siguiente frame
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y - 90))  # Actualizar el rect

        # DEBUG: dibujar hitbox
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)


class Plantas(Criaturas):
    def __init__(self, x, y, imagen, vida, cooldown, costo):
        super().__init__(x, y, imagen, vida)
        self.cooldown = cooldown
        self.costo = costo
        self.pos_x = x
        self.pos_y = y

        # El rect sigue siendo para dibujar la imagen
        self.rect = self.image.get_rect(midleft=(self.pos_x, self.pos_y))
        
        # Hitbox separada: más pequeña, para colisiones
        self.hitbox = pygame.Rect(0, 0, self.rect.width - 50, self.rect.height - 60)
        self.hitbox.midbottom = self.rect.midbottom

class lanzaguisantes(Plantas):
    def __init__(self, x, y, vida=300, cooldown=7500, costo=100):
        self.frames = [pygame.image.load(f"assets\lanzaguisante\\frame_{i}.png").convert_alpha() for i in range(48)]
        #"C:\Users\wikiw\OneDrive\Documentos\Pensamiento_Computacional\Python\TPs\TP3\TPF-Dean-Fernandez-Vidal-Walicki\assets\zombies\cono\caminata"
        #C:\Users\wikiw\OneDrive\Documentos\Pensamiento_Computacional\Python\TPs\TP3\TPF-Dean-Fernandez-Vidal-Walicki\assets\lanzaguisante
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
        ahora = pygame.time.get_ticks()
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]
            self.rect = self.image.get_rect(midleft= (self.pos_x,self.pos_y))

            # Actualizar rect para que la animación se vea bien posicionada

        if ahora - self.ultimo_disparo >= 1500:
            self.ultimo_disparo = ahora
            guisante = Proyectil("assets\\lanzaguisante\\guisante.png", self.hitbox.x + 60, self.hitbox.y + 6, 20)
            grupo_proyectiles.add(guisante)


class Girasol(Plantas):
    def __init__(self, x, y, vida=300, cooldown=7500, costo=50):
        self.x = x
        self.y = y
        self.vida = vida
        self.cooldown = cooldown
        self.costo = costo
        self.image = pygame.image.load("assets\girasol\girasol.png")
        self.rect = self.image.get_rect(midleft=(x, y))
        super().__init__(x, y, self.image, vida, cooldown, costo)


class Nuez(Plantas):
    def __init__(self, x, y, vida=4000, cooldown=30000, costo=50):
        self.x = x
        self.y = y
        self.vida = vida
        self.cooldown = cooldown
        self.costo = costo
        self.image = pygame.image.load("assets/nuez/wallnut.png")
        self.rect = self.image.get_rect(midleft=(x, y))
        super().__init__(x, y, self.image, vida, cooldown, costo)


class Proyectil(pygame.sprite.Sprite):

    def __init__(self,imagen,x,y,daño,impacto=[pygame.mixer.Sound("assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit1.ogg"),pygame.mixer.Sound("assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit2.mp3"),pygame.mixer.Sound("assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit3.ogg")]):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(imagen).convert_alpha()
        self.daño = daño
        self.impacto = impacto

        # rect para posicionar y dibujar la imagen
        self.rect = self.image.get_rect(center=[x, y])

        # hitbox más pequeña para colisiones
        self.hitbox = pygame.Rect(0, 0, self.rect.width - 10, self.rect.height - 10)
        self.hitbox.center = self.rect.center

    def update(self):
        self.rect.x += constantes.VELOCIDAD_PROYECTIL
        self.hitbox.center = self.rect.center  # mantener hitbox alineada

        for zombie in grupo_zombies:
            if self.hitbox.colliderect(zombie.hitbox):
                random.choice(self.impacto).play()
                zombie.recibir_daño(self.daño)
                self.kill()
                break

        if self.rect.right > constantes.ANCHO_VENTANA:
            self.kill()
