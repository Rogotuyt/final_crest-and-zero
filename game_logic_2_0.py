import pickle
import random

WIN_PATTERNS = (
    ((1, 1), (-1, -1)),
    ((1, -1), (-1, 1)),
    ((1, 0), (-1, 0)),
    ((0, 1), (0, -1)),
)


class Game_logic:
    def __init__(self, q_file="q_tab.pkl"):
        self.q_file = q_file
        self.q_tab = self.load_q(q_file)
        self.reset()

    def reset(self):
        self.board = [[0] * 5 for _ in range(5)]

    def load_q(self, file):
        try:
            with open(file, "rb") as stream:
                data = pickle.load(stream)
            return data if isinstance(data, dict) else {}
        except FileNotFoundError:
            return {}

    def svoboda(self, board=None):
        current = self.board if board is None else board
        return [(r, c) for r in range(1, 4) for c in range(1, 4)
                if current[r][c] == 0]

    def detect_win(self):
        for r in range(1, 4):
            for c in range(1, 4):
                for first, second in WIN_PATTERNS:
                    r2, c2 = r + first[0], c + first[1]
                    r3, c3 = r + second[0], c + second[1]
                    value = self.board[r][c]
                    if value != 0 and value == self.board[r2][c2] == self.board[r3][c3]:
                        return [(r, c), (r2, c2), (r3, c3)]
        return [0, 0, 0]

    def create_key(self, pl, board=None):
        current = self.board if board is None else board
        return (tuple(tuple(row) for row in current), pl)

    def ai_hod(self, pl, eps=0):
        available = self.svoboda()
        if not available:
            return None
        key = self.create_key(pl=pl)
        if key not in self.q_tab:
            self.q_tab[key] = {move: 0 for move in available}
        # Older saved tables may not contain moves added by a changed state.
        for move in available:
            self.q_tab[key].setdefault(move, 0)
        if eps > random.random():
            return random.choice(available)
        return max(available, key=lambda move: self.q_tab[key][move])

    def is_game(self):
        return self.detect_win()[0] == 0 and bool(self.svoboda())

    def move(self, row, col, pl):
        if (row, col) not in self.svoboda():
            return False
        self.board[row][col] = pl
        return True

    def save_q(self):
        with open(self.q_file, "wb") as stream:
            pickle.dump(self.q_tab, stream)

    def q_lerninig(self, winer, gamma=0.9, history=None, lr=0.1):
        history = history or []
        for index in reversed(range(len(history))):
            pl, move, state = history[index]
            if index == len(history) - 1:
                target = winer * pl
            else:
                next_state = history[index + 1][2]
                next_values = self.q_tab.get(next_state, {}).values()
                target = -gamma * max(next_values, default=0)
            self.q_tab[state][move] += lr * (target - self.q_tab[state][move])
