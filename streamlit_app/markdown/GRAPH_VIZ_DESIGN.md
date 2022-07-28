Dado que el programa genera información de artistas relacionados entre sí resulta ideal graficar las relaciones mediante un grafo.

- Cada nodo del grafo representa a un artista donde el nodo central corresponde al `artista base` que fue utilizado como input de la query que genera la información.


- Los nodos se encuentran representados por el nombre de cada artista lo que permite visualizar de manera inmediata las relaciones.


- El layout del grafo corresponde a un layout de jerarquia circular. Esta decisión se debe a que al utilizar un layout tipo arbol existe un choque entre los nombres de los artistas, lo que disminuye la legibilidad y comprensión de la información. Adicionalmente se logra rerpesentar de forma clara el nodo central y queda en evidencia que mientras más alejados se encuentran los nodos del nodo inicial, menor es la relación con éste.


- Dado que el proposito original del programa era generar playlists de artistas relacionados, obtenemos también información de canciones relevantes de cada artista. Para agregar valor al grafo se agrega como funcionalidad interactiva el poder desplegar los nombres de las canciones al pasar el cursor sobre los nombres de los nodos.


- Al momento de crear el grafo se realizaron pruebas con todas las grandes librerias de Python que permiten realizar grafos interactivos (nx_altair, pyvis, bokeh y plotly). Finalmente se opta por bokeh al ser la más intuitiva para este caso de uso especifico, por permitir generar una toolbar personalizable con herramientas de interacción a elección y por compilarse a HTML lo que permite realizar personalizaciones más allá de lo permitido por la librería misma.


- Al grafo se le implementan las interacciones de wheel zooming, panning y hover junto a una adicional que permite reiniciar el grafo. Estos 3 atributos se encuentran activos por defecto pero pueden ser desactivados en el toolbar.

- Adicionalmente para simular una integración nativa con la página se vuelve el fondo transparente de la visualización, utilizando CSS se modifica el color del texto de la ventana al hacer hover, se elimina el logo de bokeh y adicionalmente se elimina el boton que permite hacer las visualizaciones full-screen ya que generalmente las visualizaciones amplificadas en streamlit presentan bugs y no dan acceso a todas las capacidades de los gráficos.