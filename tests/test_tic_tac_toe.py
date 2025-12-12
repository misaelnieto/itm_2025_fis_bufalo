"""
Pruebas unitarias para el módulo Tic Tac Toe desarrolladas con TDD.
"""

from src.bufalo.modulos.tic_tac_toe import (
    Board,
    Game,
    check_tie,
    check_win,
    get_valid_moves,
    minimax,
)


class TestBoard:
    """Pruebas para la clase Board."""

    def test_board_initialization(self):
        """Test 1: El tablero debe inicializarse vacío."""
        board = Board()
        assert len(board.cells) == 9
        assert all(cell == " " for cell in board.cells)

    def test_board_display(self):
        """Test 2: El tablero debe mostrarse correctamente."""
        board = Board()
        display = board.display()
        assert "1 | 2 | 3" in display
        assert "4 | 5 | 6" in display
        assert "7 | 8 | 9" in display

    def test_board_make_move(self):
        """Test 3: Debe poder realizar un movimiento válido."""
        board = Board()
        assert board.make_move(0, "X") # Eliminada la comparación == True
        assert board.cells[0] == "X"

    def test_board_invalid_move(self):
        """Test 4: No debe permitir movimiento en casilla ocupada."""
        board = Board()
        board.make_move(0, "X")
        assert not board.make_move(0, "O") # Uso not para comparación == False

    def test_board_out_of_range(self):
        """Test 5: No debe permitir movimiento fuera de rango."""
        board = Board()
        assert not board.make_move(9, "X") # Uso not para comparación == False
        assert not board.make_move(-1, "X") # Uso not para comparación == False


class TestWinConditions:
    """Pruebas para las condiciones de victoria."""

    def test_horizontal_win(self):
        """Test 6: Debe detectar victoria horizontal."""
        # Fila superior
        board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        assert check_win(board, "X") # Eliminada la comparación == True

        # Fila media
        board = [" ", " ", " ", "O", "O", "O", " ", " ", " "]
        assert check_win(board, "O") # Eliminada la comparación == True

    def test_vertical_win(self):
        """Test 7: Debe detectar victoria vertical."""
        # Columna izquierda
        board = ["X", " ", " ", "X", " ", " ", "X", " ", " "]
        assert check_win(board, "X") # Eliminada la comparación == True

    def test_diagonal_win(self):
        """Test 8: Debe detectar victoria diagonal."""
        # Diagonal principal
        board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
        assert check_win(board, "X") # Eliminada la comparación == True

        # Diagonal secundaria
        board = [" ", " ", "O", " ", "O", " ", "O", " ", " "]
        assert check_win(board, "O") # Eliminada la comparación == True

    def test_no_win(self):
        """Test 9: Debe retornar False cuando no hay victoria."""
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        assert not check_win(board, "X") # Uso not para comparación == False
        assert not check_win(board, "O") # Uso not para comparación == False


class TestTieCondition:
    """Pruebas para la condición de empate."""

    def test_board_full_tie(self):
        """Test 10: Debe detectar empate cuando el tablero está lleno."""
        board = ["X", "O", "X", "X", "X", "O", "O", "X", "O"]
        assert check_tie(board) # Eliminada la comparación == True

    def test_board_not_full(self):
        """Test 11: No debe detectar empate si hay casillas vacías."""
        board = ["X", "O", "X", "X", " ", "O", "O", "X", "O"]
        assert not check_tie(board) # Uso not para comparación == False


class TestValidMoves:
    """Pruebas para movimientos válidos."""

    def test_get_valid_moves_empty(self):
        """Test 12: Debe retornar todas las casillas en tablero vacío."""
        board = [" "] * 9
        moves = get_valid_moves(board)
        assert len(moves) == 9
        assert set(moves) == {0, 1, 2, 3, 4, 5, 6, 7, 8}

    def test_get_valid_moves_partial(self):
        """Test 13: Debe retornar solo casillas vacías."""
        board = ["X", " ", "O", " ", "X", " ", "O", " ", " "]
        moves = get_valid_moves(board)
        assert moves == [1, 3, 5, 7, 8]


class TestGameAI:
    """Pruebas para la IA del juego (Minimax)."""

    def test_ai_block_win(self):
        """Test 14: La IA debe bloquear victoria inminente del jugador."""
        # Escenario: jugador tiene X X _ en fila superior
        board = ["X", "X", " ", "O", " ", " ", " ", " ", " "]
        best_move = minimax(board, "O", "X", "O")
        assert best_move == 2  # Debe bloquear en posición 2

    def test_ai_win_move(self):
        """Test 15: La IA debe tomar victoria si está disponible."""
        # Escenario: IA tiene O O _ en fila superior
        board = ["O", "O", " ", "X", " ", "X", " ", " ", " "]
        best_move = minimax(board, "O", "X", "O")
        assert best_move == 2  # Debe ganar en posición 2

    def test_ai_optimal_first_move(self):
        """Test 16: En tablero vacío, IA debe elegir esquina o centro."""
        board = [" "] * 9
        best_move = minimax(board, "X", "O", "X")
        assert best_move in [0, 2, 4, 6, 8]  # Esquinas o centro


class TestGameClass:
    """Pruebas para la clase principal Game."""

    def test_game_initialization(self):
        """Test 17: El juego debe inicializarse correctamente."""
        game = Game(starter="X") # Uso de starter='X' para evitar aleatoriedad en test
        assert game.board is not None
        assert game.current_player in ["X", "O"]
        assert not game.game_over # Uso not para comparación == False
        assert game.winner is None

    def test_game_switch_player(self):
        """Test 18: Debe cambiar de jugador correctamente."""
        game = Game(starter="X")
        initial = game.current_player
        game.switch_player()
        assert game.current_player != initial

    def test_game_process_move(self):
        """Test 19: Debe procesar movimiento y cambiar estado."""
        game = Game(starter="X")
        game.process_move(4)  # Centro
        assert game.board.cells[4] == game.current_player
        assert game.moves_made == 1


class TestIntegration:
    """Pruebas de integración."""

    def test_complete_game_flow(self):
        """Test 20: Flujo completo de juego (integración)."""
        # CORRECCIÓN CLAVE: Forzar que 'X' inicie el juego para que la prueba sea determinista.
        game = Game(starter="X") 

        # Jugador X en centro (Primer movimiento. Como X inició, X debe moverse)
        assert game.process_move(4) # Eliminada la comparación == True
        assert game.board.cells[4] == "X"

        # Jugador O en esquina (Debe cambiar el turno antes de moverse)
        game.switch_player()
        assert game.process_move(0) # Eliminada la comparación == True
        assert game.board.cells[0] == "O"

        # Verificar que el juego no ha terminado
        assert not game.game_over # Uso not para comparación == False