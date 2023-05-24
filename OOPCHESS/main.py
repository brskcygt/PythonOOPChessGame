from chess.game.game import ChessGame
from chess.render.render import *

import tkinter as tk
from tkinter import *

import pathlib
path = pathlib.Path().resolve()

def tkinter_start():

    root.destroy()
    object = ChessGame(WindowRender())
    object.run()

root = tk.Tk()

root.geometry("500x500")
root.resizable(False, False)
root.title("Chess Game")
bg= PhotoImage(file=f"{path}\chess_background.png")
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

Button(root, text="Oyna", command=tkinter_start, height=3, width=12,bg= "white").place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()
