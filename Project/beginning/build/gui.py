
import tkinter as tk
from PIL import Image, ImageTk


def center_window_popUp(root, app_width, app_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (app_width/2)
    y = (screen_height/2) - (app_height/2)
    root.geometry(f'{app_width}x{app_height} + {x} + {y}')

class AnimatedSplashWindow:

    def __init__(self, master, gif_file):
        self.master = master
        self.gif_file = gif_file
        self.gif = None

        self.label = tk.Label(self.master)
        self.label.pack(fill=tk.BOTH, expand=tk.YES)

        self.animate()

    def animate(self):
        if self.gif is None:
            self.gif = Image.open(self.gif_file)
        try:
            self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            self.gif.seek(0)
        self.resized_gif = self.gif.resize((800, 533))
        self.photo = ImageTk.PhotoImage(self.resized_gif)
        self.label.config(image=self.photo)
        self.master.after(100, self.animate)

# Create the Tkinter window
root = tk.Tk()
width = 800
height = 533
root.geometry("{}x{}".format(width, height))


# Get the width and height of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y positions of the window to center it on the screen
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

# Set the position of the window
root.geometry("+{}+{}".format(x, y))

root.overrideredirect(True)

# Create the animated splash screen
splash_window = AnimatedSplashWindow(root, "D:/college/GP/ALAA/build/assets/cover.gif")

def mainWindow():
    root.destroy()
    

# Show the splash screen for 5 seconds
root.after(5000, mainWindow)

# Create the main application window
main_window = tk.Frame(root)
main_window.pack(fill=tk.BOTH, expand=tk.YES)
# Add widgets to the main window here...

# Run the Tkinter event loop
root.mainloop()