from blessed import Terminal
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
import rich

# Inicializa `blessed` y `rich`
term = Terminal()
console = Console()

# Definir la matriz (puede ser de cualquier tamaño)
matriz_init = [
    [2, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

moves = [
    matriz_init,
    [
        [0, 0, 2],
        [0, 0, 0],
        [0, 0, 0]
    ],
    [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 2]
    ],
    [
        [0, 0, 0],
        [0, 0, 0],
        [2, 0, 0]
    ],
    [
        [2, 2, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    [
        [0, 0, 4],
        [0, 0, 0],
        [0, 0, 0]
    ]
]

# Dimensiones de la matriz y el espaciado entre paneles
filas = len(matriz_init)
columnas = len(matriz_init[0])
espacio_x = 6  # Espacio entre columnas, ajusta según el tamaño del panel
espacio_y = 3   # Espacio entre filas, ajusta según el tamaño del panel
x_tab = 50
y_tab = 5
x_padding = 2 + x_tab
y_padding = 1 + y_tab
ficha = (0, 0)
desFicha = (0, 2)
saltoLinea = "\n"

def imprimir_matriz(matriz, prev=None):
    for i, fila in enumerate(matriz):
        for j, numero in enumerate(fila):
            if not numero:
                if prev and prev[i][j] != 0:
                    # Calcular la posición x, y
                    x = j * espacio_x + x_padding
                    y = i * espacio_y + y_padding

                    # Crear el panel con el número
                    panel = Panel(str(numero), style="bold green", expand=False)

                    # Mover el cursor a la posición (x, y) y luego imprimir el panel
                    with console.capture() as capture:
                        console.print(panel)
                    contenido_panel = capture.get()

                    # Imprimir el panel en la posición calculada
                    for k, linea in enumerate(contenido_panel.splitlines()):
                        print(term.move_xy(x, y + k) + " "*len(linea), end="")
                continue

            # Calcular la posición x, y
            x = j * espacio_x + x_padding
            y = i * espacio_y + y_padding

            # Crear el panel con el número
            panel = Panel(str(numero), style="bold green", expand=False)

            # Mover el cursor a la posición (x, y) y luego imprimir el panel
            with console.capture() as capture:
                console.print(panel)
            contenido_panel = capture.get()

            # Imprimir el panel en la posición calculada
            for k, linea in enumerate(contenido_panel.splitlines()):
                print(term.move_xy(x, y + k) + linea, end="")


# Imprimir la matriz en la consola
with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    with console.capture() as capture:
        console.print(Panel("".join([" "*18 + saltoLinea for _ in range(8)]), style="bold green", expand=False))
    contenido_panel = capture.get()
    for i, linea in enumerate(contenido_panel.splitlines()):
        print(term.move_xy(x_tab, y_tab + i) + linea)
    for matriz in moves:
        imprimir_matriz(matriz)
        input()
    input()