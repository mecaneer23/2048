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

    def _move(self, direction: Event) -> None:
        raise NotImplementedError("move")

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
        self._root.bind("q", self._root.destroy)

    def __init__(self) -> None:
        self._root = Tk()
        self._board: list[list[StringVar]] = []
        for i in range(self._BOARD_SIZE):
            self._board.append([])
            for j in range(self._BOARD_SIZE):
                self._board[i].append(StringVar(self._root))
                ttk.Label(
                    self._root,
                    textvariable=self._board[i][j],
                    padding=5,
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
