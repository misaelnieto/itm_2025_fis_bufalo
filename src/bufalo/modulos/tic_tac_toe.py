import random

import click

# =================================================================
# 1. Variables Globales y de Reglas (LÓGICA INTACTA)
# =================================================================

POSITION_MAP = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8}
WIN_CONDITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def check_win(board, mark):
    for condition in WIN_CONDITIONS:
        if all(board[i] == mark for i in condition):
            return True
    return False


def check_tie(board):
    return " " not in board


def get_valid_moves(board):
    return [i for i, mark in enumerate(board) if mark == " "]


def minimax(board, current_mark, player_mark, computer_mark):
    """Implementación de IA simple con estrategia de apertura."""
    for i in range(9):
        if board[i] == " ":
            board_copy = list(board)
            board_copy[i] = current_mark
            if check_win(board_copy, current_mark):
                return i

    opponent_mark = player_mark if current_mark != player_mark else computer_mark

    for i in range(9):
        if board[i] == " ":
            board_copy = list(board)
            board_copy[i] = opponent_mark
            if check_win(board_copy, opponent_mark):
                return i

    available_moves = get_valid_moves(board)

    if len(available_moves) == 9:
        optimal_moves = [4, 0, 2, 6, 8]
        first_moves = [move for move in optimal_moves if move in available_moves]
        return random.choice(first_moves)

    if available_moves:
        return random.choice(available_moves)
    return -1


# =================================================================
# 2. Clases de Lógica (POO) (LÓGICA INTACTA)
# =================================================================


class Board:
    def __init__(self):
        self.cells = [" "] * 9

    def display(self):
        output = "\n"
        output += (
            f"| {self.cells[0] if self.cells[0] != ' ' else '1'} | "
            f"{self.cells[1] if self.cells[1] != ' ' else '2'} | "
            f"{self.cells[2] if self.cells[2] != ' ' else '3'} |\n"
        )
        output += "-------------\n"
        output += (
            f"| {self.cells[3] if self.cells[3] != ' ' else '4'} | "
            f"{self.cells[4] if self.cells[4] != ' ' else '5'} | "
            f"{self.cells[5] if self.cells[5] != ' ' else '6'} |\n"
        )
        output += "-------------\n"
        output += (
            f"| {self.cells[6] if self.cells[6] != ' ' else '7'} | "
            f"{self.cells[7] if self.cells[7] != ' ' else '8'} | "
            f"{self.cells[8] if self.cells[8] != ' ' else '9'} |\n"
        )
        output += "\n"
        return output

    def make_move(self, index, mark):
        if 0 <= index < 9 and self.cells[index] == " ":
            self.cells[index] = mark
            return True
        return False


class Game:
    def __init__(self, starter=None):
        self.board = Board()
        if starter:
            self.current_player = starter
        else:
            self.current_player = random.choice(["X", "O"])
        self.game_over = False
        self.winner = None
        self.moves_made = 0
        self.player_mark = "X"
        self.computer_mark = "O"

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def process_move(self, index):
        if self.game_over:
            return False

        if self.board.make_move(index, self.current_player):
            self.moves_made += 1
            board_cells = self.board.cells

            if check_win(board_cells, self.current_player):
                self.game_over = True
                self.winner = self.current_player
            elif check_tie(board_cells):
                self.game_over = True
                self.winner = "Tie"

            return True
        return False


# =================================================================
# 3. Lógica CLI (ADAPTADA AL PATRÓN GRUPO)
# =================================================================


def get_player_input(board):
    """Pide y valida la entrada del usuario."""
    while True:
        try:
            position = click.prompt("Elige tu movimiento (1-9)", type=int)
            index = POSITION_MAP.get(position)

            if index is None or not board.cells[index] == " ":
                click.echo("¡Movimiento no válido! Elige un número disponible (1-9).")
            else:
                return index
        except click.exceptions.Abort:
            raise
        except Exception:
            click.echo("Entrada no válida. Por favor, introduce un número.")


# >>> CAMBIO CLAVE AQUÍ <<<
# 1. Definimos el GRUPO principal (que es lo que busca cli.py)
@click.group(invoke_without_command=True)
def tictactoe():
    """Juego Tic Tac Toe (Tres en Raya)."""
    pass


# 2. Definimos el COMANDO 'jugar' adjunto al grupo
@tictactoe.command()
def jugar():
    """Ejecuta el juego contra la computadora."""
    click.echo("¡Bienvenido a Tic Tac Toe!")

    # 1. Asignar símbolos
    player_mark = click.prompt(
        "¿Quieres ser 'X' o 'O'?", type=click.Choice(["X", "O"]), show_choices=True
    )
    computer_mark = "O" if player_mark == "X" else "X"

    # 2. Inicializar el juego
    game = Game()
    game.player_mark = player_mark
    game.computer_mark = computer_mark

    click.echo(f"\n¡Tú eres: {player_mark}! La computadora es: {computer_mark}.")
    click.echo(f"¡El jugador {game.current_player} empieza primero!")

    # 3. Ciclo principal del juego
    while not game.game_over:
        click.echo(game.board.display())

        if game.current_player == player_mark:
            # Turno del jugador
            move_index = get_player_input(game.board)
            if game.process_move(move_index):
                game.switch_player()

        elif game.current_player == computer_mark:
            # Turno de la computadora
            click.echo("Turno de la computadora...")

            move_index = minimax(
                game.board.cells, computer_mark, player_mark, computer_mark
            )

            if move_index != -1 and game.process_move(move_index):
                game.switch_player()

    # 4. Resultado final
    click.echo(game.board.display())
    if game.winner == "Tie":
        click.echo("¡Es un empate!")
    elif game.winner:
        if game.winner == player_mark:
            click.echo("¡Felicidades! ¡Has ganado!")
        else:
            click.echo("¡La computadora ha ganado!")
