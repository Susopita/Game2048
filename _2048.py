from enum import Enum, auto
from blessed import Terminal
import rich
import random

import rich.panel

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
        print(term.move_xy(0, 1))
        for i in board.game:
            for j in i:
                print(f"{j:>4}", end="")
            print()
        for i in board.game:
            for j in i:
                print(term.move_xy(20, 10))
                rich.print(rich.panel.Panel(f"{j}", expand=False), end="")
            rich.print()

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
            Right
            """
            for i in matrix:
                    print(i)
                    
                    for idx in range(2, -1, -1):

                        if i[idx] == 0:
                            continue

                        nextIdx: int

                        for nextIdx in range(idx + 1, 4):
                            if i[nextIdx] != 0:
                                nextIdx -= 1
                                break
                        
                        if nextIdx != idx:
                            i[nextIdx] = i[idx]
                            i[idx] = 0

        print(term.move_xy(0, 10))
        match (direction):
            case Direction.RIGHT:
                rows = [i for i in board.game]

                rightShift(rows)

                print() 

                for i in rows:
                    print(i)
                    
                board.game = rows

            case Direction.LEFT:
                rows = [i[::-1] for i in board.game]

                rightShift(rows)

                print() 

                for i in rows:
                    print(i)

                board.game = [i[::-1] for i in rows]

            case Direction.DOWN:
                columns = [[board.game[j][i] for j in range(4)] for i in range(4)]

                rightShift(columns)

                print() 

                for i in columns:
                    print(i)
                
                board.game = [[columns[j][i] for j in range(4)] for i in range(4)]

            case Direction.UP:
                columns = [[board.game[j][i] for j in range(4)][::-1] for i in range(4)]

                rightShift(columns)

                print() 
                
                for i in columns:
                    print(i)
                
                board.game = [[columns[j][i] for j in range(4)] for i in range(3, -1, -1)]

        generate_value()


    def isWin():
        for i in board.game:
            if 2048 in i:
                return True
        return False

    if not hasattr(board, "game"):
        board.game = init()
    board.print = print_
    board.isWin = isWin
    board.move = move

    return board

def player(name):
    """
    Pequeña funcion para asignar un nombre al jugador.
    """
    player.name = name
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

        print("Tablero actual:")
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print(f"Jugador: {Game2048.player.name}\nPresione una direccion: ↑ ↓ → ←")

        with term.cbreak():
            while True:
                
                # Aqui se imprime el tablero
                Game2048.board().print()

                key = term.inkey()

                try:
                    match (key.name):

                        case "KEY_UP":
                            Game2048.board().move(Direction.UP)

                        case "KEY_DOWN":
                            Game2048.board().move(Direction.DOWN)

                        case "KEY_LEFT":
                            Game2048.board().move(Direction.LEFT)

                        case "KEY_RIGHT":
                            Game2048.board().move(Direction.RIGHT)

                        case "KEY_ESCAPE":
                            print()
                            print("Juego terminado.\nbye bye")
                            break

                        case _:
                            print()
                            print("Direccion no valida. Intente de nuevo")
                            print()

                    if Game2048.board().isWin():
                        print("Has ganado!!!")
                        print("Juego terminado.\nbye byeee")
                        break

                except:
                    print("Has perdido.")
                    print("Juego terminado.\nbye bye :b")
                    break
                   
 
    Game2048.start = start
    Game2048.player = player
    Game2048.board = board
    
    return Game2048

