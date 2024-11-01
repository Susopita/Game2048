from blessed import Terminal
from rich.console import Console
from rich.live import Live
from rich.text import Text
import time

term = Terminal()
console = Console()

# Contenido que se animará en vivo
texto_animado = Text("Animación en tiempo real con blessed y rich", style="bold magenta")

# Usar blessed para pantalla completa, modo cbreak y ocultar el cursor
with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    # Usar rich Live para actualización en tiempo real
    with Live(texto_animado, console=console, refresh_per_second=10) as live:
        for i in range(50):  # Simulación de 50 "frames"
            texto_animado = Text(f"Posición del texto: {i}", style="bold cyan")
            live.update(texto_animado)  # Actualizar el contenido en cada iteración
            time.sleep(0.1)  # Control de velocidad de la animación
