Dado que se cuenta con información de las canciones se decide realizar un scatter plot para poder entregar mayores insights sobre la playlist generada.

- Se decide utilizar un scatter plot ya que solo se cuenta con 2 atributos y se pueden ver las características de las canciones como un todo. Adicionalmente scatter plots ofrecen variados elementos de interactividad.


- El gráfico contiene los 2 atributos que presentan las canciones: Duración en minutos en el eje X y Popularidad en el eje Y. Para este último se encuentran designados limites fijos entre 0 y 100 mientras duración (X) no cuenta con límites.


- Cada punto corresponde a un track distinto. Estos se representan como circulos verdes para complementar el diseño de la página. 


- Todos los circulos son del mismo color ya que dada la cantidad de grupos se tendrían demasiados colores diferentes y la gráfica se volvería desordenada y difícil de interpretar.


- Cada punto cuenta con información desplegable al pasar el mouse por sobre ellos. La información corresponde a:
  - Track (Canción)
  - Artist
  - Duration (minutes)
  - Popularity


- Se puede interactuar con el gráfico realizando click sobre los circulos, al hacer esto el gráfico se enfocará únicamente en las canciones que tengan el mismo autor (opacidad de los otros puntos disminuye).


- A su vez es posible buscar directamente grupos especificos si es deseado utilizando un dropdown menu que contiene a todos los artistas.


- Estos 2 filtros no se excluyen entre sí, es decir, para poder utlizar la funcionalidad de click, debe estar el dropdown situado en *All artists*


- El gráfico puede reiniciarse haciendo doble click sobre algún espacio vacio.


- El Dropdown menu se encuentra modificado utilizando CSS para tener una apariencia acorde al resto de la página.