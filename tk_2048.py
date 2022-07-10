#!/usr/bin/env python3

from tkinter import Tk, ttk, StringVar
import random


def main():
    def move(direction):
        direction = direction.keycode
        if direction in (38, 87):
            direction = "up"
        elif direction in (40, 83):
            direction = "down"
        elif direction in (37, 65):
            direction = "left"
        elif direction in (39, 68):
            direction = "right"
        print(direction)
        spawn_random()
        compress(direction)
        merge(direction)
        compress(direction)
        check_win()
        color_board()

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
                if vars[i][j].get() == 2048:
                    print("You win!")
                    root.destroy()
        if all(vars[i][j].get() for i in range(4) for j in range(4)):
            print("You lose!")
            root.destroy()

    def color_board():
        for i in range(4):
            for j in range(4):
                if vars[i][j].get() == "":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#ffffff", foreground="#000000")
                elif vars[i][j].get() == "2":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#eee4da", foreground="#000000")
                elif vars[i][j].get() == "4":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#ede0c8", foreground="#000000")
                elif vars[i][j].get() == "8":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#f2b179", foreground="#000000")
                elif vars[i][j].get() == "16":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#f59563", foreground="#000000")
                elif vars[i][j].get() == "32":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#f67c5f", foreground="#000000")
                elif vars[i][j].get() == "64":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#f65e3b", foreground="#000000")
                elif vars[i][j].get() == "128":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#edcf72", foreground="#000000")
                elif vars[i][j].get() == "256":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#edcc61", foreground="#000000")
                elif vars[i][j].get() == "512":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#edc850", foreground="#000000")
                elif vars[i][j].get() == "1024":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#edc53f", foreground="#000000")
                elif vars[i][j].get() == "2048":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#edc22e", foreground="#000000")
                elif vars[i][j].get() == "4096":
                    ttk.Style().configure(f"{i}{j}.TLabel", background="#000000", foreground="#ffffff")

    spawn_random()
    spawn_random()
    color_board()
    root.mainloop()


if __name__ == "__main__":
    main()
