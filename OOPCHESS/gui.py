from tkinter import *

root = Tk()
root.geometry("1040x640")
root.title("Chess Game")
root.resizable(False,False)
root.configure(bg="#ece0d1")

left_frame = Frame(
    root,
    bg = "#ece0d1",
    width = 200,
    height= 640
)
left_frame.place(x=0, y=0)

right_frame = Frame(
    root,
    bg = "#ece0d1",
    width = 200,
    height= 640
)
right_frame.place(x=840, y=0)

#chess board
canvas = Canvas(root, width = 640, height=640)
color = True

for x in range(0,561,80):
    for y in range(0,561,80):
        if color == True:
            canvas.create_rectangle(x,y,x+80,y+80,fill="#dbc1ac")
        else:
            canvas.create_rectangle(x,y,x+80,y+80,fill="#967259")
        color = not color
    color = not color

canvas.pack() 


root.mainloop()