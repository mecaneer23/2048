#!/usr/bin/env python3
"""2048 game using tkinter"""

from dataclasses import dataclass
from enum import Enum
from random import choice, choices
from tkinter import Event, StringVar, Tk, messagebox, ttk


class Direction(Enum):
    """Enum to store which movement key was most recently pressed"""

    DOWN = "down"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    NONE = ""


@dataclass
class RangeData:
    """Hold data based on given directions"""

    i_range: range
    j_range: range


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
    _RANGE_DATA = {
        Direction.UP: RangeData(range(1, _BOARD_SIZE), range(_BOARD_SIZE)),
        Direction.DOWN: RangeData(range(_BOARD_SIZE - 2, -1, -1), range(_BOARD_SIZE)),
        Direction.LEFT: RangeData(range(_BOARD_SIZE), range(1, _BOARD_SIZE)),
        Direction.RIGHT: RangeData(range(_BOARD_SIZE), range(_BOARD_SIZE - 2, -1, -1)),
    }

    def _merge(self, direction: Direction) -> None:
        i_addend = int(direction == Direction.DOWN) - int(direction == Direction.UP)
        j_addend = int(direction == Direction.RIGHT) - int(direction == Direction.LEFT)
        range_data = self._RANGE_DATA[direction]
        for i in range_data.i_range:
            for j in range_data.j_range:
                if (
                    self._board[i][j].get() != ""
                    and self._board[i + i_addend][j + j_addend].get() != ""
                    and self._board[i][j].get()
                    == self._board[i + i_addend][j + j_addend].get()
                ):
                    self._board[i][j].set(str(int(self._board[i][j].get()) * 2))
                    self._board[i + i_addend][j + j_addend].set("")

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

    def _compress(self, direction: Direction) -> None:
        i_addend = int(direction == Direction.DOWN) - int(direction == Direction.UP)
        j_addend = int(direction == Direction.RIGHT) - int(direction == Direction.LEFT)
        range_data = self._RANGE_DATA[direction]
        # TODO: iterate in the opposite direction so each element isn't checked twice
        for _ in range(
            self._BOARD_SIZE - 1
        ):  # hack to ensure elements are moved over all the way
            for i in range_data.i_range:
                for j in range_data.j_range:
                    current_elem = self._board[i][j]
                    check_elem = self._board[i + i_addend][j + j_addend]
                    if current_elem.get() != "" and check_elem.get() == "":
                        check_elem.set(current_elem.get())
                        current_elem.set("")

    def _move(self, key: Event) -> None:
        key_symbol = key.keysym
        direction = Direction.NONE
        if key_symbol in ("Up", "w"):
            direction = Direction.UP
        elif key_symbol in ("Down", "s"):
            direction = Direction.DOWN
        elif key_symbol in ("Left", "a"):
            direction = Direction.LEFT
        elif key_symbol in ("Right", "d"):
            direction = Direction.RIGHT
        if direction == Direction.NONE:
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
        number = choices("24", (0.9, 0.1))[0]
        cell = choice(
            [
                (i, j)
                for i in range(self._BOARD_SIZE)
                for j in range(self._BOARD_SIZE)
                if self._board[i][j].get() == ""
            ]
        )
        self._board[cell[0]][cell[1]].set(number)

    def _color_board(self) -> None:
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
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
