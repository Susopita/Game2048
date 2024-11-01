from blessed import Terminal
from rich.console import Console
from rich.panel import Panel
import rich

# Inicializa `blessed` y `rich`
term = Terminal()
console = Console()

# Definir la matriz (puede ser de cualquier tamaño)
matriz = [
    [2, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# Dimensiones de la matriz y el espaciado entre paneles
filas = len(matriz)
columnas = len(matriz[0])
espacio_x = 6  # Espacio entre columnas, ajusta según el tamaño del panel
espacio_y = 3   # Espacio entre filas, ajusta según el tamaño del panel
x_tab = 2
y_tab = 1
ficha = (0, 0)
desFicha = (0, 2)
saltoLinea = "\n"

# Imprimir la matriz en la consola
with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    with console.capture() as capture:
        console.print(Panel("".join([" "*18 + saltoLinea for _ in range(8)]), style="bold green", expand=False))
    contenido_panel = capture.get()
    for i, fila in enumerate(matriz):
        for j, numero in enumerate(fila):
            # Calcular la posición x, y
            x = j * espacio_x + x_tab
            y = i * espacio_y + y_tab

            # Crear el panel con el número
            panel = Panel(str(numero), style="bold green", expand=False)

            # Mover el cursor a la posición (x, y) y luego imprimir el panel
            with console.capture() as capture:
                console.print(panel)
            contenido_panel = capture.get()

            # Imprimir el panel en la posición calculada
            for k, linea in enumerate(contenido_panel.splitlines()):
                print(term.move_xy(x, y + k) + linea, end="")

    input()