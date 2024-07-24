#!/usr/bin/env python3
"""2048 game using tkinter"""

from tkinter import Event, Tk, ttk, StringVar, messagebox
import random


class Game:
    """2048 game"""

    _BOARD_SIZE = 4
    _COLORS = {
        "": "#ffffff",
        "2": "#eee4da",
        "4": "#ede0c8",
        "8": "#f2b179",
        "16": "#f59563",
        "32": "#f67c5f",
        "64": "#f65e3b",
        "128": "#edcf72",
        "256": "#edcc61",
        "512": "#edc850",
        "1024": "#edc53f",
        "2048": "#edc22e",
    }
    _FG_COLOR = "#000000"

    def _compress(self, direction: str) -> None:
        i_addend = {
            "down": 1,
            "up": -1,
            "left": 0,
            "right": 0,
        }[direction]
        j_addend = {
            "down": 0,
            "up": 0,
            "left": -1,
            "right": 1,
        }[direction]
        i_range = {
            "down": range(self._BOARD_SIZE - 1),
            "up": range(self._BOARD_SIZE - 1, 0, -1),
            "left": range(self._BOARD_SIZE),
            "right": range(self._BOARD_SIZE),
        }[direction]
        j_range = {
            "down": range(self._BOARD_SIZE),
            "up": range(self._BOARD_SIZE),
            "left": range(self._BOARD_SIZE - 1, 0, -1),
            "right": range(self._BOARD_SIZE - 1),
        }[direction]
        for i in i_range:
            for j in j_range:
                if (
                    self._board[i][j].get() != ""
                    and self._board[i + i_addend][j + j_addend].get() == ""
                ):
                    self._board[i + i_addend][j + j_addend].set(self._board[i][j].get())
                    self._board[i][j].set("")

    def _check_win(self) -> str:
        amount_empty = 0
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
                if self._board[i][j].get() == "2048":
                    return "You win!"
                if self._board[i][j].get() == "":
                    amount_empty += 1
        if amount_empty == 0:
            return "You lose!"
        return "continue"

    def _merge(self, direction: str) -> None:
        i_addend = {
            "down": 0,
            "up": -1,
            "left": 0,
            "right": 0,
        }[direction]
        j_addend = {
            "down": -1,
            "up": 0,
            "left": 1,
            "right": -1,
        }[direction]
        i_range = {
            "down": range(self._BOARD_SIZE - 1, 0, -1),
            "up": range(self._BOARD_SIZE - 1),
            "left": range(self._BOARD_SIZE),
            "right": range(self._BOARD_SIZE),
        }[direction]
        j_range = {
            "down": range(self._BOARD_SIZE),
            "up": range(self._BOARD_SIZE),
            "left": range(self._BOARD_SIZE - 1),
            "right": range(self._BOARD_SIZE - 1, 0, -1),
        }[direction]
        for i in i_range:
            for j in j_range:
                if (
                    self._board[i][j].get() != ""
                    and self._board[i + i_addend][j + j_addend].get() != ""
                    and self._board[i][j].get()
                    == self._board[i + i_addend][j + j_addend].get()
                ):
                    self._board[i][j].set(str(int(self._board[i][j].get()) * 2))
                    self._board[i + i_addend][j + j_addend].set("")

    def _move(self, key: Event) -> None:
        key_symbol = key.keysym
        direction = ""
        if key_symbol in ("Up", "w"):
            direction = "up"
        elif key_symbol in ("Down", "s"):
            direction = "down"
        elif key_symbol in ("Left", "a"):
            direction = "left"
        elif key_symbol in ("Right", "d"):
            direction = "right"
        if direction == "":
            return
        self._compress(direction)
        self._merge(direction)
        self._compress(direction)
        self._spawn_random()
        self._color_board()
        message = self._check_win()
        if message == "continue":
            return
        if messagebox.askyesno(title=message, message="Do you want to play again?"):
            for i in range(self._BOARD_SIZE):
                for j in range(self._BOARD_SIZE):
                    self._board[i][j].set("")
            return
        self._root.destroy()
        # TODO: is this line necessary?
        # exit()

    def _end_win(self, _) -> None:
        self._root.destroy()

    def _init_tk(self) -> None:
        self._root.title("2048")
        self._root.bind("<Up>", self._move)
        self._root.bind("<Down>", self._move)
        self._root.bind("<Left>", self._move)
        self._root.bind("<Right>", self._move)
        self._root.bind("w", self._move)
        self._root.bind("s", self._move)
        self._root.bind("a", self._move)
        self._root.bind("d", self._move)
        self._root.bind("q", self._end_win)
        ttk.Style().configure(
            "TLabel",
            font=("Helvetica", 64),
            width=3,
            height=3,
            borderwidth=1,
            relief="ridge",
        )

    def __init__(self) -> None:
        self._root = Tk()
        self._init_tk()
        self._board: list[list[StringVar]] = []
        for i in range(self._BOARD_SIZE):
            self._board.append([])
            for j in range(self._BOARD_SIZE):
                self._board[i].append(StringVar(self._root))
                ttk.Label(
                    self._root,
                    textvariable=self._board[i][j],
                    padding=5,
                    style=f"{i}{j}.TLabel",
                ).grid(
                    row=i,
                    column=j,
                )

    def _spawn_random(self) -> None:
        number = random.choices("24", (0.9, 0.1))[0]
        cell = random.choice(
            [
                (i, j)
                for i in range(self._BOARD_SIZE)
                for j in range(self._BOARD_SIZE)
                if self._board[i][j].get() == ""
            ]
        )
        self._board[cell[0]][cell[1]].set(number)

    def _color_board(self) -> None:
        for i in range(4):
            for j in range(4):
                ttk.Style().configure(
                    f"{i}{j}.TLabel",
                    background=self._COLORS[self._board[i][j].get()],
                    foreground=self._FG_COLOR,
                )

    def run(self) -> None:
        """Start 2048 game"""
        self._spawn_random()
        self._spawn_random()
        self._color_board()
        self._root.mainloop()


if __name__ == "__main__":
    Game().run()
