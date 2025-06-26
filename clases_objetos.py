import pygame
import constantes
import random
from pygame import mixer
from clases_criaturas import grupo_zombies, Plantas, Petacereza
import funciones

grupo_cortapastos = pygame.sprite.Group()
grupo_semillas = pygame.sprite.Group()
grupo_pala = pygame.sprite.Group()
grupo_deplegables = pygame.sprite.Group()
grupo_sol = pygame.sprite.Group()

class Semillas(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        image,
        reproductor_de_sonido,
        item,
        valor=0,
        cooldown=0,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.valor = valor
        self.cooldown = cooldown
        self.item = item
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.reproductor_de_sonido = reproductor_de_sonido
        self.tiempo = -30000
        self.encooldown = False

    def update(self, evento, contador):
    
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos) and contador[0] >= self.valor:
                if not self.encooldown:
                    self.clicked = True
                    self.reproductor_de_sonido.reproducir_sonido("semilla_seleccionar")
                else:
                    self.clicked = False
            else:
                self.clicked = False

    def dibujarcooldown(self,screen):
        ahora = pygame.time.get_ticks()

        if ahora - self.tiempo >= self.cooldown:
            self.encooldown = False
        else:
            self.encooldown = True

        if self.encooldown:
            imagencooldown = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            imagencooldown.fill((125, 125, 125, 100))
            screen.blit(imagencooldown, (self.rect.x, self.rect.y))



class Cortapasto(pygame.sprite.Sprite):
    cortapasto_id = 0

    def __init__(self, x, y, lista, reproductor_de_sonido):
        self.image = pygame.image.load("assets\cortapasto\cortapasto.png")
        self.rect = self.image.get_rect(topleft=[x, y])
        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height - 60)
        self.hitbox.center = self.rect.center
        self.moving = False
        Cortapasto.cortapasto_id += 1
        self.id = Cortapasto.cortapasto_id
        self.cortapastos_col = lista
        self.reproductor_de_sonido = reproductor_de_sonido
        super().__init__()

    def update(self):
        for zombies in grupo_zombies:
            if self.moving == 0 and self.hitbox.colliderect(zombies.hitbox):
                self.moving = True
                self.reproductor_de_sonido.reproducir_sonido("cortapastos_activar", 0)
            elif self.moving == 1 and self.hitbox.colliderect(zombies.hitbox):
                zombies.recibir_daño(10000)
        if self.moving == True:
            self.rect.x += 10
            self.hitbox.center = self.rect.center
        if self.rect.x >= constantes.FIN_PASTO_X:
            funciones.eliminar(self.cortapastos_col, self.id, Cortapasto)
            self.kill()



class Pala(pygame.sprite.Sprite):

    def __init__(self, reproductor_de_sonido):
        self.image = pygame.image.load(r"assets\pala\pala_icono.jpg")
        self.x = 860
        self.y = 10
        self.rect = self.image.get_rect(topleft = [self.x, self.y])
        self.clicked = False
        self.reproductor_de_sonido = reproductor_de_sonido
        self.cursor = pygame.image.load(r"assets\pala\pala_cursor.png")
        super().__init__()

    def update(self, evento):
        if self.rect.collidepoint(evento.pos):
            self.clicked = True
            self.reproductor_de_sonido.reproducir_sonido("pala_sonido")
        else:
            self.clicked = False

    def dibujar_cursor(self, x,y,screen):
        self.cursor_rect = self.cursor.get_rect(bottomleft = [x, y])
        screen.blit(self.cursor, self.cursor_rect)

    def excavar(self,grilla_entidades:list, grilla_x:int, grilla_y:int, seleccion_planta: str):
        if (isinstance(grilla_entidades[grilla_y][grilla_x], (Plantas, Petacereza))):
            self.reproductor_de_sonido.reproducir_sonido("pala_sonido")
            for zombie in grupo_zombies:
                if grilla_entidades[grilla_y][grilla_x].hitbox.colliderect(zombie.hitbox):
                    self.reproductor_de_sonido.detener_reproduccion("zombie_masticar")
            funciones.eliminar(grilla_entidades, grilla_entidades[grilla_y][grilla_x].id, type(grilla_entidades[grilla_y][grilla_x]))
            seleccion_planta = False
        elif seleccion_planta == "pala":
            seleccion_planta = False
        return seleccion_planta
    