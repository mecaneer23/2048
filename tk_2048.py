#!/usr/bin/env python3

from tkinter import Tk, ttk, StringVar, messagebox
import random


def main():
    def move(direction):
        direction = direction.keycode
        if direction in (38, 87, 111):
            direction = "up"
        elif direction in (40, 83, 116):
            direction = "down"
        elif direction in (37, 65, 113):
            direction = "left"
        elif direction in (39, 68, 114):
            direction = "right"
        spawn_random()
        compress(direction)
        merge(direction)
        compress(direction)
        color_board()
        message = check_win()
        if message != "continue":
            if messagebox.askyesno(title=message, message="Do you want to play again?"):
                for i in range(4):
                    for j in range(4):
                        vars[i][j].set("")
            else:
                root.destroy()
                exit()

    root = Tk()
    root.title("2048")
    root.bind("<Up>", move)
    root.bind("<Down>", move)
    root.bind("<Left>", move)
    root.bind("<Right>", move)
    root.bind("w", move)
    root.bind("s", move)
    root.bind("a", move)
    root.bind("d", move)
    root.bind("m", lambda x: vars[0][0].set("2048"))

    vars = [[StringVar(root) for _ in range(4)] for _ in range(4)]
    ttk.Style().configure(
        "TLabel",
        font=("Helvetica", 64),
        width=3,
        height=3,
        borderwidth=1,
        relief="ridge",
    )
    [
        [
            ttk.Label(root, textvariable=vars[i][j], padding=5, style=f"{i}{j}.TLabel").grid(row=i, column=j)
            for j in range(4)
        ]
        for i in range(4)
    ]

    def spawn_random():
        number = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        cell = random.choice(
            [(i, j) for i in range(4) for j in range(4) if vars[i][j].get() == ""]
        )
        vars[cell[0]][cell[1]].set(number)

    def compress(direction):
        if direction == "down":
            for j in range(4):
                for i in range(3):
                    if vars[i][j].get() != "" and vars[i + 1][j].get() == "":
                        vars[i + 1][j].set(vars[i][j].get())
                        vars[i][j].set("")
        elif direction == "up":
            for j in range(4):
                for i in range(3, 0, -1):
                    if vars[i][j].get() != "" and vars[i - 1][j].get() == "":
                        vars[i - 1][j].set(vars[i][j].get())
                        vars[i][j].set("")
        elif direction == "right":
            for i in range(4):
                for j in range(3):
                    if vars[i][j].get() != "" and vars[i][j + 1].get() == "":
                        vars[i][j + 1].set(vars[i][j].get())
                        vars[i][j].set("")
        elif direction == "left":
            for i in range(4):
                for j in range(3, 0, -1):
                    if vars[i][j].get() != "" and vars[i][j - 1].get() == "":
                        vars[i][j - 1].set(vars[i][j].get())
                        vars[i][j].set("")

    def merge(direction):
        if direction == "up":
            for j in range(4):
                for i in range(3):
                    if (
                        vars[i][j].get() != ""
                        and vars[i + 1][j].get() != ""
                        and vars[i][j].get() == vars[i + 1][j].get()
                    ):
                        vars[i][j].set(int(vars[i][j].get()) * 2)
                        vars[i + 1][j].set("")
        elif direction == "down":
            for j in range(4):
                for i in range(3, 0, -1):
                    if (
                        vars[i][j].get() != ""
                        and vars[i - 1][j].get() != ""
                        and vars[i][j].get() == vars[i - 1][j].get()
                    ):
                        vars[i][j].set(int(vars[i][j].get()) * 2)
                        vars[i - 1][j].set("")
        elif direction == "left":
            for i in range(4):
                for j in range(3):
                    if (
                        vars[i][j].get() != ""
                        and vars[i][j + 1].get() != ""
                        and vars[i][j].get() == vars[i][j + 1].get()
                    ):
                        vars[i][j].set(int(vars[i][j].get()) * 2)
                        vars[i][j + 1].set("")
        elif direction == "right":
            for i in range(4):
                for j in range(3, 0, -1):
                    if (
                        vars[i][j].get() != ""
                        and vars[i][j - 1].get() != ""
                        and vars[i][j].get() == vars[i][j - 1].get()
                    ):
                        vars[i][j].set(int(vars[i][j].get()) * 2)
                        vars[i][j - 1].set("")

    def check_win():
        for i in range(4):
            for j in range(4):
                if vars[i][j].get() == "2048":
                    return "You win!"
        if all(vars[i][j].get() for i in range(4) for j in range(4)):
            return "You lose!"
        return "continue"

    def color_board():
        for i in range(4):
            for j in range(4):
                ttk.Style().configure(
                    f"{i}{j}.TLabel",
                    background={
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
                        "2048": "#edc22e"
                    }[vars[i][j].get()],
                    foreground="#000000")

    spawn_random()
    spawn_random()
    color_board()
    root.mainloop()


if __name__ == "__main__":
    main()
