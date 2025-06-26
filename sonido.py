import pygame

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

def iniciar_administrador_sonido():
    """
    Inicia el administrador de sonidos utilizado en todas las clases para la reproduccion.

    Para añadir nuevos sonidos esta el dict diccionario_sonidos, que se puede modificar a continuacion con el siguiente formato:
    diccionario_sonidos = {"nombre_sonido": "ruta_sonido"}

    Returns:
    ------
    administrador_de_sonido: es la variable con la clase Administrador_de_sonido, chequear en clases para ver su funcionamiento.
    """
    administrador_de_sonido = Administrador_de_sonido()
    diccionario_sonidos = {
        "musica_menu_principal": r"assets\Musica\[Main Menu].mp3",
        "musica_nivel_dia": r"assets\Musica\[Day Stage].mp3",
        "hit1": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit1.ogg",
        "hit2": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit2.mp3",
        "hit3": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\Hit3.ogg",
        "semilla_seleccionar": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_seleccion.ogg",
        "semilla_plantar": r"assets\Sonidos_Plantas\Lanzaguisantes\Guisante contra zombi\semillas\semillas_plantar.ogg",
        "zombie_masticar": r"assets\zombies\zombie_masticando.ogg",
        "zombie_tragar": r"assets\zombies\zombie_tragando_planta.ogg",
        "cortapastos_activar": r"assets\cortapasto\cortapastos_activa.ogg",
        "pala_sonido": r"assets\pala\pala_sonido.mp3",
        "petacereza_explosion": r"assets\petacereza\petacereza_explosion_sonido.ogg",
        "perder": r"assets\Musica\[You Lost].mp3",
        "botones": r"assets\boton_inicio.mp3",
        "recoger_sol": r"assets\Sonidos_Plantas\sol_recoleccion.mp3",
        "zombies_coming": r"assets\zombies\The Zombies Are coming Sound Effect.mp3",
        "webiwabo": r"assets\dave_el_hermoso\webiwabo.ogg",
        "ovawabodabawabaobadabowadaba": r"assets\dave_el_hermoso\ovawabodabawabaobadabowadaba.ogg",
        "bwadawbabadfbaw": r"assets\dave_el_hermoso\bwadawbabadfbaw.ogg",
        "budubuwedivadibo": r"assets\dave_el_hermoso\budubuwedivadibo.ogg",
    }
    for nombre_sonido, ruta_sonido in diccionario_sonidos.items():
        administrador_de_sonido.cargar_sonido(ruta_sonido, nombre_sonido)

    return administrador_de_sonido