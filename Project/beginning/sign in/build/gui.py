
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\LAPTOP\Desktop\smart music player\sign in\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.configure(bg="#FFFFFF")
width = 1000
height = 600
window.geometry("{}x{}".format(width, height))

# Get the width and height of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y positions of the window to center it on the screen
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

# Set the position of the window
window.geometry("+{}+{}".format(x, y))





title_bar = tk.Frame(window, bg="#1DB954", height=50, relief="flat", bd=0)
title_bar.pack(side="top", fill="x")

title_label = tk.Label(title_bar, text="My App", font=("Helvetica", 16), bg="#1DB954", fg="white")
title_label.place(relx=0.5, rely=0.5, anchor="center")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    750.0,
    300.0,
    image=image_image_1
)

canvas.create_rectangle(
    0.0,
    0.0,
    500.0,
    600.0,
    fill="#FFFCFC",
    outline="")

canvas.create_text(
    590.0,
    253.0,
    anchor="nw",
    text="Experience music like never\nbefore with our smart player\n powered by AI",
    fill="#FFFCFC",
    font=("Poppins Bold", 28 * -1)
)

canvas.create_text(
    102.0,
    526.0,
    anchor="nw",
    text="Don’t have an account? Sign Up",
    fill="#000000",
    font=("Poppins Regular", 14 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=102.0,
    y=480.0,
    width=135.0,
    height=46.19769287109375
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    267.51231384277344,
    433.73765563964844,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F1F1F1",
    fg="#9E9E9E",
    font=("Poppins Regular", 22 * -1),
    show="*",
    highlightthickness=0
)
entry_1.place(
    x=119.73765563964844,
    y=408.0,
    width=295.54931640625,
    height=49.475311279296875
)

def remove_placeholder_text(text):
    if len(text) > 0:
        userName_placeholder.config(text="")
        userName_placeholder.place_configure(x=113)
    else:
        userName_placeholder.config(text="Please enter your password")
        userName_placeholder.place_configure(x=122)


entry_1.bind('<KeyRelease>', lambda e: remove_placeholder_text(entry_1.get()))



userName_placeholder = tk.Label(window, text="Please enter your password", fg="#CDCDCD", font=("Poppins Regular", 22 * -1))
userName_placeholder.place(x=122, y=420)
userName_placeholder.bind('<Button-1>', lambda e: entry_1.focus())

'''canvas.create_text(
    112.31034851074219,
    421.95074462890625,
    anchor="nw",
    text="Please enter your password",
    fill="#000000",
    font=("Poppins Regular", 22 * -1)
)'''

canvas.create_text(
    102.0,
    346.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Poppins Regular", 28 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    271.0756378173828,
    299.26622009277344,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F1F1F1",
    fg="#9E9E9E",
    font=("Poppins Regular", 22 * -1),
    highlightthickness=0
)
entry_2.place(
    x=120.26622009277344,
    y=273.0,
    width=301.61883544921875,
    height=50.532440185546875
)
def remove_placeholder_text2(text):
    if len(text) > 0:

        userName2_placeholder.config(text="")
        userName2_placeholder.place_configure(x=113)
    else:
        userName2_placeholder.config(text="Please enter your password")
        userName2_placeholder.place_configure(x=122)


entry_2.bind('<KeyRelease>', lambda e: remove_placeholder_text2(entry_2.get()))



userName2_placeholder = tk.Label(window, text="Please enter your email", fg="#CDCDCD", font=("Poppins Regular", 22 * -1))
userName2_placeholder.place(x=122, y=286)
userName2_placeholder.bind('<Button-1>', lambda e: entry_2.focus())

'''canvas.create_text(
    112.69798278808594,
    286.355712890625,
    anchor="nw",
    text="Please enter your email",
    fill="#000000",
    font=("Poppins Regular", 22 * -1)
)'''

canvas.create_text(
    102.0,
    211.0,
    anchor="nw",
    text="Email ",
    fill="#000000",
    font=("Poppins Regular", 28 * -1)
)

canvas.create_text(
    94.0,
    151.0,
    anchor="nw",
    text="Sign in",
    fill="#285689",
    font=("Poppins Bold", 36 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    144.0,
    103.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()
