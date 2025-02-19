from functools import wraps
from typing import Callable
from colorama import Fore
import sys
import io
from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
import traceback
import shutil
import re

tests: list[Callable] = list()

tests_result: dict[str, dict[str, str | bool]]

@contextmanager
def silenciar_logs():
    sys.stdout = io.StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = sys.__stdout__

def Test(enable_logs: bool = True) -> Callable:
    """
    Requiere que lo uses de forma:
    ```python
    @Test()
    def test_1():
        ...
    
    @Test(enable_logs=True, ...)
    def test_2():
        ...
    ```
    Evita:
    ```python
    @Test
    def test_1():
        ...
    ```
    """
    def wrapperArgs(func: Callable) -> Callable:

        if enable_logs:
            func.__with_logs__ = True
        else:
            func.__with_logs__ = False
        
        tests.append(func)

        return func
    return wrapperArgs



def _ejecutar_test(test: Callable, tests_result):

    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        if not test.__with_logs__:
            with silenciar_logs():
                test()
        else:
            test()
        result = {
            "pass" : True,
            "error" : "",
            "logs" : buffer.getvalue()
        }
    except Exception:
        result = {
            "pass" : False,
            "error" : traceback.format_exc(),
            "logs" : buffer.getvalue()
        }

    finally:
        tests_result[test.__name__] = result
        sys.stdout = sys.__stdout__

def clen(te):
    lines = []
    r, c = 0, 0
    ansi_p = re.compile(r'\x1b\[(\d+);(\d+)H')
    last_end=0
    for match in ansi_p.finditer(te):
        n_r = int(match.group(1)) -1
        n_c = int(match.group(2)) -1
        seg = te[last_end:match.start()]
        while len(lines) <= r:
            lines.append([])
        
        while len(lines[r]) <= c:
            lines[r].append(" ")

        for char in seg:
            if c >= len(lines[r]):
                lines[r].append(" ")
            lines[r][c] = char
            c += 1
        r, c = n_r, n_c
        last_end = match.end()

    r_te = te[last_end:]
    while len(lines) <= r:
        lines.append([])

    for char in r_te:
            while c >= len(lines[r]):
                lines[r].append(" ")
            lines[r][c] = char
            c += 1

    resul_lines = ["".join(line).rstrip() for line in lines]

    return "\n".join(resul_lines).rstrip()

def TesterMain(enable_logs: bool = True) -> Callable:
    def wrapperArgs(func: Callable) -> Callable:
        @wraps(func)
        def wrapper():
            global tests, tests_result
            
            max_name_test = len(max(list(map(lambda func: func.__name__, tests)), key=len))
            space = max_name_test + 10

            print(Fore.GREEN + f"{f' Ejecutando tests de {func.__name__} ':=^{space + 3 }}")

            # Ejecucion paralelizada 
            with Manager() as manager:
                tests_result = manager.dict()
                with ProcessPoolExecutor() as executor:
                    executor.map(_ejecutar_test, tests, [tests_result] * len(tests))
                tests_result = dict(tests_result)
            
            # Muestra de resultados
                
            for test, result in tests_result.items():
                if result["pass"]:
                    print(Fore.GREEN + f" {test:·<{space}} O")
                else:
                    print(Fore.RED + f" {test:·<{space}} X")

            print(Fore.GREEN + f"{' Fin de tests ':=^{space + 3}}")

            # Errores, debug y logs

            def filter_errors(test):
                return True if test[1]['pass'] == False else False
            
            def filter_logs(test):
                return True if test[1]['logs'] != '' else False
            
            errors = dict(filter(filter_errors, tests_result.items()))
            logs   = dict(filter(filter_logs,   tests_result.items()))
            err_logs = errors | logs

            if len(err_logs):

                print(Fore.RED + f"Errores "+Fore.LIGHTBLACK_EX+". . .  " + Fore.YELLOW + f"{len(errors)}")
                print(Fore.WHITE + f"Logs    "+Fore.LIGHTBLACK_EX+". . .  " + Fore.YELLOW + f"{len(logs)}")

                col, _ = shutil.get_terminal_size()
    
                for test, debug in err_logs.items():
                    if enable_logs == False and debug["error"] == "":
                        continue

                    print()
                    print(Fore.YELLOW + f"{f' Debug {test} ':–^{col}}")

                    # Errors
                    if debug["error"] != "":
                        print(Fore.RED + debug["error"])

                    # Logs
                    if debug["logs"] != "":
                        print(Fore.WHITE + f"logs: ")
                        print(clen(debug["logs"]))
                    
                    print(Fore.YELLOW + "–"*col)

            print(Fore.RESET)

        return wrapper
    return wrapperArgs
