from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from game_logic_2_0 import Game_logic


class MainApp(App):
    def build(self):
        self.title = "XvsO"
        Window.clearcolor = (0.035, 0.07, 0.14, 1)
        self.bot_starts = True
        self.bot_score = 0
        self.you_score = 0
        self.gameplay = True
        self.game = Game_logic("ww_beast.pkl")
        self.buttons = {}

        root = FloatLayout()
        self.bot_label = Label(text="Бот\n0", size_hint=(.3,.12),
                               pos_hint={"center_x":.78,"top":.98}, font_size="20sp")
        self.you_label = Label(text="Ты\n0", size_hint=(.3,.12),
                               pos_hint={"center_x":.22,"top":.98}, font_size="20sp")
        self.status = Label(text="XvsO", size_hint=(.8,.08),
                            pos_hint={"center_x":.5,"top":.85}, font_size="20sp")
        root.add_widget(self.bot_label)
        root.add_widget(self.you_label)
        root.add_widget(self.status)

        board = GridLayout(rows=3, cols=3, spacing=5, padding=5,
                           size_hint=(.88,.52), pos_hint={"center_x":.5,"center_y":.49})
        for row in range(1,4):
            for col in range(1,4):
                btn = Button(text="", font_size="48sp",
                             background_normal="", background_color=(.10,.20,.34,1),
                             color=(.35,.95,.95,1))
                btn.row, btn.col = row, col
                btn.bind(on_press=self.press_player)
                self.buttons[(row,col)] = btn
                board.add_widget(btn)
        root.add_widget(board)

        reset_btn = Button(text="Новая игра", size_hint=(.42,.09),
                           pos_hint={"center_x":.28,"y":.06},
                           background_normal="", background_color=(.08,.55,.68,1))
        reset_btn.bind(on_press=self.reset)
        mode_btn = Button(text="Первым: Бот", size_hint=(.42,.09),
                          pos_hint={"center_x":.72,"y":.06},
                          background_normal="", background_color=(.30,.25,.58,1))
        mode_btn.bind(on_press=self.switch_first)
        root.add_widget(reset_btn)
        root.add_widget(mode_btn)
        self.mode_button = mode_btn
        self.reset(None)
        return root

    def switch_first(self, *_):
        self.bot_starts = not self.bot_starts
        self.mode_button.text = "Первым: Бот" if self.bot_starts else "Первым: Ты"
        self.reset()

    def reset(self, *_):
        self.gameplay = True
        self.game.reset()
        for btn in self.buttons.values():
            btn.text = ""
            btn.disabled = False
            btn.color = (0.35,0.95,0.95,1)
        self.status.text = "Твой ход" if not self.bot_starts else "Ход бота"
        if self.bot_starts:
            self.ai_press()

    def finish_if_needed(self):
        winning_line = self.game.detect_win()
        if winning_line[0] != 0:
            winner = self.game.board[winning_line[0][0]][winning_line[0][1]]
            self.gameplay = False
            if winner == 1:
                self.bot_score += 1
                self.bot_label.text = f"Бот\n{self.bot_score}"
                self.status.text = "Победил бот"
            else:
                self.you_score += 1
                self.you_label.text = f"Ты\n{self.you_score}"
                self.status.text = "Ты победил!"
            self._lock_board()
            return True
        if not self.game.svoboda():
            self.gameplay = False
            self.status.text = "Ничья!"
            self._lock_board()
            return True
        return False

    def _lock_board(self):
        for btn in self.buttons.values():
            btn.disabled = True

    def press_player(self, instance):
        if not self.gameplay or not self.game.move(instance.row, instance.col, -1):
            return
        instance.text = "O"
        instance.color = (0.20,0.95,0.85,1)
        if not self.finish_if_needed():
            self.ai_press()

    def ai_press(self):
        if not self.gameplay:
            return
        move = self.game.ai_hod(pl=1, eps=0)
        if move is None:
            self.finish_if_needed()
            return
        if self.game.move(move[0], move[1], 1):
            btn = self.buttons[move]
            btn.text = "X"
            btn.color = (1,.48,.30,1)
        self.finish_if_needed()


if __name__ == "__main__":
    MainApp().run()
