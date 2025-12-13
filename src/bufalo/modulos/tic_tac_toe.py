import random, click
P_MAP = {i+1: i for i in range(9)}
WINS = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
def check_win(b, m):
    for c in WINS:
        if all(b[i] == m for i in c): return True
    return False
def simple_ai(b, m):
    for i in range(9):
        if b[i] == " ":
            cp = list(b); cp[i] = m
            if check_win(cp, m): return i
    mv = [i for i, v in enumerate(b) if v == " "]
    return random.choice(mv) if mv else -1
class Board:
    def __init__(self): self.cells = [" "] * 9
    def display(self):
        c = [self.cells[i] if self.cells[i] != " " else str(i+1) for i in range(9)]
        return f"|{c[0]}|{c[1]}|{c[2]}|\n|{c[3]}|{c[4]}|{c[5]}|\n|{c[6]}|{c[7]}|{c[8]}|"
class Game:
    def __init__(self, s="X"): self.board, self.curr, self.over, self.res = Board(), s, False, None
    def process(self, i):
        if self.over or i < 0 or self.board.cells[i] != " ": return False
        self.board.cells[i] = self.curr
        if check_win(self.board.cells, self.curr): self.over, self.res = True, self.curr
        elif " " not in self.board.cells: self.over, self.res = True, "Tie"
        return True
@click.group(invoke_without_command=True)
def tictactoe(): pass
@tictactoe.command()
def jugar():
    try:
        pm = click.prompt("X/O", type=click.Choice(["X", "O"])); cm = "O" if pm == "X" else "X"; g = Game("X")
        while not g.over:
            idx = click.prompt("Pos", type=int) - 1 if g.curr == pm else simple_ai(g.board.cells, cm)
            if g.process(idx): 
                if not g.over: g.curr = "O" if g.curr == "X" else "X"
            else: click.echo("Err")
        click.echo(f"Fin:{g.res}")
    except Exception as e: click.echo(f"Out:{type(e).__name__}")