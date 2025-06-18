import pygame
import constantes
import random
from pygame import mixer
import funciones

grupo_plantas = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
grupo_zombies = pygame.sprite.Group()
grupo_cortapastos = pygame.sprite.Group()
grupo_semillas = pygame.sprite.Group()
grupo_pala = pygame.sprite.Group()
grupo_deplegables = pygame.sprite.Group()
grupo_sol = pygame.sprite.Group()
class Administrador_de_sonido():

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)
        self.sonidos = {}
        self.canales_sonidos_ocupados = {}#Aca se guarda el nombre del sonido y su canal nada mas cuando se ejecuta reproducir_sonido con evitar_superposicion = True
    
    def cargar_sonido(self, ruta_sonido:str, nombre_sonido:str):
        try:
            sonido = pygame.mixer.Sound(ruta_sonido)
            self.sonidos[nombre_sonido] = sonido
        except pygame.error as error:
            print(f"Error al cargar el sonido {nombre_sonido}\nRuta: {ruta_sonido}\nError: {error}")


    def reproducir_sonido(self, nombre_sonido:str, loop = 0, evitar_superposicion = False):

        if nombre_sonido in self.sonidos:
            if evitar_superposicion:
                if nombre_sonido in self.canales_sonidos_ocupados:
                    #Si el canal que se le asigno al sonido está reproduciendo, el método finaliza.
                    canal = self.canales_sonidos_ocupados[nombre_sonido]
                    if canal.get_busy():
                        return
                    #Si no está asignado a un canal, se le asigna uno.
                else:
                    canal = pygame.mixer.find_channel()
                    self.canales_sonidos_ocupados[nombre_sonido] = canal
                if canal:
                    canal.play(self.sonidos[nombre_sonido], loops = loop)
            else:
                self.sonidos[nombre_sonido].play(loops = loop)
        else:
            print(f"Sonido {nombre_sonido} no encontrado.")


    def detener_reproduccion(self, nombre_sonido:str):
        if nombre_sonido in self.canales_sonidos_ocupados:
            self.canales_sonidos_ocupados[nombre_sonido].stop()
            del self.canales_sonidos_ocupados[nombre_sonido]
        elif nombre_sonido in self.sonidos:
            self.sonidos[nombre_sonido].stop()

    def detener_todos(self):
        pygame.mixer.stop()

        
class Criaturas(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, vida, reproductor_de_sonido):
        super().__init__()
        self.pos_x = x
        self.pos_y = y
        self.image = imagen  # Si ya es una Surface
        self.rect = self.image.get_rect(center=[self.pos_x, self.pos_y])
        self.vida = vida
        self.reproductor_de_sonido = reproductor_de_sonido
        
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            self.kill()
            return True

class Enemigos(Criaturas):
    def __init__(self, x, y, tipo, vida, reproductor_de_sonido, daño= constantes.DAÑO_ZOMBIE, velocidad= constantes.VELOCIDAD_ZOMBIE):
        
        # Se cargan los frames
        self.tipo = tipo
        self.frames_caminata = [pygame.image.load(f"assets/zombies/{self.tipo}/caminata/frame_{i}.png").convert_alpha() for i in range(constantes.Cant_frames[self.tipo][0])]
        self.frames_ataque = [pygame.image.load(f"assets/zombies/{self.tipo}/ataque/frame_{i}.png").convert_alpha() for i in range (constantes.Cant_frames[self.tipo][1])] # Por ahora tiene las mismas img de movimiento
        self.frames_caminatahielo = [pygame.image.load(f"assets/zombies/{self.tipo}/caminatahielo/frame_{i}.png").convert_alpha() for i in range(constantes.Cant_frames[self.tipo][0])]
        self.frames_ataquehielo = [pygame.image.load(f"assets/zombies/{self.tipo}/ataquehielo/frame_{i}.png").convert_alpha() for i in range (constantes.Cant_frames[self.tipo][1])]

        self.estado= "caminar" # caminar o atacar
        self.frames= self.frames_caminata
        imagen_inicial = self.frames[0]

        # Se llama a la Superclase con la imagen cargada
        super().__init__(x, y, imagen_inicial, vida, reproductor_de_sonido)

        self.velocidad = velocidad
        self.daño = daño
        self.pos_x = float(x)
        self.pos_y = y
        self.indice_frame = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.ultimo_ataque = pygame.time.get_ticks()
        self.velocidad_animacion = constantes.VEL_ANIM_ZOMBIE
        #self.image = pygame.transform.scale(self.image, (120, 140))  # opcional

        self.realentizado = False
        self.tiemporealentizado = pygame.time.get_ticks()

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
                    self.reproductor_de_sonido.reproducir_sonido("zombie_masticar", -1, True)
                    if planta.recibir_daño(self.daño):
                        self.velocidad = constantes.VELOCIDAD_ZOMBIE
            
        if atacando == True and len(grupo_plantas) == 0:
            atacando = False
            self.velocidad = constantes.VELOCIDAD_ZOMBIE

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

        if self.realentizado:
            ahora = pygame.time.get_ticks()
            self.velocidad = 0.08
            self.velocidad_animacion = 45
            if self.estado == "caminar":
                self.frames = self.frames_caminatahielo
            elif self.estado == "atacar":
                self.frames = self.frames_ataquehielo
            if ahora - self.tiemporealentizado > 3000:
                self.realentizado = False
                self.velocidad = constantes.VELOCIDAD_ZOMBIE
                self.velocidad_animacion = constantes.VEL_ANIM_ZOMBIE
                if self.estado == "caminar":
                    self.frames = self.frames_caminata
                elif self.estado == "atacar":
                    self.frames = self.frames_ataque


        if atacando:
            if self.estado != "atacar":
                self.estado = "atacar"
                if not self.realentizado:
                    self.frames = self.frames_ataque
                else:
                    self.frames = self.frames_ataquehielo
                self.indice_frame = 0
        else:
            if self.estado != "caminar":
                self.estado = "caminar"
                if not self.realentizado:
                    self.frames = self.frames_caminata
                else:
                    self.frames = self.frames_caminatahielo
                self.indice_frame = 0
            self.velocidad = constantes.VELOCIDAD_ZOMBIE
            self.pos_x -= self.velocidad
            if self.pos_x <= 0:
                self.kill()

        # DEBUG: dibujar hitbox
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            if self.estado == "atacar":
                self.reproductor_de_sonido.detener_reproduccion("zombie_masticar")
            self.kill()


class Plantas(Criaturas):
    plantas_id = 0
    def __init__(self, x, y, imagen, vida, cooldown, costo, lista_entidades, reproductor_de_sonido):
        super().__init__(x, y, imagen, vida, reproductor_de_sonido)
        self.cooldown = cooldown
        self.costo = costo
        self.pos_x = x
        self.pos_y = y

        # El rect sigue siendo para dibujar la imagen
        self.rect = self.image.get_rect(midleft=(self.pos_x, self.pos_y))
        
        # Hitbox separada: más pequeña, para colisiones
        self.hitbox = pygame.Rect(0, 0, self.rect.width - 50, self.rect.height - 60)
        self.hitbox.midbottom = self.rect.midbottom
        self.hitbox.y -= 20
        self.lista_entidades = lista_entidades
        Plantas.plantas_id += 1
        self.id = Plantas.plantas_id

    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            funciones.eliminar(self.lista_entidades, self.id, Plantas)
            self.reproductor_de_sonido.detener_reproduccion("zombie_masticar")
            self.reproductor_de_sonido.reproducir_sonido("zombie_tragar")
            self.kill()
            return True

class lanzaguisantes(Plantas):
    def __init__(self, x, y, lista_entidades, reproductor_de_sonido, costo=100, hielo = False, vida=300, cooldown=7500):
        if hielo == False:
            self.frames = [pygame.image.load(f"assets\lanzaguisante\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["lanzaguisante"])]
        else:
            self.frames = [pygame.image.load(f"assets\hielaguisante\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["hielaguisantes"])]
        self.hielo = hielo
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
        self.velocidad_animacion = constantes.VEL_ANIM_LG[hielo]  # milisegundos por frame
        self.rect = self.image.get_rect(midleft= (x,y))
        Plantas.__init__(self, x, y, self.image, vida, cooldown, costo, lista_entidades, reproductor_de_sonido)

    def update(self):
        global grupo_zombies
        ahora = pygame.time.get_ticks()
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]

        # Chequear si hay zombies en el mismo carril y delante de la planta
        hay_zombie_en_frente = False
        for zombie in grupo_zombies:
            mismo_carril = abs(zombie.hitbox.centery - self.hitbox.centery) < 50
            esta_adelante = zombie.hitbox.x >= self.hitbox.x and zombie.hitbox.x <= constantes.ANCHO_VENTANA - 27
            if mismo_carril and esta_adelante:
                hay_zombie_en_frente = True
                break

        if hay_zombie_en_frente and ((ahora - self.ultimo_disparo) >= 1500):
            self.ultimo_disparo = ahora
            if self.hielo:
                guisante = Proyectil(r"assets\\proyectil\\guisantehielo.png", self.hitbox.x + 110, self.hitbox.y + 18, 20, self.reproductor_de_sonido, True)
            else:
                guisante = Proyectil(r"assets\\proyectil\\guisante.png", self.hitbox.x + 60, self.hitbox.y, 20, self.reproductor_de_sonido)
            grupo_proyectiles.add(guisante)


class Girasol(Plantas):
    def __init__(self, x, y, lista_entidades, reproductor_de_sonido, vida=300, cooldown=7500, costo=50):
        self.x = x +12
        self.y = y +12
        self.vida = vida
        self.frames = [pygame.image.load(f"assets\girasol\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["girasol"])]
        self.indice_frames = 0
        self.image = self.frames[self.indice_frames]
        self.cooldown = cooldown
        self.costo = costo
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion = 18
        self.rect = self.image.get_rect(midleft=(self.x, self.y))
        super().__init__(self.x, self.y, self.image, vida, cooldown, costo, lista_entidades, reproductor_de_sonido)
        self.creacion = pygame.time.get_ticks()
        self.contador = 0
        self.tiempo_ultimo_sol = pygame.time.get_ticks()
        self.intervalo_soles = 23000  # 23 segundos en milisegundos

    def update(self):
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_sol > self.intervalo_soles:
            self.tiempo_ultimo_sol = ahora
            nuevo_sol = Sol(self.rect.x + 20, self.rect.y, self.rect.y)
            return nuevo_sol
        return None


class Nuez(Plantas):
    def __init__(self, x, y, lista_entidades, reproductor_de_sonido, vida=4000, cooldown=30000, costo=50):
        self.x = x
        self.y = y
        self.vida = vida
        self.cooldown = cooldown
        self.costo = costo
        self.frames = [pygame.image.load(f"assets\\nuez\\frame_{i}.png").convert_alpha() for i in range(constantes.CANT_FRAMES_PLANTAS["nuez"])]
        self.indice_frames = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion= 50
        self.image = self.frames[self.indice_frames]
        self.rect = self.image.get_rect(midleft=(self.x, self.y))
        super().__init__(self.x + 17, self.y+ 17, self.image, vida, cooldown, costo, lista_entidades, reproductor_de_sonido)

    def update(self):
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]


class Papapum(Plantas):
    def __init__(self, x, y,lista_entidades, reproductor_de_sonido, vida= 300, cooldown = 8000, costo = 25):
        self.x = x
        self.y = y
        self.vida = vida
        self.cooldown = cooldown
        self.costo = costo
        self.frames_activados = [pygame.image.load(f"assets\\papapum\\papapum_activado\\frame_{i}.png").convert_alpha() for i in range(28)]
        self.frames_desactivados = [pygame.image.load(f"assets\\papapum\\papapum_desactivado\\frame_{i}.png").convert_alpha() for i in range(24)]
        self.frames_explosion = [pygame.image.load(f"assets\\papapum\\papapum_explosion\\frame_{i}.png").convert_alpha() for i in range(26)]
        self.estado = "desactivado"
        self.contador_activacion = 0
        self.frame_desactivado_contador = 0
        self.frame_explosion_contador = 0
        self.indice_frames = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion= 20
        self.image = self.frames_desactivados[self.indice_frames]
        self.rect = self.image.get_rect(midleft=(self.x, self.y))
        super().__init__(x, y, self.image, vida, cooldown, costo, lista_entidades, reproductor_de_sonido)

    def activar_hitbox(self):
        self.hitbox_activacion = pygame.Rect(0, 0, constantes.CELDA_ANCHO // 2, constantes.CELDA_ALTO // 2)
        self.hitbox_explosion = pygame.Rect(0, 0, constantes.CELDA_ANCHO, constantes.CELDA_ALTO)
        self.hitbox_activacion.center = self.rect.center
        self.hitbox_explosion.center = self.rect.center

    def explotar(self):
        self.reproductor_de_sonido.reproducir_sonido("petacereza_explosion", 0)
        for zombie in grupo_zombies:
            if self.hitbox_explosion.colliderect(zombie.hitbox):
                zombie.recibir_daño(10000)
        
    def cambiar_animacion(self, animacion):
        if animacion == "activado":
            self.activar_hitbox()
            self.estado = "activado"
        else:
            self.estado ="explosion"
            self.explotar()

    def update(self):
        tiempo_frame= pygame.time.get_ticks()
        if self.estado == "desactivado":
            if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
                self.contador_activacion += 1
                if self.frame_desactivado_contador < 23:
                    self.frame_desactivado_contador += 1
                    self.ultimo_frame = tiempo_frame
                    self.indice_frames = (self.indice_frames + 1) % len(self.frames_desactivados)
                    self.image = self.frames_desactivados[self.indice_frames]
                    self.rect = self.image.get_rect(center = (self.x + constantes.CELDA_ANCHO / 2 + 10, self.y))
                if self.contador_activacion == 600:
                    self.cambiar_animacion("activado")
        elif self.estado == "activado":
            for zombie in grupo_zombies:
                if self.hitbox_activacion.colliderect(zombie.hitbox):
                    self.cambiar_animacion("explosion")
            if tiempo_frame - self.ultimo_frame > self.velocidad_animacion * 1.7:
                self.indice_frames = (self.indice_frames + 1) % len(self.frames_activados)
                self.image = self.frames_activados[self.indice_frames]
                self.ultimo_frame = tiempo_frame
                self.rect = self.image.get_rect(center = (self.x  + constantes.CELDA_ANCHO / 1.5,self.y + constantes.CELDA_ALTO / 4))
        else:
            self.indice_frames = 0 if self.frame_explosion_contador == 0 else tiempo_frame
            if tiempo_frame - self.ultimo_frame > 80:
                if self.frame_explosion_contador < 10:
                    self.frame_explosion_contador += 1
                    self.indice_frames = (self.indice_frames + 1) % len(self.frames_explosion)
                    self.image  = self.frames_explosion[self.indice_frames]
                    self.rect = self.image.get_rect(center = (self.x + constantes.CELDA_ANCHO / 1.5, self.y ))
                    self.ultimo_frame = tiempo_frame
            if self.frame_explosion_contador >= 10:
                funciones.eliminar(self.lista_entidades, self.id, Plantas)
class Petacereza(pygame.sprite.Sprite):
    petacerezas_id = 0
    def __init__(self, x, y, administrador_de_sonido, costo = 150):
        self.costo = costo
        self.x = x
        self.y = y
        self.image = pygame.image.load(r"assets\petacereza\gif\frame_0.png")
        self.administrador_de_sonido = administrador_de_sonido
        self.frames = [pygame.image.load(f"assets\\petacereza\\gif\\frame_{i}.png").convert_alpha() for i in range(7)]
        self.indice_frames = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion= 200
        self.image = self.frames[self.indice_frames]
        self.rect = self.image.get_rect(midleft=(x,y))
        Petacereza.petacerezas_id += 1
        self.id = Petacereza.petacerezas_id
        self.contador_explosion = 0
        self.hitbox_explosion = pygame.Rect(0, 0, constantes.CELDA_ANCHO * 3, constantes.CELDA_ALTO * 3)
        self.hitbox_explosion.center = self.rect.center
        self.alpha = 256
        super().__init__()

    def update(self, grilla_entidades):
        tiempo_frame= pygame.time.get_ticks()

        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            if self.contador_explosion < 6:
                self.image = self.frames[self.indice_frames]
            self.contador_explosion += 1
        if self.contador_explosion == 6:
            self.image = pygame.image.load(r"assets\petacereza\petacereza_explosion_imagen.png")
            self.rect = self.image.get_rect(center = (self.x + constantes.CELDA_ANCHO / 2, self.y))
            self.administrador_de_sonido.reproducir_sonido("petacereza_explosion", 0, False)
            for zombie in grupo_zombies:
                if self.hitbox_explosion.colliderect(zombie.hitbox):
                    zombie.recibir_daño(10000)
            self.contador_explosion += 1          
        if self.contador_explosion >= 7:
            self.image.set_alpha(self.alpha)
            self.alpha -= 3
            if self.contador_explosion == 13:
                funciones.eliminar(grilla_entidades, self.id, Petacereza)



class Proyectil(pygame.sprite.Sprite):

    def __init__(self,imagen,x,y,daño,administrador_de_sonido, hielo = False):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(imagen).convert_alpha()
        self.daño = daño
        self.hielo = hielo
        self.administrador_de_sonido = administrador_de_sonido

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
                self.administrador_de_sonido.reproducir_sonido(random.choice(["hit1", "hit2", "hit3"]))
                zombie.recibir_daño(self.daño)
                if self.hielo:
                    zombie.realentizado = True
                    zombie.tiemporealentizado = pygame.time.get_ticks()
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
    
class Sol(pygame.sprite.Sprite):
    def __init__(self, x, y, alturas_sol, velocidad = constantes.VELOCIDAD_SOL):#aparicion = constantes.TIEMPO_APARICION_SOL = 7500)
        pygame.sprite.Sprite.__init__(self) 
        self.frames = [pygame.image.load(f"assets\\sol\\frame_{i}.png").convert_alpha() for i in range(30)]
        self.indice_frames = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.velocidad_animacion = 10
        self.image = self.frames[self.indice_frames]
        self.velocidad = velocidad
        self.pos_x = x
        self.pos_y = y 
        self.rect = self.image.get_rect()
        self.rect.x = float(x)
        self.rect.y = float(y)  
        self.altura = alturas_sol
        self.creacion = pygame.time.get_ticks() # Para evaluar el tiempo desde la creación

    # Animacion
    
    def update(self):
        if self.pos_y < self.altura:
            self.pos_y += self.velocidad
            self.rect.center = (self.pos_x, self.pos_y) # Para que se actualize la ubiacion del rectagnulo del sol
        tiempo_frame= pygame.time.get_ticks()                   
        if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            self.image = self.frames[self.indice_frames]
        tiempo_muerte = pygame.time.get_ticks() # Tiempo actual antes de ejecutarse la accion
        if tiempo_muerte - self.creacion > 11000: 
            self.kill()

    def recolectar (self):
        self.kill()    
        return constantes.VALOR_SOL