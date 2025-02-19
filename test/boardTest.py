import sys
import os

ruta_src = os.path.abspath(os.path.join(__file__, '..', '..'))

sys.path.append(ruta_src)

from utils.tester import TesterMain, Test
import io
from blessed.terminal import Terminal
from _2048 import board, Direction


"""
@test -> test = test(func)
@test() -> test = test()(func)
@test(args) -> test = test(args)(func)

"""

@Test()
def tablero_inicializado_correctamente():
    tablero = board().game
    assert len(tablero) == 4 and len(tablero[0]) == 4
    assert sum([sum(i) for i in tablero]) > 2

@Test()
def verificar_print():
    buffer = io.StringIO()
    stdout_ori = sys.stdout
    sys.stdout = buffer
    try:
        tablero = board()
        tablero.game = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        tablero.print()
    finally:
        sys.stdout = stdout_ori

    x = tablero.config["x"]
    y = tablero.config["y"]
    pdx = tablero.config["padding_x"]
    pdy = tablero.config["padding_y"]

    def generate_table(x, y, pdx, pdy, m, n):
        test_print = f''
        term = Terminal()
        for i in range(m):
            for j in range(n):
                test_print += f'{term.move_xy(x + pdx * i, y + pdy * j)}\x1b[38;5;181m╭───╮\x1b[0m\n{term.move_xy(x + pdx * i, y + pdy * j + 1)}\x1b[38;5;181m│   │\x1b[0m\n{term.move_xy(x + pdx * i, y + pdy * j + 2)}\x1b[38;5;181m╰───╯\x1b[0m\n'
        test_print += '\n'
        return test_print
    
    assert buffer.getvalue() == generate_table(
        x=x,
        y=y,
        pdx=pdx,
        pdy=pdy,
        m=len(tablero.game),
        n=len(tablero.game[0])
    )
    

@Test(enable_logs=False)
def gano_partida():
    tablero = board()
    
    tablero.game = [
        [2048, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    
    assert tablero.isWin() == True

@Test(enable_logs=False)
def perdio_partida():
    tablero = board()
    
    tablero.game = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2]
    ]
    
    try:
        tablero.move(Direction.RIGHT)
    except:
        return    
    raise Exception("Debio perder la partida")


@Test(enable_logs=False)
def verificando_movimientos_derecho():
    tablero = board()
    
    tablero.game = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    tablero.move(Direction.RIGHT)

    assert tablero.game != [
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

@Test(enable_logs=False)
def verificando_movimientos_izquierdo():
    tablero = board()
    
    tablero.game = [
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    tablero.move(Direction.LEFT)

    assert tablero.game != [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

@Test(enable_logs=False)
def verificando_movimientos_arriba():
    tablero = board()
    
    tablero.game = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 2]
    ]

    tablero.move(Direction.UP)

    assert tablero.game != [
        [2, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

@Test(enable_logs=False)
def verificando_movimientos_abajo():
    tablero = board()
    
    tablero.game = [
        [2, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    tablero.move(Direction.DOWN)

    assert tablero.game != [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [2, 0, 0, 2]
    ]


@TesterMain(enable_logs=True)
def main():
    """
    python test/boardTest.py
    """
    ...

if __name__ == '__main__':
    main()
