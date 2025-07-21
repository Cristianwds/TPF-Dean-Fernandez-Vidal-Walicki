# TPF Dean - Fernandez - Vidal - Walicki

## Reporte

### **General**

Los códigos demuestran un excelente nivel de dominio técnico, pero podría beneficiarse de una mayor claridad estructural. Si bien la modularización en archivos separados es un acierto, la lógica en algunos módulos (especialmente en `main.py`) está demasiado acoplada y extensa, lo que dificulta la legibilidad y el mantenimiento a largo plazo. Sería ideal dividir tareas en funciones más pequeñas, usar comentarios más explicativos y seguir convenciones de documentación para facilitar la comprensión por terceros (en este caso lo atiende el docente pero a futuro lo va a tomar alguien que quizas no esté acostumbado a cómo codifican las cosas). Los nombres de las clases y variables son en su mayoría claros, aunque algunas estructuras podrían estandarizarse con un estilo más consistente (por ejemplo, __snake_case__ o __camelCase__). **Un punto negativo importante es el uso de rutas absolutas y específicas para sistemas Windows**, lo cual rompe la portabilidad del proyecto. En un entorno académico, se espera que los programas sean multiplataforma o que, al menos, se especifique en el README si están pensados exclusivamente para un sistema operativo.

Por otro lado, el repositorio está bien organizado y estructurado en cuanto a la separación de módulos, imágenes y sonidos, lo que facilita navegar por los recursos del proyecto. Sin embargo, se extraña un `README.md` más técnico que incluya instrucciones claras de instalación, requerimientos (por ejemplo, versión de Python o dependencias como `pygame`) y posibles advertencias sobre compatibilidad del sistema. También sería valioso incorporar un archivo `requirements.txt`. Aunque los nombres de los archivos son apropiados, se recomienda evitar el uso de acentos o espacios en blanco, especialmente si el objetivo es compatibilidad multiplataforma.

**Puntos positivos:**

* Excelente nivel de complejidad, muy cercana al juego original.
* Modularización fácil de reconocer: todos los archivos están separados por función específica (`main.py`, `funciones`, `pantallas`, `clases`, `sonido`, etc.).
* El `README.md` es completo, con instrucciones claras y detalles técnicos.
* Se nota un enorme esfuerzo y nivel de conocimiento en programación orientada a objetos, animaciones, colisiones y gestión de estados. Excelente trabajo con las animaciones y cómo aplicaron la pofunda investigación de la librería.

**Aspectos a mejorar:**

* El juego tiene una base tan extensa que, sin una guía clara en el código (por ejemplo, más docstrings o un esquema visual del flujo), puede ser difícil de mantener por otros.
* Algunos archivos (`main.py`) podrían subdividirse aún más en controladores específicos. Se pueden realizar tranquilamente más modificaciones y códigos distintos que tomen partes concretas.

**Recomendaciones:**

* Incluir un `requirements.txt` o al menos una línea sobre la versión de `pygame` utilizada.
* Sugerencia menor: agregar mensajes de ayuda in-game (por ejemplo, si no tenés soles suficientes).

---

### **Backend**

**Puntos positivos:**

* Uso avanzado de herencia para plantas y zombis. Gran uso de los conceptos vistos en clases y clara muestra del entendimiento que tuvieron al respecto.
* Integración perfecta entre clases de proyectiles, criaturas, objetos especiales y eventos.
* El sistema de cooldown por planta es completo y tiene feedback visual, funcional y técnico.
* Se manejan múltiples estados dentro de objetos complejos como `Papapum` o `Petacereza` con animaciones y efectos diferenciados.
* Excelente trabajo con el sistema de dificultad. Muy oiginal y bien ejecutado (también muy desafiante).

**Aspectos a mejorar:**

* Algunas lógicas están acopladas al main (por ejemplo, las decisiones de qué planta plantar están demasiado cerca del `event loop`).
* No se utiliza aún tipado fuerte en todas las funciones (aunque algunas sí lo hacen).
* Un error me sacó del juego en numeroas ocasiones:

``` bash
"/TPF-Dean-Fernandez-Vidal-Walicki/inicializacion.py", line 279, in creacion_zombies
    constantes.contador_nv_balde += 1
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'constantes' has no attribute 'contador_nv_balde'

-- OTRO ERROR --

File "/TPF-Dean-Fernandez-Vidal-Walicki/inicializacion.py", line 276, in creacion_zombies
    ubi2 = lista_ubis.pop(random.choice(lista_ubis))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IndexError: pop index out of range
```

**Recomendaciones:**

* Delegar completamente la lógica de cada clase en sus métodos (`zombie.atacar()`, `papapum.detectar_colisión()`), haciendo el `main` más limpio.
* Reducir el cooldown de la nuez!!!!
* Siempre prueben **MUY BIEN Y MUCHAS VECES**  su código antes de mandarlo.

---

### **Frontend**

**Puntos positivos:**

* Buen trabajo con las animaciones variadas en todas las entidades.
* Inclusión de efectos de ralentización (con animaciones distintas) y múltiples tipos de interacción.
* Previsualización clara de ubicación y planta seleccionada.
* La interfaz tiene un sistema muy bien hecho, incluyendo sombras de cooldown y sonido por selección.

**Aspectos a mejorar:**

* No hay mensajes visibles para el usuario cuando intenta plantar sin soles suficientes o en una celda ocupada.

**Recomendaciones:**

* Agregar un cartel intermedio de “Game Over” antes de cerrar o un botón para reiniciar.
* Mostrar el nombre y costo de la planta al pasar el mouse por las semillas (como un tooltip).

---

### **Extras**

**Puntos positivos:**

* Implementación del personaje de Dave con diálogo aleatorio y su propia pantalla.
* Petacereza y Papapum son recreaciones funcionales fieles, con múltiples animaciones y lógica muy bien elaborada.
* Sistema de sonido complejo: con control de canales, evitación de superposición, y uso específico de sonidos para cada entidad.
* Cortapastos funcionales, incluyendo activación por fila.
* Gran cantidad de animaciones por entidad (frames múltiples, ralentizaciones, muerte, explosión, etc.).

**Aspectos a mejorar:**

* Solo falta una pantalla de créditos o reinicio para cerrar la experiencia redonda.

**Recomendaciones:**

* Considerar agregar una tabla de puntuación, niveles, o progresión entre partidas si quisieran expandir.
