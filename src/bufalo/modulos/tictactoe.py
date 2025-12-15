"""
Módulo Tic Tac Toe - Juego de tres en raya para dos jugadores.
"""

import click


class TicTacToe:
    """Clase que maneja la lógica del juego Tic Tac Toe."""

    def __init__(self) -> None:
        """Inicializa un nuevo juego de Tic Tac Toe."""
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.jugador_actual = "X"  # X siempre comienza
        self.ganador = None
        self.movimientos = 0
        self.juego_terminado = False

    def mostrar_tablero(self) -> str:
        """
        Devuelve una representación en string del tablero.

        Returns:
            str: Tablero formateado con números para casillas vacías.
        """
        resultado = []
        for i, fila in enumerate(self.tablero):
            fila_str = []
            for j, celda in enumerate(fila):
                if celda == " ":
                    fila_str.append(str(i * 3 + j + 1))
                else:
                    fila_str.append(celda)
            resultado.append(" | ".join(fila_str))
        return "\n---------\n".join(resultado)

    def hacer_movimiento(self, posicion: int) -> tuple[bool, str]:
        """
        Realiza un movimiento en la posición especificada.

        Args:
            posicion: Número del 1 al 9 representando la casilla.

        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if self.juego_terminado:
            return False, "El juego ya terminó."

        if not 1 <= posicion <= 9:
            return False, "Posición inválida. Debe ser entre 1 y 9."

        fila = (posicion - 1) // 3
        columna = (posicion - 1) % 3

        if self.tablero[fila][columna] != " ":
            return False, "Esa casilla ya está ocupada."

        # Realizar el movimiento
        self.tablero[fila][columna] = self.jugador_actual
        self.movimientos += 1

        # Verificar si hay ganador
        if self._verificar_ganador(fila, columna):
            self.juego_terminado = True
            self.ganador = self.jugador_actual
            return True, f"¡Jugador {self.jugador_actual} gana!"

        # Verificar empate
        if self.movimientos == 9:
            self.juego_terminado = True
            return True, "¡Empate!"

        # Cambiar jugador
        self.jugador_actual = "O" if self.jugador_actual == "X" else "X"
        return True, f"Movimiento realizado. Turno de: {self.jugador_actual}"

    def _verificar_ganador(self, fila: int, columna: int) -> bool:
        """Verifica si el último movimiento resultó en una victoria."""
        jugador = self.tablero[fila][columna]

        # Verificar la fila del movimiento
        gana_fila = True
        for c in range(3):
            if self.tablero[fila][c] != jugador:
                gana_fila = False
                break

        # Verificar la columna del movimiento
        gana_columna = True
        for f in range(3):
            if self.tablero[f][columna] != jugador:
                gana_columna = False
                break

        # Verificar diagonal principal (solo si está en la diagonal)
        gana_diag1 = False
        if fila == columna:
            gana_diag1 = True
            for i in range(3):
                if self.tablero[i][i] != jugador:
                    gana_diag1 = False
                    break

        # Verificar diagonal secundaria (solo si está en la diagonal)
        gana_diag2 = False
        if fila + columna == 2:
            gana_diag2 = True
            for i in range(3):
                if self.tablero[i][2 - i] != jugador:
                    gana_diag2 = False
                    break

        return gana_fila or gana_columna or gana_diag1 or gana_diag2

    def reiniciar(self) -> None:
        """Reinicia el juego a su estado inicial."""
        self.__init__()


# Variable global para mantener el estado del juego
_juego = TicTacToe()


@click.group()
def tictactoe() -> None:
    """Juego de Tic Tac Toe (Tres en raya) para dos jugadores."""
    pass


@tictactoe.command()
def tablero() -> None:
    """Muestra el tablero actual del juego."""
    click.echo("Tablero actual:")
    click.echo(_juego.mostrar_tablero())
    if not _juego.juego_terminado:
        click.echo(f"\nTurno de: {_juego.jugador_actual}")


@tictactoe.command()
@click.argument("posicion", type=int)
def mover(posicion: int) -> None:
    """
    Realiza un movimiento en la posición especificada (1-9).

    Las posiciones son:
      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9
    """
    exito, mensaje = _juego.hacer_movimiento(posicion)
    click.echo(mensaje)
    if exito:
        click.echo("\n" + _juego.mostrar_tablero())


@tictactoe.command()
def reiniciar() -> None:
    """Reinicia el juego a su estado inicial."""
    _juego.reiniciar()
    click.echo("Juego reiniciado. ¡Nueva partida!")
    click.echo(_juego.mostrar_tablero())
    click.echo(f"\nTurno de: {_juego.jugador_actual}")


@tictactoe.command()
def estado() -> None:
    """Muestra el estado actual del juego."""
    click.echo(f"Jugador actual: {_juego.jugador_actual}")
    click.echo(f"Movimientos realizados: {_juego.movimientos}")
    click.echo(f"Juego terminado: {_juego.juego_terminado}")
    if _juego.ganador:
        click.echo(f"Ganador: {_juego.ganador}")
    elif _juego.juego_terminado:
        click.echo("Resultado: Empate")
    click.echo("\nTablero:")
    click.echo(_juego.mostrar_tablero())
