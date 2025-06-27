import pygame
import constantes
import random
from pygame import mixer
import funciones
import sonido

grupo_plantas = pygame.sprite.Group()
grupo_proyectiles = pygame.sprite.Group()
grupo_zombies = pygame.sprite.Group()

        
class Criaturas(pygame.sprite.Sprite):

    def __init__(self, x, y, imagen, vida, reproductor_de_sonido):
        """
            Clase base para todas las criaturas del juego (plantas y zombies).

            Inputs:
            -------
            x, y: coordenadas iniciales
            imagen: imagen inicial de la criatura
            vida: vida inicial
            reproductor_de_sonido: instancia de Administrador_de_sonido
        """
        super().__init__()
        self.pos_x = x
        self.pos_y = y
        self.image = imagen  # Si ya es una Surface
        self.rect = self.image.get_rect(center=[self.pos_x, self.pos_y])
        self.vida = vida
        self.reproductor_de_sonido = reproductor_de_sonido
        
    def recibir_daño(self, daño):
        """
        Resta vida a la criatura y la elimina si su vida llega a 0.

        Inputs:
        -------
        daño: cantidad de daño recibido

        Returns:
        -------
        bool: True si murió, False si sobrevivió
        """
        self.vida -= daño
        if self.vida <= 0:
            self.kill()
            return True

class Enemigos(Criaturas):
    def __init__(self, x, y, tipo, vida, reproductor_de_sonido, daño= constantes.DAÑO_ZOMBIE, velocidad= constantes.VELOCIDAD_ZOMBIE):
        """
        Clase para los enemigos del juego (zombies).

        Inputs:
        -------
        x, y: coordenadas iniciales
        tipo: tipo de zombie (normal, cono, balde)
        vida: vida inicial
        reproductor_de_sonido: instancia de Administrador_de_sonido
        daño: daño que inflige al atacar
        velocidad: velocidad de movimiento
        """
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
        """
        Actualiza el estado del zombie: animación, ataque, movimiento y efectos de ralentización.
        """
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
            ahora2 = pygame.time.get_ticks()
            self.velocidad = 0.05
            self.velocidad_animacion = 55
            if self.estado == "caminar":
                self.frames = self.frames_caminatahielo
            elif self.estado == "atacar":
                self.frames = self.frames_ataquehielo
            if ahora2 - self.tiemporealentizado > 3000:
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
                    if self.tipo == "cono":
                        self.velocidad_animacion = constantes.VEL_ANIM_ATQ_CONO
                else:
                    self.frames = self.frames_ataquehielo
                self.indice_frame = 0
        else:
            if self.estado != "caminar":
                self.estado = "caminar"
                if not self.realentizado:
                    self.frames = self.frames_caminata
                    self.velocidad_animacion = constantes.VEL_ANIM_ZOMBIE
                else:
                    self.frames = self.frames_caminatahielo
                self.indice_frame = 0
            self.velocidad = constantes.VELOCIDAD_ZOMBIE
            self.pos_x -= self.velocidad
            if self.pos_x <= 0:
                self.kill()

    def recibir_daño(self, daño):
        """
        Recibe daño y elimina al zombie si su vida llega a 0.
        Si estaba atacando, detiene el sonido de masticar.

        Inputs:
        -------
        daño: cantidad de daño recibido
        """
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
            nuevo_sol = Sol(self.rect.x + 20, self.rect.y, self.rect.y, self.reproductor_de_sonido)
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
        """
        El papapum tiene tres estados:
        desactivado: por 600 ticks el papapum esta desactivado y puede ser comido por el zombie.
        activado: el papapum esta activado, se le activa su hitbox de explosion y si colisiona contra un zombie explota.
        explosion: una vez el zombie colisiono con el papapum se les inflinge daño a los zombies en la hitbox, se cambia de animacion y se elimina el papapum.
        """
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
        """
        Activa una hitbox que si colisiona contra un zombie el papapum cambia de estado y explota
        """
        self.hitbox_activacion = pygame.Rect(0, 0, constantes.CELDA_ANCHO // 2, constantes.CELDA_ALTO // 2)
        self.hitbox_explosion = pygame.Rect(0, 0, constantes.CELDA_ANCHO, constantes.CELDA_ALTO)
        self.hitbox_activacion.center = self.rect.center
        self.hitbox_explosion.center = self.rect.center

    def explotar(self):
        """
        Reproduce el sonido de explosion y les inflinge el daño a los zombies.
        """
        self.reproductor_de_sonido.reproducir_sonido("petacereza_explosion", 0)
        for zombie in grupo_zombies:
            if self.hitbox_explosion.colliderect(zombie.hitbox):
                zombie.recibir_daño(10000)
        
    def cambiar_animacion(self, animacion):
        """
        Cambia entre estados del papapum
        """
        if animacion == "activado":
            self.activar_hitbox()
            self.estado = "activado"
        else:
            self.estado ="explosion"
            self.explotar()

    def update(self):
        """
        El papapum aparece en estado desactivado, despues de un tiempo cambia de estado a activado y en este estado se verificia que si hay una colision con un zombie explote.
        """
        tiempo_frame= pygame.time.get_ticks()
        if self.estado == "desactivado": #Cuando esta desactivado
            if tiempo_frame - self.ultimo_frame > self.velocidad_animacion:
                self.contador_activacion += 1 #Contador para el tiempo que pasa desactivado.
                if self.frame_desactivado_contador < 23: #Contador para que la animacion de spawn del papapum se reproduzca una sola vez
                    self.frame_desactivado_contador += 1
                    #Animacion:
                    self.ultimo_frame = tiempo_frame
                    self.indice_frames = (self.indice_frames + 1) % len(self.frames_desactivados)
                    self.image = self.frames_desactivados[self.indice_frames]
                    self.rect = self.image.get_rect(center = (self.x + constantes.CELDA_ANCHO / 2 + 10, self.y))
                if self.contador_activacion == 600:
                    self.cambiar_animacion("activado")
        elif self.estado == "activado": #Cuando esta activado
            for zombie in grupo_zombies:#Si colisiona con un zombie explota
                if self.hitbox_activacion.colliderect(zombie.hitbox):
                    self.cambiar_animacion("explosion")
                    #Animacion:
            if tiempo_frame - self.ultimo_frame > self.velocidad_animacion * 1.7:
                self.indice_frames = (self.indice_frames + 1) % len(self.frames_activados)
                self.image = self.frames_activados[self.indice_frames]
                self.ultimo_frame = tiempo_frame
                self.rect = self.image.get_rect(center = (self.x  + constantes.CELDA_ANCHO / 1.5,self.y + constantes.CELDA_ALTO / 4))
        else:
            #Cuando explotó
            self.indice_frames = 0 if self.frame_explosion_contador == 0 else tiempo_frame
            #Animacion
            if tiempo_frame - self.ultimo_frame > 80:
                if self.frame_explosion_contador < 10:
                    self.frame_explosion_contador += 1#Contador que se usa para cuando termina la animacion eliminar el papapum
                    self.indice_frames = (self.indice_frames + 1) % len(self.frames_explosion)
                    self.image  = self.frames_explosion[self.indice_frames]
                    self.rect = self.image.get_rect(center = (self.x + constantes.CELDA_ANCHO / 1.5, self.y ))
                    self.ultimo_frame = tiempo_frame
            if self.frame_explosion_contador >= 10: #Se elimina el papapum
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
            #Animacion:
            self.ultimo_frame = tiempo_frame
            self.indice_frames = (self.indice_frames + 1) % len(self.frames)
            if self.contador_explosion < 6:
                self.image = self.frames[self.indice_frames]
            self.contador_explosion += 1 #Contador que se utiliza para verificar cuando tiene que explotar la petacereza.
        if self.contador_explosion == 6:
            self.image = pygame.image.load(r"assets\petacereza\petacereza_explosion_imagen.png")
            self.rect = self.image.get_rect(center = (self.x + constantes.CELDA_ANCHO / 2, self.y))
            self.administrador_de_sonido.reproducir_sonido("petacereza_explosion", 0, False)
            for zombie in grupo_zombies:
                if self.hitbox_explosion.colliderect(zombie.hitbox):
                    zombie.recibir_daño(10000)
            self.contador_explosion += 1          
        if self.contador_explosion >= 7: #La imagen de explosion se va desvaneciendo
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

class Sol(pygame.sprite.Sprite):
    def __init__(self, x, y, alturas_sol,administrador_de_sonido, velocidad = constantes.VELOCIDAD_SOL):#aparicion = constantes.TIEMPO_APARICION_SOL = 7500)
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
        self.administrador_de_sonido = administrador_de_sonido

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
        self.administrador_de_sonido.reproducir_sonido("recoger_sol")
        self.kill()    
        return constantes.VALOR_SOL