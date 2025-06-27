# Plantas-vs-Zombies

El siguiente proyecto se basa en la recreación del juego conocido como Plantas vs Zombies. El trabajo surgió sobre la entrega final de la materia Pensamiento Computacional de la Universidad de San Andrés acompañado del propósito y entusiasmo de los estudiantes. Acontinuación, nuestro desarrollo:

## Tabla de contenidos:
###   -Descripción general
###   -Estructura/características del juego
###   -Cómo jugar
###   -Estructura del código
###   -Tecnologias utilizadas
###   -Agradecimientos
###   -Coders

## Descripción general

-El programa se basa en Plantas-vs-Zombies. Es un juego de estrategia tipo tower defense donde el objetivo principal del jugador es defender su casa de una incesante horda de zombis utilizando un arsenal de
plantas con habilidades únicas. Deberá colocar estratégicamente sus plantas en el jardín para detener el avance de los zombis antes de que lleguen a su hogar y...  ¡se coman su cerebro! 

## Estructura/características del juego

  ### Recursos
  Al iniciar, el jugador dispone de 50 soles, los cuales servirán para la obtención de plantas para la defensa del jardín.
  
  ### Generación de soles
  Con el avance del tiempo, soles adicionales caerán del cielo. Recógelos para aumentar tu economía y desbloquear plantas más poderosas, cruciales para fortalecer tu defensa y evitar que los zombis cumplan su
  misión.
  
  ### Diversidad de plantas:
  
   #### Girasoles: 
  Producen soles adicionales cada cierto tiempo, es recomendable jugar con estas plantas para acelerar tu economía
   #### Lanzaguisantes:
  Son de las principales defensas del juego, disparan guisantes que producen daño a los zombies
   #### Huielaguizantes:
  Una variante del Lanzaguisantes que dispara guisantes congelados. Además de infligir daño, ralentiza significativamente el movimiento de los zombis, dándote más tiempo para reaccionar y atacar.
   #### Petacereza:
  Una planta explosiva de un solo uso que detona en un área pequeña, eliminando instantáneamente a múltiples zombis. Ideal para situaciones de emergencia o grupos densos de enemigos.
   #### Papapum:
  Una mina terrestre que requiere un tiempo para armarse bajo tierra. Una vez lista, explota al contacto con el primer zombi que la pisa, causando un gran daño en un área reducida. Útil para emboscadas tempranas.
   #### Nuez:
  Una planta defensiva con una alta resistencia. Sirve como una barrera impenetrable para los zombis, absorbiendo una gran cantidad de daño y protegiendo a tus plantas de ataque detrás de ella.

  ### Variedad de zombies - Prepárate para enfrentar diferentes tipos de zombis, cada uno con sus propias características de resistencia:
  
  #### Zombi Normal: 
  El enemigo básico. Es el primer obstáculo que encontrarás, con una resistencia estándar que lo hace vulnerable a la mayoría de tus ataques.

  #### Zombi con Cono: 
  Ligeramente más resistente que el zombi normal gracias a su casco de cono. Requiere un poco más de potencia de fuego para ser derrotado.

  #### Zombi con Balde: 
  ¡Cuidado con este! Equipado con un balde metálico en su cabeza, es el zombi más resistente de los tres. Necesitarás concentrar una buena defensa!

  ### Sistema de dificultad: 
  Los enemigos aparecen en niveles de dificultad, aumentando progresivamente en numero a medida que avanza el tiempo

  ### Condiciones de victoria/derrota:
  El juego termina si un zombie llega a tu casa luego de haber pasado por las cortapastos. Y en cuanto al la victoria...! Nunca termina ! Mientras más niveles de dificultad subas, más crack serás!!

## Cómo jugar
  ¡Prepararse para la batalla es sencillo! Sigue los siguientes pasos para disfrutar del juego!

  ### Requisitos y configuracion inicial
  Antes de empezar, verifica que tienes instalado una versión de python versión 3.10.0 o superior. Si aún no lo tienes, puedes descargarlo desde la web oficial de python

  - Nuestro juego utiliza la librería Pygame, si no la tienes instalada, abre la terminal (o linea de comandos) y ejecuta el siguiente comando: pip install pygame
     
 # IMPORTACION COMPLETAR

  ### Controles y Mecánicas básicas
  Al iniciar el juego, te encotrarás con la interfaz, clickea el botón de PLAY y dile al loco Dave que puedes salvar el jardím! Luego, te encontrarás el jardín listo para empezar a plantar y armar tu defensa!

   #### Recolectar soles:
   Los soles caen cada cierto tiempo, es muy recomendable recogerlos para aumentar tu economía de soles , para ello, solamente debes hacer click izquierdo sobre ellos ¡Son la principal fuente para conseguir las
   plantas!

   #### Compra de plantas:
   1) En la parte superior de la pantalla, te encontrarás la barra con las platnas disponibles. Cada una mostrará su costo en soles.
   2) Si tienes soles suficientes, haz click izquierdo sobre la planta que quieras colocar en el jardín (por ejemploÑ el lanzaguisantes o el girasol), la planta quedará seleccionada.
   3) Mueve el cursor (el mouse) sobre tu jardín y te aparecerá el contorno de la planta. Luego, haz click izquierdo sobre la cuadrilla deseada (dentro del jardín) para colocar la defensa. Cuando realizes esta      acción, se te descontarán los soles del costo de la planta que usaste.
   4) Ahora, la imagen de la planta que colocaste aparecerá con un tono oscurecido, eso significa que empezó su Cooldown el cual es su tiempo de espera para volver a colocarla.

   #### Defensa automática:
   Una vez colocada la planta, ellas solas empezarán a cumplir su función. Asegúrate de seguir recolectando soles para seguír mejorando la defensa ¡No te olvides de tener en cuenta su cooldown!

   #### La pala:
   Es una herramienta útil para remover las plantas que colocaste en tu jardín (por si te equivocaste) pero ten en cuenta que no te devolverá los soles del costo de la planta.

   #### Objetivo del juego:
   El objetivo es evitar que los zombis lleguen al lado izquierdo de la pantalla, donde se encuentra tu casa. Si un zombi la alcanza, ¡habrás perdido la batalla! Sobrevive a los niveles que más puedas!
   
   
   
   


    


