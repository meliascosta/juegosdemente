Estas instrucciones son para agregar uno de los juegos existentes al servidor.
No son instrucciones de como crear juegos, sino de como instalarlos una vez creados

# Ejemplo para agregar el juego "control" #

### 1) Verificar que exista la carpeta static/games/control ###


### 2) Loguearse a http://localhost:8080/ con un usuario administrador ###


### 3) Abrir la dirección: http://localhost:8080/admin/contributable_games/game/add/ ###


### 4) Completar los campos de registro ###
**nombre:** control

**title:** CONTROL

**description:** `Este es un juego de velocidad, debes responder lo más rápido que puedas pero sin equivocarte. La letra L indica derecha y la letra A, izquierda. Si el avión es amarillo, tienes que indicar a qué lado apunta; si el avión es naranja, debes indicar el lado opuesto al cual apunta. Si los aviones están dados vuelta, debes indicar la dirección opuesta a la que seleccionarías si estuvieran derechos. ¡Es muy difícil!`

**instructions:** `Este es un juego de velocidad pero también de precisión: gana el que logra responder lo más rápido posible, y correctamente, la mayor cantidad de veces. En este juego aparecerá un avión en la pantalla y deberás presionar una tecla según qué dirección está indicando. La dirección derecha la elegirás presionando la letra L y la izquierda, la letra A. Después de cada elección la pantalla te indicará si ésta ha sido correcta o no y tendrás un nuevo avión para jugar. Luego de cierta cantidad de decisiones correctas ganarás un checkpoint (un checkpoint es un puntaje seguro, que ya no puede perderse, y se representa por un dibujo distinto en la barra de puntuación). Pero debes tener cuidado, porque sólo una decisión incorrecta hará que pierdas los últimos puntos y que desciendas al checkpoint anterior. Tres errores en un mismo checkpoint indican el final de esa partida. Entonces, aparecerá un avión en pantalla y deberás decidir, lo más rápido que puedas y sin equivocarte, qué dirección está indicando. Hasta aquí parece sencillo, ¡pero no lo es! Existen cuatro tipos de aviones: comenzarás con uno y a medida que vayas jugando mejor irán agregándose más posibilidades. Si aparece un avión amarillo, debes presionar la tecla de la dirección a la cual apunta. En cambio, si el que aparece es un avión naranja, debes presionar la tecla de la dirección opuesta a la cual apunta. Los mismos aviones pueden aparecer también dados vuelta (“patas para arriba”), en ese caso deberás presionar la tecla opuesta a la tecla que deberías presionar si el avión estuviese derecho. Como puedes ver, el juego se hace cada vez más complicado, ¡pruébalo! El reloj central indica el tiempo que tienes para tomar cada decisión, si da una vuelta completa, has perdido esa pantalla. El tiempo total de juego lo marca la barra verde inferior, que avanza a medida que juegas y, si no has cometido demasiados errores, cuando llega al final de la pantalla indica que la partida ha terminado. Cuanto más rápido y mejor juegues llegarás más lejos y sumarás más puntos. ¡A practicar! Al final de tu juego, aparecerá en pantalla el puntaje alcanzado y el ranking con las mejores posiciones. Sólo los usuarios registrados pueden aparecer en el ranking de las mejores puntuaciones, ¡regístrate!`


### 5) Hacer click en Grabar ###

### 6) Ir a http://localhost:8080/ ###

### 7) Hacer click en jugar (nos debería llevar a http://localhost:8080/login_to_game/control/ ) ###
Y disfrutar, ;)