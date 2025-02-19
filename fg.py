from blessed import Terminal
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
import time
from typing import Union
import attr

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

@attr.s
class Celda:
    valor: Union[int, str] = attr.ib(converter=lambda x: str(x))
    x: int = attr.ib(converter=lambda x: int(x), default=0)
    y: int = attr.ib(converter=lambda x: int(x), default=0)
    style: Style = attr.ib(default=None)

# Función para imprimir toda la matriz con una celda móvil
def imprimir_matriz(matriz, celda_pos):
    for i, fila in enumerate(matriz):
        for j, numero in enumerate(fila):
            x = j * espacio_x
            y = i * espacio_y

            celda = Celda(
                valor=numero,
                x=x,
                y=y,
                style="bold red" if celda_pos == (i, j) else "bold green"
            )

            print_celda(celda)

def print_celda(celda: Celda, style: Style = None):
    _style = celda.style if not style else style
    panel = Panel(celda.valor, style=_style, expand=False)

    with console.capture() as cap:
        console.print(panel)
    contenido_panel = cap.get()

    for k, linea in enumerate(contenido_panel.splitlines()):
        print(term.move_xy(celda.x, celda.y + k) + linea)

def animate_celda_to(): 
    ...              

# Función para animar el movimiento de una celda en direcciones permitidas
def animar_celda(matriz, inicio, fin, delay=0.3):
    i, j = inicio

    # Bucle de animación
    while (i, j) != fin:
        input()
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

    input()
