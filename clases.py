import pygame
import constantes
import random
from pygame import mixer
from funciones import *
pygame.mixer.init()

grupo_plantas = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
grupo_zombies = pygame.sprite.Group()
grupo_cortapastos = pygame.sprite.Group()
grupo_semillas = pygame.sprite.Group()
grupo_pala = pygame.sprite.Group()
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
    def __init__(self, x, y, tipo, vida, daño= constantes.DAÑO_ZOMBIE, velocidad= constantes.VELOCIDAD_ZOMBIE):
        
        # Se cargan los frames
        self.tipo = tipo
        self.frames_caminata = [pygame.image.load(f"assets/zombies/{self.tipo}/caminata/frame_{i}.png").convert_alpha() for i in range(constantes.Cant_frames[self.tipo][0])]
        self.frames_ataque = [pygame.image.load(f"assets/zombies/{self.tipo}/ataque/frame_{i}.png").convert_alpha() for i in range (constantes.Cant_frames[self.tipo][1])] # Por ahora tiene las mismas img de movimiento
        
        self.estado= "caminar" # caminar o atacar
        self.frames= self.frames_caminata
        imagen_inicial = self.frames[0]

        # Se llama a la Superclase con la imagen cargada
        super().__init__(x, y, imagen_inicial, vida)

        self.velocidad = velocidad
        self.daño = daño
        self.pos_x = float(x)
        self.pos_y = y
        self.indice_frame = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.ultimo_ataque = pygame.time.get_ticks()
        self.velocidad_animacion = constantes.VEL_ANIM_ZOMBIE
        #self.image = pygame.transform.scale(self.image, (120, 140))  # opcional

        # Rect de dibujo
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y - 90))

        # Hitbox para colisiones
        self.hitbox = pygame.Rect(0, 0, 30, 60)
        self.hitbox.center = self.rect.center
        
    def update(self):
        atacando = False

        for planta in grupo_plantas:
            ahora = pygame.time.get_ticks()
            if self.hitbox.colliderect(planta.hitbox):
                atacando = True
                self.velocidad= 0
                if ahora - self.ultimo_ataque >= constantes.VELOCIDAD_ATAQUE_ZOMBIE:
                    self.ultimo_ataque = ahora
                    #random.choice(self.impacto).play()
                    if planta.recibir_daño(self.daño):
                        self.velocidad = constantes.VELOCIDAD_ZOMBIE
            
        if atacando:
            if self.estado != "atacar":
                self.estado = "atacar"
                self.frames = self.frames_ataque
                self.indice_frame = 0
        else:
            if self.estado != "caminar":
                self.estado = "caminar"
                self.frames = self.frames_caminata
                self.indice_frame = 0
            self.pos_x -= self.velocidad
            if self.pos_x <= 0:
                self.kill()

        self.rect.x = round(self.pos_x)
        self.hitbox.center = self.rect.center
        self.hitbox.x += 5
        
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
    plantas_id = 0
    def __init__(self, x, y, imagen, vida, cooldown, costo, lista_entidades):
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
        self.lista_entidades = lista_entidades
        Plantas.plantas_id += 1
        self.id = Plantas.plantas_id

    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            eliminar(self.lista_entidades, self.id)
            self.kill()
            return True

class lanzaguisantes(Plantas):
    def __init__(self, x, y, lista_entidades, vida=300, cooldown=7500, costo=100):
        self.frames = [pygame.image.load(f"assets\lanzaguisante\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["lanzaguisante"])]
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
        Plantas.__init__(self, x, y, self.image, vida, cooldown, costo, lista_entidades)

    def update(self):
        ahora = pygame.time.get_ticks()
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]

        if ahora - self.ultimo_disparo >= 1500:
            self.ultimo_disparo = ahora
            guisante = Proyectil(r"assets\\proyectil\\guisante.png", self.hitbox.x + 60, self.hitbox.y - 15, 20)
            grupo_proyectiles.add(guisante)


class Girasol(Plantas):
    def __init__(self, x, y, lista_entidades, vida=300, cooldown=7500, costo=50):
        self.x = x
        self.y = y
        self.vida = vida
        self.frames = [pygame.image.load(f"assets\girasol\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["girasol"])]
        self.indice_frames = 0
        self.image = self.frames[self.indice_frames]
        self.cooldown = cooldown
        self.costo = costo
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion = 18
        self.rect = self.image.get_rect(midleft=(x, y))
        super().__init__(x, y, self.image, vida, cooldown, costo, lista_entidades)

    def update(self):
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]

class Nuez(Plantas):
    def __init__(self, x, y, lista_entidades, vida=4000, cooldown=30000, costo=50):
        self.x = x
        self.y = y
        self.vida = vida
        self.cooldown = cooldown
        self.costo = costo
        self.frames = [pygame.image.load(f"assets\\nuez\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["nuez"])]
        self.indice_frames = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion= 35
        self.image = self.frames[self.indice_frames]
        self.rect = self.image.get_rect(midleft=(x, y))
        super().__init__(x, y, self.image, vida, cooldown, costo, lista_entidades)

    def update(self):
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]


class Proyectil(pygame.sprite.Sprite):

    def __init__(self,imagen,x,y,daño,impacto=[pygame.mixer.Sound(r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit1.ogg"),pygame.mixer.Sound("assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit2.mp3"),pygame.mixer.Sound("assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit3.ogg")]):
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


class Semillas(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        image,
        item="lanzaguisantes",
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

    def update(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.clicked = True
                pygame.mixer.Sound(
                    "assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_seleccion.ogg"
                ).play()
            else:
                self.clicked = False


class Cortapasto(pygame.sprite.Sprite):
    cortapasto_id = 0

    def __init__(self, x, y, lista):
        self.image = pygame.image.load("assets\cortapasto\cortapasto.png")
        self.rect = self.image.get_rect(topleft=[x, y])
        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height - 60)
        self.hitbox.center = self.rect.center
        self.moving = False
        Cortapasto.cortapasto_id += 1
        self.id = Cortapasto.cortapasto_id
        self.cortapastos_col = lista
        super().__init__()

    def update(self):
        for zombies in grupo_zombies:
            if self.moving == 0 and self.hitbox.colliderect(zombies.hitbox):
                self.moving = True
                pygame.mixer.Sound("assets\cortapasto\cortapastos_activa.ogg").play()
            elif self.moving == 1 and self.hitbox.colliderect(zombies.hitbox):
                zombies.kill()
        if self.moving == True:
            self.rect.x += 10
            self.hitbox.center = self.rect.center
        if self.rect.x >= constantes.FIN_PASTO_X:
            eliminar(self.cortapastos_col, self.id)
            self.kill()



class Pala(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.image.load(r"assets\pala\pala_icono.jpg")
        self.x = 860
        self.y = 10
        self.rect = self.image.get_rect(topleft = [self.x, self.y])
        self.clicked = False
        self.sonido = pygame.mixer.Sound(r"assets\pala\pala_sonido.mp3")
        self.cursor = pygame.image.load(r"assets\pala\pala_cursor.png")
        super().__init__()

    def update(self, evento):
        if self.rect.collidepoint(evento.pos):
            self.clicked = True
            self.sonido.play()
        else:
            self.clicked = False

    def dibujar_cursor(self, x,y,screen):
        self.cursor_rect = self.cursor.get_rect(bottomleft = [x, y])
        screen.blit(self.cursor, self.cursor_rect)