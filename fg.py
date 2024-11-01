from blessed import Terminal
from rich.console import Console
from rich.panel import Panel
import time

# Inicializa `blessed` y `rich`
term = Terminal()
console = Console()

# Definir la matriz (puede ser de cualquier tamaño)
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Dimensiones de la matriz y el espaciado entre paneles
espacio_x = 12  # Ajuste horizontal (columna)
espacio_y = 4   # Ajuste vertical (fila)

# Función para imprimir toda la matriz con una celda móvil
def imprimir_matriz(matriz, celda_pos):
    for i, fila in enumerate(matriz):
        for j, numero in enumerate(fila):
            x = j * espacio_x
            y = i * espacio_y
            # Crear el panel con el número y destacar si es la posición actual
            style = "bold red" if celda_pos == (i, j) else "bold green"
            panel = Panel(str(numero), style=style, expand=False)

            # Capturar el panel en texto formateado
            with console.capture() as capture:
                console.print(panel)
            contenido_panel = capture.get()

            # Imprimir el panel en la posición calculada
            for k, linea in enumerate(contenido_panel.splitlines()):
                print(term.move_xy(x, y + k) + linea)

# Función para animar el movimiento de una celda en direcciones permitidas
def animar_celda(matriz, inicio, fin, delay=0.3):
    i, j = inicio

    # Bucle de animación
    while (i, j) != fin:
        # Limpiar la pantalla y reimprimir la matriz con la posición actual de la celda destacada
        print(term.home + term.clear())
        imprimir_matriz(matriz, celda_pos=(i, j))
        time.sleep(delay)  # Pausar para el efecto de animación

        # Movimiento en pasos
        if i < fin[0]:      # Mover hacia abajo
            i += 1
        elif i > fin[0]:    # Mover hacia arriba
            i -= 1
        elif j < fin[1]:    # Mover hacia la derecha
            j += 1
        elif j > fin[1]:    # Mover hacia la izquierda
            j -= 1

    # Imprimir la posición final
    print(term.home + term.clear())
    imprimir_matriz(matriz, celda_pos=(i, j))

# Ejecutar la animación
with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    animar_celda(matriz, inicio=(0, 0), fin=(2, 2), delay=0.2)
