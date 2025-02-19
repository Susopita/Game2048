from enum import Enum, auto
from blessed import Terminal
import rich
import random
import shutil
import rich.panel
from rich.console import Console
from rich.style import Style

console = Console()
term = Terminal()

class Direction(Enum):
    """
    Movimientos posibles en el tablero de 2048.

    - RIGHT: Mover hacia la derecha.
    - LEFT: Mover hacia la izquierda.
    - DOWN: Mover hacia abajo.
    - UP: Mover hacia arriba.
    """
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()
    UP = auto()

colors = {
    0: Style(color="rgb(205, 193, 180)"),
    2: Style(color="rgb(238, 228, 218)"),
    4: Style(color="rgb(237, 224, 200)"),
    8: Style(color="rgb(242, 117, 121)"),
    16: Style(color="rgb(245, 149, 99)"),
    32: Style(color="rgb(246, 124, 95)"),
    64: Style(color="rgb(247, 94, 59)"),
    128: Style(color="rgb(237, 207, 114)"),
    256: Style(color="rgb(238, 228, 218)"),
    512: Style(color="rgb(238, 228, 218)"),
    1024: Style(color="rgb(238, 228, 218)"),
    2048: Style(color="rgb(238, 228, 218)")
}

def board():
    """
    Funcion que crea y inicializar los atributos de si mismo para el tablero de 2048.
    """

    def init():
        """
        Funcion inicializadora del tablero.
        - Crea el tablero de 4 x 4.
        - Genera los primeros dos valores en posiciones aleatorias.
        """
        inicialBoard = [[0 for _ in range(4)] for _ in range(4)]
        for _ in range(2):
            x, y = random.choice([(i, j) for i in range(4) for j in range(4) if inicialBoard[i][j] == 0])
            inicialBoard[x][y] = random.choice([2, 4])
        return inicialBoard

    def print_():
        """
        0: rgb(205, 193, 180)
        2: rgb(238, 228, 218)
        4: rgb(237, 224, 200)
        8: rgb(242, 117, 121)
        16: rgb(245, 149, 99)
        32: rgb(246, 124, 95)
        64: rgb(247, 94, 59)
        128: rgb(237, 207, 114)
        """
        for i, fila in enumerate(board.game):
            for j, num in enumerate(fila):
                x = board.config["x"] + board.config["padding_x"] * j
                y = board.config["y"] + board.config["padding_y"] * i
                with console.capture() as capture:
                    console.print(rich.panel.Panel(f"    \n{num if num else ' ':^4}\n    ", expand=False))
                contenido_panel = capture.get()

                # Imprimir el panel en la posición calculada
    
                for k, linea in enumerate(contenido_panel.splitlines()):
                    print(term.move_xy(x, y + k), end="")
                    console.print(linea, style=colors[num], highlight=False)
        print()
            

    def generate_value():
        pos = [(j, i) for j in range(4) for i in range(4) if board.game[j][i] == 0]

        if len(pos) == 0:
            raise Exception("No hay mas espacio en el tablero")
        
        t = random.choice(pos)
        board.game[t[0]][t[1]] = random.choice([2, 4])

    def move(direction: Direction):
        """
        Funcion multiproposito para mover el tablero en las 4 direcciones y generar un nuevo valor en el tablero.
        Mediante "rightShift" se realiza el desplazamiento de los valores en el tablero.
        """

        def rightShift(matrix: list):
            """
            Desplaza todos los numeros hacia la derecha y fusiona aquellos compatibles
            """

            for i in matrix:
                    
                    for idx in range(len(i) - 2, -1, -1):

                        # Obvia los espacios en blanco
                        if i[idx] == 0:
                            continue

                        nextIdx: int

                        # Busca el indice hasta el cual se puede desplazar
                        for nextIdx in range(idx + 1, len(i)):
                            if i[nextIdx] != 0:
                                nextIdx -= 1
                                break
                        
                        # Intercambio el indice nuevo por el antiguo
                        if nextIdx != idx:
                            i[nextIdx] = i[idx]
                            i[idx] = 0
                        
                        
                        if i[nextIdx] and nextIdx + 1 < len(i) and i[nextIdx] == i[nextIdx + 1]:
                            i[nextIdx + 1] *= 2
                            i[nextIdx] = 0
                        
             
        match (direction):
    
            case Direction.RIGHT:
                rows = [i for i in board.game]

                rightShift(rows)
                
                """
                print() 

                for i in rows:
                    print(i)
                """
                    
                board.game = rows

            case Direction.LEFT:
                rows = [i[::-1] for i in board.game]

                rightShift(rows)

                """
                print() 

                for i in rows:
                    print(i)
                """

                board.game = [i[::-1] for i in rows]

            case Direction.DOWN:
                columns = [[board.game[j][i] for j in range(4)] for i in range(4)]

                rightShift(columns)

                """
                print() 

                for i in rows:
                    print(i)
                """
                
                board.game = [[columns[j][i] for j in range(4)] for i in range(4)]

            case Direction.UP:
                columns = [[board.game[j][i] for j in range(4)][::-1] for i in range(4)]

                rightShift(columns)

                """
                print() 

                for i in rows:
                    print(i)
                """
                
                board.game = [[columns[j][i] for j in range(4)] for i in range(3, -1, -1)]


        generate_value()

    def isWin() -> bool:
        for i in board.game:
            if 2048 in i:
                return True
        return False

    if not hasattr(board, "game"):
        board.game = init()
        board.print = print_
        board.isWin = isWin
        board.move = move
        pd_x = 8
        pd_y = 5
        board.config = {
            "x": shutil.get_terminal_size().columns // 2 - pd_x * len(board.game) // 2,
            "y": shutil.get_terminal_size().lines // 2 - pd_y * len(board.game) // 2,
            "padding_x": pd_x,
            "padding_y": pd_y,
        }

    return board


def player():
    """
    Pequeña funcion para asignar un nombre al jugador.
    """
    player.name = ""
    return player

def Game2048():
    """
    Funcion Base para el juego 2048.
    Gestiona la inicializacion, flujo y finalizacion del juego.
    """

    def setup():
        """
        Setter para el nombre del jugador. (require interaccion con el usuario)
        """
        print(f"\rIngrese nombre del jugador:", end="", flush=True)
        with term.cbreak():
            name = ""
            while True:
                key = term.inkey()

                if key.is_sequence:
                    if key.name == "KEY_BACKSPACE":
                        print(term.clear())
                        name = name[:-1]
                    if key.name == "KEY_ENTER":
                        Game2048.player.name = name
                        print()
                        break
                else:
                    name += key
                print(f"\rIngrese nombre del jugador: {name}", end="", flush=True)

    def start():
        """
        Main loop principal del juego.

        Maneja:
        - Imprimir el tablero.
        - Recibir la direccion del movimiento del jugador.
        - Verificar si el jugador ha ganado.
        - Verificar si el jugador ha perdido.
        - Finalizar el juego.

        Notas:
            El flujo del juego se mantiene en un loop infinito hasta que el jugador gane o pierda.
            Y las acciones que modifican el tablero son envueltas en un try-except.
            Esto para evitar que la experiencia de usuario se vea interrumpida por errores.
        """

        print(term.clear(), end="")
        setup()
        print(term.clear(), end="")

        print(term.move_xy(board.config["x"], board.config["y"] - 1), end="")
        print("Tablero actual:")

        print(term.move_xy(board.config["x"], board.config["y"] + board.config["padding_y"] * 4), end="")
        print(f"Jugador: {Game2048.player.name}")
        print(term.move_xy(board.config["x"], board.config["y"] + board.config["padding_y"] * 4 + 1), end="")
        print("Presione una direccion: ↑ ↓ → ←")

        with term.cbreak():
            while True:
                
                # Aqui se imprime el tablero
                Game2048.board.print()

                key = term.inkey()

                try:
                    match (key.name):

                        case "KEY_UP":
                            Game2048.board.move(Direction.UP)

                        case "KEY_DOWN":
                            Game2048.board.move(Direction.DOWN)

                        case "KEY_LEFT":
                            Game2048.board.move(Direction.LEFT)

                        case "KEY_RIGHT":
                            Game2048.board.move(Direction.RIGHT)

                        case "KEY_ESCAPE":
                            print()
                            print("Juego terminado.\nbye bye")
                            break

                        case _:
                            print()
                            print("Direccion no valida. Intente de nuevo")
                            print()

                    if Game2048.board.isWin():
                        print("Has ganado!!!")
                        print("Juego terminado.\nbye byeee")
                        break

                except:
                    print("Has perdido.")
                    print("Juego terminado.\nbye bye :b")
                    break
                   
    if not hasattr(Game2048, "start"):      
        Game2048.start = start
        Game2048.player = player()
        Game2048.board = board()
    
    return Game2048

