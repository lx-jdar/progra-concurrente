# Proyecto: Caballo de Ajedrez

Se trata de un juego basado en el Ajedrez y, una de sus piezas, el caballo. El juego consiste en intentar recorrer todas las casillas de un tablero de Ajedrez con un caballo, que respeta el movimiento del juego en el cual se basa, y sin repetir casillas. La finalidad de este Software es el entretenimiento.

Se utilizó el lenguaje de programación Python, y el framework Pygame para renderizar la gráfica del juego y detectar los eventos que acciona el jugador. 

Para llevar a cabo la gestion de presentación en pantalla, el juego utiliza 8 hilos para la actualización de cada fila del tablero y un hilo que verifica si se ha ganado o perdido el juego. 

Para represnetar los objetos del juego, se lleva a cabo de dos clases, la clase Tablero que tiene la responsabilidad de llevar registro del estado de todas las casillas y de actualizar el tablero y como complemento una clase Caballo en el cual se realiza la logica de mover la pieza caballo y determinar los movimientos posibles que puede hacer dentro del tablero, como siguiente movimiento o retroceder a pasos anteriores para elegir otro camino.

## Instrucciones del juego "Caballo de Ajedrez"

### Objetivo

El objetivo del juego es pasar por todas las casillas de un tablero de ajedrez (8x8) con el caballo. Si no pasas por todas las ubicaciones, pierdes.


### Manual de usuario:
Botones:
+ Click izquierdo: Selecciona una casilla a moverte.
+ "R": Comienza de nuevo el juego.
+ "Z": Deshace un movimiento.
+ "Y": Vuelve a realizar un movimiento deshecho.
+ "Escape" o click en X : Sale del juego.

### Jugando el juego
+ Haz click en cualquier casilla donde desees moverte con el caballo para iniciar el juego.
+ Selecciona alguna de las casillas disponibles para que el caballo se mueva (NOTA: El caballo solo puede moverse en forma de L)
+ Si el caballo no puede moverse a ninguna casilla adyacente, pierdes el juego.

### Conclusiones:
En resumen, podemos decir que al utilizar threads hay que tener en cuenta dos puntos importantes, uno de ellos es la sincronización y comunicación, si no se realiza correctamente, puede llegar a generar errores inesperados, como puede ser que se trabe el juego o se cierre de la nada. 

La mayoría de los problemas que tuvimos fueron de este tipo, por ejemplo, descubrimos que el display solo puede ser instanciado y actualizado por el thread principal, por lo tanto debemos hacerlo en el main; otro problema fue a la hora de cerrar todos los hilos, estábamos intentando cerrar todos los hilos desde un hilo secundario, pero nos decantamos en utilizar un semáforo que le avise al hilo principal que debe terminar la ejecución.

Una mejora que consideramos que se podría implementar a la hora de actualizar las “cruces” (lugares donde ya paso el caballo), en vez de utilizar un hilo por cada fila del tablero, podríamos haber utilizado la GPU con la librería pycuda, enviando todos los casilleros en paralelo, evitando el uso de los for. 

En general, el proyecto fue inspirado en los conceptos vistos en la clase a la hora de desarrollar el juego, nos pareció entretenido hacer el desarrollo basado en las tecnologías y lenguajes aprendidos en clase, aparte de lo divertido que es jugar un juego de ingenio desarrollado por nosotros.



 
