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

    @staticmethod
    def _get_addends(direction: str) -> tuple[int, int]:
        return {
            "down": 1,
            "up": -1,
            "left": 0,
            "right": 0,
        }[direction], {
            "down": 0,
            "up": 0,
            "left": -1,
            "right": 1,
        }[direction]

    def _compress(self, direction: str) -> None:
        i_addend, j_addend = self._get_addends(direction)
        range_obj = (
            range(self._BOARD_SIZE - 1, 0, -1)
            if direction in ("up", "left")
            else range(self._BOARD_SIZE - 1)
        )
        for j in range(self._BOARD_SIZE):
            for i in range_obj:
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
        i_addend, j_addend = self._get_addends(direction)
        j_addend = - j_addend
        if direction == "up":
            for j in range(4):
                for i in range(3):
                    if (
                        self._board[i][j].get() != ""
                        and self._board[i + 1][j].get() != ""
                        and self._board[i][j].get() == self._board[i + 1][j].get()
                    ):
                        self._board[i][j].set(int(self._board[i][j].get()) * 2)
                        self._board[i + 1][j].set("")
        elif direction == "down":
            for j in range(4):
                for i in range(3, 0, -1):
                    if (
                        self._board[i][j].get() != ""
                        and self._board[i - 1][j].get() != ""
                        and self._board[i][j].get() == self._board[i - 1][j].get()
                    ):
                        self._board[i][j].set(int(self._board[i][j].get()) * 2)
                        self._board[i - 1][j].set("")
        elif direction == "left":
            for i in range(4):
                for j in range(3):
                    if (
                        self._board[i][j].get() != ""
                        and self._board[i][j + 1].get() != ""
                        and self._board[i][j].get() == self._board[i][j + 1].get()
                    ):
                        self._board[i][j].set(int(self._board[i][j].get()) * 2)
                        self._board[i][j + 1].set("")
        elif direction == "right":
            for i in range(4):
                for j in range(3, 0, -1):
                    if (
                        self._board[i][j].get() != ""
                        and self._board[i][j - 1].get() != ""
                        and self._board[i][j].get() == self._board[i][j - 1].get()
                    ):
                        self._board[i][j].set(int(self._board[i][j].get()) * 2)
                        self._board[i][j - 1].set("")

    def _move(self, direction: Event) -> None:
        direction = direction.keycode
        if direction in (38, 87, 111):
            direction = "up"
        elif direction in (40, 83, 116):
            direction = "down"
        elif direction in (37, 65, 113):
            direction = "left"
        elif direction in (39, 68, 114):
            direction = "right"
        self._spawn_random()
        self._compress(direction)
        self._merge(direction)
        self._compress(direction)
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
