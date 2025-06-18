from tkinter import *
from pathlib import Path
import pypyodbc as odbc
import pandas as pd
import tkinter.messagebox as messagebox
import tkinter as tk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ACTIVE,END,Listbox
import tkinter as tk
from pygame import mixer
import os
from mutagen.mp3 import MP3
import time
from tkinter import ttk
import re
import sqlite3
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ACTIVE,END,Listbox
import tkinter as tk
from pygame import mixer
import os
from mutagen.mp3 import MP3
import time
from tkinter import ttk
import pyodbc as odbc
import re
import random
from datetime import datetime, timedelta
import lyricsgenius
import keras_nlp
import keras
from keras_nlp.models.task import Task
driver_name = "SQL SERVER"
server_name = "localhost\SQLEXPRESS"
Database_Name = "SmartMusicPlayer"
connection_string = f"""
    DRIVER={{{driver_name}}};
    SERVER={server_name};
    DATABASE={Database_Name};
    Trust_Connection = yes;
"""
connection = odbc.connect(connection_string)
print(connection)

################################################## MODEL #################################################################
CLASSIFYING_THRESHOLD=0.7
LYRICS_RETRIEVAL_TRYS=5
genius = lyricsgenius.Genius("0NcFEOg-YopNwxBQrZjTvZ5Cqm07LUvIerQOsxYL6pKcqjtvzZycw1Wc5H97j1-J")
preprocessor = keras_nlp.models.DistilBertPreprocessor.from_preset("distil_bert_base_en_uncased",sequence_length=20)
def getLyrics(songName,artist):
    i=0
    songLyrics=None
    while i<LYRICS_RETRIEVAL_TRYS : 
        try :
            i=i+1
            song = genius.search_song(songName, artist)
            if song is not None :
                songLyrics=song.lyrics
                print("Found")
                break
        except :
            print("Trying Again")
            pass
    if i == LYRICS_RETRIEVAL_TRYS:
        return "Not Found"
    else:
        return songLyrics
def classifySong(songName,artist):
    songLyrics=getLyrics(songName,artist)
    if songLyrics is not None :
        songLyrics = songLyrics.split()
        n = 100
        inputModel = [' '.join(songLyrics[i:i+n]) for i in range(0,len(songLyrics),n)]
        return getLabel(inputModel)
    else:
        return "Not Found"
def remove_marks(input_string):
    marks = ['!', '?','@','$','%','^','&','*','(',')','[',']']

    return "".join((char for char in input_string if char not in marks and not char.isdigit()))


def getLabel(inputModel): # Takes Lyrics Segments and return label
    Preprocessed_Inputs=preprocessor(inputModel)
    Prediction_Inputs = classifier.predict(Preprocessed_Inputs)
    for prediction in Prediction_Inputs :
        if prediction > CLASSIFYING_THRESHOLD:
            return 1
    return 0

def getPredictions(inputModel):
  Preprocessed_Inputs=preprocessor(inputModel)
  Predictions = classifier.predict(Preprocessed_Inputs)
  for i in range(0,len(Predictions)):
    print(inputModel[i],"->",Predictions[i],"->","True" if Predictions[i] > CLASSIFYING_THRESHOLD else "False","\n")
  print("Average : ",np.sum(Predictions)/len(Predictions))


def delete_text_in_parentheses(text):
    pattern = r'\([^)]*\)'
    return re.sub(pattern, '', text)
def delete_text_in_brackets(text):
    pattern = r'\[[^\]]*\]'
    return re.sub(pattern, '', text)
def PreprocessInput(lyrics):
  return delete_text_in_parentheses(delete_text_in_brackets(lyrics))


def distilbert_kernel_initializer(stddev=0.02):
    return keras.initializers.TruncatedNormal(stddev=stddev)

class myClassifier(Task):
  def __init__(
      self,backbone,dropout=0.45,preprocessor=None,**kwargs
  ):

    inputs = backbone.input

    cls = backbone(inputs)[:, backbone.cls_token_index, :]

    x = keras.layers.Dense(
              768,
              activation="relu",
              kernel_initializer=distilbert_kernel_initializer(),
              name="pooled_dense",
          )(cls)

    x = keras.layers.Dense(
              512,
              activation="relu",
              kernel_initializer=distilbert_kernel_initializer(),
              name="pooled_dense1",
          )(cls)

    x = keras.layers.Dropout(dropout, name="classifier_dropout")(x)

    outputs = keras.layers.Dense(
              1,
              kernel_initializer=distilbert_kernel_initializer(),
              name="output_layer",
              activation="sigmoid"
          )(x)
    super().__init__(
              inputs=inputs,
              outputs=outputs,
              include_preprocessing=preprocessor is not None,
              **kwargs,
          )
    self.backbone = backbone
    self.preprocessor = preprocessor

backbone = keras_nlp.models.DistilBertBackbone.from_preset("distil_bert_base_en_uncased")
classifier = myClassifier(backbone,preprocessor=None,dropout=0.2)
classifier.backbone.trainable = False

def cleanLyrics(lyrics,songname):
    return lyrics[lyrics.find(songname):]

classifier.compile(
    loss=keras.losses.BinaryCrossentropy(),
    optimizer=keras.optimizers.SGD(),
    metrics=['accuracy','Recall'],
)

classifier.load_weights("D:\\college\\GP\\project\\HateSpeech-5-NoBackbone\\")
#classifySong("Woman", "Doja Cat")






#################################################### SIGN UP ###################################################
def signup():
    signup_win = Tk()
    signup_win.configure(bg="#FFFFFF")
    width = 1000
    height = 600
    signup_win.geometry("{}x{}".format(width, height))

    OUTPUT_PATH = os.path.dirname(os.path.abspath("_file_"))
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\college\\GP\\Project\\sign up\\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Get the width and height of the screen
    screen_width = signup_win.winfo_screenwidth()
    screen_height = signup_win.winfo_screenheight()

    # Calculate the x and y positions of the window to center it on the screen
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the position of the window
    signup_win.geometry("+{}+{}".format(x, y))

    canvas = Canvas(
        signup_win,
        bg="#FFFFFF",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        250.0,
        300.0,
        image=image_image_1
    )

    canvas.create_text(
        76.0,
        253.0,
        anchor="nw",
        text="Experience music like never\nbefore with our smart player\n powered by AI",
        fill="#FFFCFC",
        font=("Poppins Bold", 28 * -1)
    )

    canvas.create_rectangle(
        500.0,
        0.0,
        1000.0,
        600.0,
        fill="#FFFCFC",
        outline="")

    logo_image = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        644.0,
        74.0,
        image=logo_image
    )

    canvas.create_text(
        594.0,
        129.0,
        anchor="nw",
        text="Register your account",
        fill="#3E4772",
        font=("Poppins Bold", 30 * -1)
    )

    email_entry_image = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    email_entry_bg = canvas.create_image(
        771.0756225585938,
        245.26622009277344,
        image=email_entry_image
    )
    email_entry = Entry(
        bd=0,
        bg="#F1F1F1",
        fg="#9E9E9E",
        font=("Poppins Regular", 22 * -1),
        highlightthickness=0
    )
    email_entry.place(
        x=620.2662200927734,
        y=219.0,
        width=301.6188049316406,
        height=50.532440185546875
    )

    canvas.create_text(
        855.0,
        186.0,
        anchor="nw",
        text="Email ",
        fill="#000000",
        font=("Poppins Regular", 22 * -1)
    )

    canvas.create_text(
        675.0,
        229.0,
        anchor="nw",
        text="Please enter your email",
        fill="#000000",
        font=("Poppins Regular", 22 * -1)
    )

    password_input_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    password_input_bg_1 = canvas.create_image(
        771.0123291015625,
        342.73765563964844,
        image=password_input_image_1
    )
    password_input = Entry(
        bd=0,
        bg="#F1F1F1",
        fg="#9E9E9E",
        font=("Poppins Regular", 22 * -1),
        show="*",
        highlightthickness=0
    )
    password_input.place(
        x=619.7376556396484,
        y=317.0,
        width=302.5493469238281,
        height=49.475311279296875
    )

    canvas.create_text(
        809.0,
        283.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Poppins Regular", 22 * -1)
    )

    canvas.create_text(
        625.0,
        326.0,
        anchor="nw",
        text="Please enter your password",
        fill="#000000",
        font=("Poppins Regular", 22 * -1)
    )

    confirm_password_entry_image = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    confirm_password_entry_bg = canvas.create_image(
        767.5123291015625,
        440.73765563964844,
        image=confirm_password_entry_image
    )
    confirm_password_entry = Entry(
        bd=0,
        bg="#F1F1F1",
        fg="#9E9E9E",
        font=("Poppins Regular", 22 * -1),
        show="*",
        highlightthickness=0
    )
    confirm_password_entry.place(
        x=619.7376556396484,
        y=415.0,
        width=295.5493469238281,
        height=49.475311279296875
    )

    canvas.create_text(
        673.0,
        425.0,
        anchor="nw",
        text="Confirm your password",
        fill="#000000",
        font=("Poppins Regular", 22 * -1)
    )

    canvas.create_text(
        714.0,
        382.0,
        anchor="nw",
        text="Confirm Password",
        fill="#000000",
        font=("Poppins Regular", 22 * -1)
    )

    email_entry.bind(
        '<KeyRelease>', lambda e: remove_placeholder_email_text(email_entry.get()))
    email_placeholder = tk.Label(
        signup_win, text="Please enter your email", fg="#CDCDCD", font=("Poppins Regular", 22 * -1))
    email_placeholder.place(x=698, y=229)
    email_placeholder.bind('<Button-1>', lambda e: email_entry.focus())

    password_input.bind(
        '<KeyRelease>', lambda e: remove_password_placeholder_text(password_input.get()))
    password_placeholder = tk.Label(
        signup_win, text="Please enter your password", fg="#CDCDCD", font=("Poppins Regular", 22 * -1))
    password_placeholder.place(x=655, y=330)
    password_placeholder.bind('<Button-1>', lambda e: password_input.focus())

    confirm_password_entry.bind(
        '<KeyRelease>', lambda e: remove_placeholder_Confirm_Password_text(confirm_password_entry.get()))
    confirm_password_placeholder = tk.Label(
        signup_win, text="Confirm your password", fg="#CDCDCD", font=("Poppins Regular", 22 * -1))
    confirm_password_placeholder.place(x=690, y=425)
    confirm_password_placeholder.bind(
        '<Button-1>', lambda e: confirm_password_entry.focus())

    text_item = canvas.create_text(
        631.0,
        540.0,
        anchor="nw",
        text="Already Registered?",
        fill="#494F7A",
        font=("Poppins Regular", 15 * -1)

    )

    def on_text_click(event):
        signup_win.destroy()
        openlogin()

    canvas.tag_bind(text_item, '<Button-1>', on_text_click)

    submit_button_image = PhotoImage(
        file=relative_to_assets("button_1.png"))
    submit_button = Button(
        image=submit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: retrieveInput(),
        relief="flat"
    )
    submit_button.place(
        x=794.0,
        y=530.0,
        width=135.0,
        height=46.19769287109375
    )
    # Create a label for the age field
    age_label = tk.Label(signup_win, text="Age:")
    age_label.config(bg="#FFFFFF", fg="#000000",
                     font=("Poppins Regular", 22 * -1))
    age_label.place(x=750, y=480)

    # Create an Entry widget for the age field
    age_entry = tk.Entry(signup_win)
    age_entry.place(x=810, y=485)

    def remove_placeholder_email_text(text):
        if len(text) > 0:
            email_placeholder.config(text="")
            email_placeholder.place_configure(x=610)
        else:
            email_placeholder.config(text="Please enter your email")
            email_placeholder.place_configure(x=698)

    def remove_password_placeholder_text(text):
        if len(text) > 0:
            password_placeholder.config(text="")
            password_placeholder.place_configure(x=610)
        else:
            password_placeholder.config(text="Please enter your password")
            password_placeholder.place_configure(x=655)

    def remove_placeholder_Confirm_Password_text(text):
        if len(text) > 0:
            confirm_password_placeholder.config(text="")
            confirm_password_placeholder.place_configure(x=610)
        else:
            confirm_password_placeholder.config(text="Confirm your password")
            confirm_password_placeholder.place_configure(x=690)

    def validateEmail(email):
        # Regular expression pattern for email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def is_email_exists(email):
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM Users WHERE Email = ?"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()[0]
        return result > 0

    def validatePassword(password):
        # Password validation criteria (e.g., minimum length, special characters, etc.)
        min_length = 8
        has_special_char = any(
            char in password for char in "!@#$%^&*()_+{}[]:;<>,.?/~`")

        return len(password) >= min_length and has_special_char

    def retrieveInput():
        emailInput = email_entry.get()
        passwordInput = password_input.get()
        confirmPassword = confirm_password_entry.get()
        ageInput = age_entry.get()

        if not validateEmail(emailInput):
            messagebox.showerror("Error", "Invalid email address")
        elif not validatePassword(passwordInput):
            messagebox.showerror(
                "Error", "Invalid password. Password should be at least 8 characters long and contain special characters.")
        elif passwordInput != confirmPassword:
            messagebox.showerror("Error", "Passwords do not match")
        elif is_email_exists(emailInput):
            messagebox.showerror("Error", "Email already exists")
        else:
            cursor = connection.cursor()
            sql = "INSERT INTO Users (UserName, Email, Password, Age) VALUES (?, ?, ?, ?)"
            val = (emailInput.split("@")[0],
                   emailInput, passwordInput, ageInput)
            cursor.execute(sql, val)
            connection.commit()
            signup_win.destroy()
            openlogin()
    signup_win.resizable(False, False)
    signup_win.mainloop()

#################################################### LOG IN ####################################################
current_user = ""
def openlogin():

    login_win=Tk()
    login_win.title("Robofiy")
    login_win.configure(bg="#FFFFFF")
    width = 1000
    height = 600
    login_win.geometry("{}x{}".format(width, height))

    OUTPUT_PATH = os.path.dirname(os.path.abspath("_file_"))
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\college\\GP\\Project\\Login\\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Get the width and height of the screen
    screen_width = login_win.winfo_screenwidth()
    screen_height = login_win.winfo_screenheight()

    # Calculate the x and y positions of the login_win to center it on the screen
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the position of the login_win
    login_win.geometry("+{}+{}".format(x, y))

    title_bar = tk.Frame(login_win, bg="#1DB954",
                         height=50, relief="flat", bd=0)
    title_bar.pack(side="top", fill="x")

    title_label = tk.Label(title_bar, text="My App", font=(
        "Helvetica", 16), bg="#1DB954", fg="white")
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    canvas = Canvas(
        login_win,
        bg="#FFFFFF",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
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

     #canvas.create_text(
      #  102.0,
      # 526.0,
      #  anchor="nw",
      #  text="Don’t have an account? Sign Up",
      #  fill="#000000",
      #  font=("Poppins Regular", 14 * -1)
    #)

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: retieveInput()

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

    entry_1.bind('<KeyRelease>',
                 lambda e: remove_placeholder_text(entry_1.get()))

    userName_placeholder = tk.Label(login_win, text="Please enter your password", fg="#CDCDCD",
                                    font=("Poppins Regular", 22 * -1))
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

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def remove_placeholder_text2(text):
        if len(text) > 0:

            userName2_placeholder.config(text="")
            userName2_placeholder.place_configure(x=113)
        else:
            userName2_placeholder.config(text="Please enter your password")
            userName2_placeholder.place_configure(x=122)

    entry_2.bind('<KeyRelease>',
                 lambda e: remove_placeholder_text2(entry_2.get()))

    userName2_placeholder = tk.Label(login_win, text="Please enter your email", fg="#CDCDCD",
                                     font=("Poppins Regular", 22 * -1))
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
    text_item3 = canvas.create_text(
        102.0,
        530.0,
        anchor="nw",
        text="Need an Account?",
        fill="#494F7A",
        font=("Poppins Regular", 15 * -1)

    )

    def on_text_click(event):
        login_win.destroy()
        signup()

    canvas.tag_bind(text_item3, '<Button-1>', on_text_click)

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        144.0,
        103.0,
        image=image_image_2
    )
    login_win.resizable(False, False)

    def retieveInput():
        global current_user
        inputValue1 = entry_1.get()
        
        inputValue2 = entry_2.get()
        current_user = inputValue2
        vaildate(inputValue2, inputValue1)
        print(inputValue1, inputValue2)

    cursor = connection.cursor()

    result = pd.read_sql("select * from Users", connection)
    result2 = pd.read_sql("select * from Admin", connection)
    df = pd.DataFrame(result)
    df2 = pd.DataFrame(result2)
    print(result)
    connection.commit()

    def show_warning_box():
        messagebox.showwarning("Invalid Credentials",
                               "Please enter valid email and password.")

    def vaildate(email, password):
        if check_credentials(email, password)=="User":
            login_win.destroy()
            Home()
        elif check_credentials(email, password)=="Admin":
            login_win.destroy()
            AdminHome()
        else:
            show_warning_box()
            print("No")

    def check_credentials(email, password):
        email_match = df['Email'] == email
        password_match = df['Password'] == password
        email_admin= df2['Email'] == email
        password_admin = df2['Password'] == password
        if df[email_match & password_match].shape[0] > 0:
            return "User"
        elif df2[email_admin & password_admin].shape[0] > 0:
            return "Admin"
        else:
            return "false"

    login_win.mainloop()

#################################################### HOME ######################################################
# Initialize the is_playing2 variable to False
is_playing2 = False
prev_song_playing = ["",""]
paused_position = 0  # Initialize paused_position as a global variable
played_song_time = 0
paused_position2 = 0
def Home():
       

    connection = odbc.connect(connection_string)
    print(connection)
    # Create a cursor
    cursor = connection.cursor()
    
    # Retrieve data from the database
    cursor.execute("SELECT SongName, ArtistName, ExplictLabel FROM SongsClassification")
    rows = cursor.fetchall()
    
    # Retrieve data from the database
    cursor.execute("SELECT SongName, ArtistName, ExplictLabel FROM SongsClassification")
    rows = cursor.fetchall()
    
    
    # Define a function that toggles between the play and pause button icons and controls the playback of the music
    
    def toggle_playback():
        global is_playing2
        global paused_position
        global prev_song_playing
        global paused_position2
        
        selected_item = tree.selection()
        if selected_item:
            if not is_playing2:
                # Get the selected song from the playlist
                song_name = return_songName()
                artist_name = return_artistName()
                
                # Retrieve the music path from the database based on the selected song
                cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
                result = cursor.fetchone()
                print(result)
                if result:
                    music_path = result[0]
                    
                    if not (song_name == prev_song_playing[0] and artist_name == prev_song_playing[1]):
                        paused_position = 0
                   
                    prev_song_playing[0] = song_name
                    prev_song_playing[1] = artist_name
                    # Load and play the music
                    mixer.music.load(music_path)
                    print( "heereee is the pause beforeplay")
                    print(paused_position)
                    mixer.music.play(start=paused_position)
                    
                    # Update the song duration, name, album, time, etc.
                    duration_text.config(text=music_duration())
                    active_song_name.config(text=limit_the_text_length())
                    active_song_album.config(text=limit_the_album_length())
                    

                    
                        
                    
                    
                    # Update the explict icon visibility
                    update_icon_visibility()
                    
                    # Change the button icon to the pause icon
                    play_button.place_forget()
                    pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                    
                    is_playing2 = True
                    update_active_song_time()
                    update_time_bar()
            else:
                
                mixer.music.pause()
                # Store the current position
                print(paused_position2)
                paused_position += paused_position2

                current_time_convertion =  time.strftime('%M:%S',time.gmtime(paused_position))
                active_song_time.config(text = current_time_convertion)
                # Pause the music
                
                current_time_convertion =  time.strftime('%M:%S',time.gmtime(paused_position))
                print("here is when its paused")
                print("")
                active_song_time.config(text= current_time_convertion)
                
                print("this is when the song is paused")
                print(current_time_convertion)
                
                # Change the button icon to the play icon
                pause_button.place_forget()
                play_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = False
                active_song_time.config(text= current_time_convertion)
            
        else:
            item_id = tree.get_children()[0]
            tree.selection_set(item_id)
            tree.focus(item_id)
            
            # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                if not (song_name == prev_song_playing[0] and artist_name == prev_song_playing[1]):
                    paused_position = 0
               
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                # Load and play the music
                mixer.music.load(music_path)
                print( "heereee is the pause beforeplay")
                print(paused_position)
                mixer.music.play(start=paused_position)
                
                # Update the song duration, name, album, time, etc.
                duration_text.config(text=music_duration())
                active_song_name.config(text=limit_the_text_length())
                active_song_album.config(text=limit_the_album_length())
                
                    
                
                
                # Update the explict icon visibility
                update_icon_visibility()
                
                # Change the button icon to the pause icon
                play_button.place_forget()
                pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = True
                
                update_active_song_time()
                update_time_bar()
                
            else:
                # Pause the music
                
                mixer.music.pause()
                paused_position += paused_position2
                # Change the button icon to the play icon
                pause_button.place_forget()
                play_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = False
                
                
    def play_button_playlist():
        global is_playing2
        global paused_position
        
        item_id = tree.get_children()[0]
        tree.selection_set(item_id)
        tree.focus(item_id)
        
        # Load and play the next song in the playlist
        the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
        selected_song = the_nextSong_toPlay
        
        #get the song name and artist name to quary the path of the next song
        song_name = the_nextSong_toPlay["values"][0]
        artist_name = the_nextSong_toPlay["values"][1]
        
        
        
        # Retrieve the music path from the database based on the selected song
        cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
        result = cursor.fetchone()
        print(result)
        if result:
            music_path = result[0]
            
            prev_song_playing[0] = song_name
            prev_song_playing[1] = artist_name
            
            
            paused_position = 0
            
            
            
            
            # Load and play the music
            mixer.music.load(music_path)
            mixer.music.play()
            
            # Update the song duration, name, album, time, etc.
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
                
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            
            update_active_song_time()
            update_time_bar()
        
    
    def play_rondom_song():
        global is_playing2
        global paused_position
        
        # Get all the children (songs) in the tree
        children = tree.get_children()
        
        if children:
            # Select a random song from the tree
            random_song = random.choice(children)
            
            # Select and focus the random song in the tree
            tree.selection_set(random_song)
            tree.focus(random_song)
            
            # Load and play the random song
            selected_song = tree.item(random_song)
            song_name = selected_song["values"][0]
            artist_name = selected_song["values"][1]
            
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
                
                
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
                
                # Update the song duration, name, album, time, etc.
                duration_text.config(text=music_duration())
                active_song_name.config(text=limit_the_text_length())
                active_song_album.config(text=limit_the_album_length())
                
                    
                # Update the explicit icon visibility
                update_icon_visibility()
                
                # Change the button icon to the pause icon
                play_button.place_forget()
                pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = True
                update_active_song_time_whensshuffleButton()
                update_time_bar()
    
    def play_next_song():
        global prev_song_playing
        global paused_position
        global is_playing2
        # Get the index of the currently selected song in the playlist
        selected_item = tree.selection()
        if selected_item:
            current_song_index = tree.index(selected_item)
            # Increment the index to get the index of the next song
            next_song_index = current_song_index + 1
            # Wrap around to the beginning of the playlist if necessary
            tree_size = len(tree.get_children())
            print("tree size is :::")
            print(tree_size)
            if next_song_index >= tree_size:
                next_song_index = 0
            # Select the next song in the playlist
            tree.selection_remove(tree.selection())
            item_id = tree.get_children()[next_song_index]
            tree.selection_set(item_id)
            tree.focus(item_id)
          # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[next_song_index]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            update_active_song_time()
            update_time_bar()
            
        else:
            
            item_id = tree.get_children()[0]
            tree.selection_set(item_id)
            tree.focus(item_id)
            
            # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            prev_song_playing[0] = song_name
            prev_song_playing[1] = artist_name
            
            
            paused_position = 0
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            update_active_song_time()
            update_time_bar()
    
            
    
    
    def play_prev_song():
        global prev_song_playing
        global paused_position
        global is_playing2
        
        # Get the index of the currently selected song in the playlist
        selected_item = tree.selection()
        if selected_item:
            current_song_index = tree.index(selected_item)
            # Increment the index to get the index of the next song
            next_song_index = current_song_index - 1
            # Wrap around to the beginning of the playlist if necessary
            tree_size = len(tree.get_children())
            print("tree size is :::")
            print(tree_size)
            if next_song_index < 0:
                next_song_index = tree_size-1
            # Select the next song in the playlist
            tree.selection_remove(tree.selection())
            item_id = tree.get_children()[next_song_index]
            tree.selection_set(item_id)
            tree.focus(item_id)
          # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[next_song_index]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                music_path = result[0]
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            update_active_song_time()
            update_time_bar()
            
        else:
            item_id = tree.get_children()[0]
            tree.selection_set(item_id)
            tree.focus(item_id)
            
            # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                music_path = result[0]
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
        
            update_active_song_time()
            update_time_bar()
        
    
    
    
    OUTPUT_PATH = os.path.dirname(os.path.abspath("__file__"))
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\college\\GP\\Project\\Home\\frame0")
    
    
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    class ImageListbox(tk.Listbox):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.images = []
    
        def insert(self, index, *elements, image=None):
            super().insert(index, *elements)
            self.images.insert(index, image)
            self.itemconfig(index, image=image, compound="left")
    
    
    window = Tk()
    window.title("ROBIFY")
    
    window.geometry("1200x700")
    window.configure(bg = "#FFFFFF")
    
    # Initialize the mixer module
    mixer.init()
    
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        1.0,
        190.0,
        703.0,
        fill="#EAEAEA",
        outline="")
    
    canvas.create_rectangle(
        190.0,
        97.0,
        191.0,
        897.0,
        fill="#CCCCCC",
        outline="")
    
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        112.0,
        127.0,
        image=image_image_1
    )
    
    

    
    canvas.create_rectangle(
        191.0,
        1.0,
        1200.0,
        53.0,
        fill="#F4F4F4",
        outline="")
    #------------------------------------the olaylist look------------------------------------------
    canvas.create_text(
        640.0,
        21.0,
        anchor="nw",
        text="ROBOFIY",
        fill="#262626",
        font=("SFProDisplay Medium", 16 * -1)
    )
    
    canvas.create_text(
        478.0,
        191.0,
        anchor="nw",
        text="The AI-powered classification algorithm embedded in the music player employs sophisticated techniques to evaluate \nthe lyrics and audio of each song. It utilizes natural language processing (NLP) and machine learning algorithms to \nunderstand the context, tone, and choice of words within the lyrics. By analyzing the song's audio and lyrics, the AI \ncan accurately determine whether the song contains explicit content or is safe for all audiences.",
        fill="#808080",
        font=("SFProDisplay Regular", 13 * -1)
    )
    
    canvas.create_text(
        479.0,
        104.0,
        anchor="nw",
        text="ROBOFIY Music",
        fill="#262626",
        font=("SFProDisplay Medium", 24 * -1)
    )
    
    canvas.create_text(
        473.0,
        135.0,
        anchor="nw",
        text="Robofiy smart music player playList",
        fill="#285689",
        font=("AndadaProRoman Regular", 24 * -1)
    )
    
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command = play_rondom_song,
        relief="flat"
    )
    button_1.place(
        x=646.0,
        y=257.0,
        width=153.0,
        height=28.0
    )
    
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command = play_button_playlist,
        relief="flat"
    )
    button_2.place(
        x=479.0,
        y=257.0,
        width=153.0,
        height=28.0
    )
    
    
    canvas.create_rectangle(
        213.0,
        334.0,
        1200.0,
        389.0,
        fill="#FAFAFA",
        outline="")
    
    
    
    
    #---------------single song-------------
    '''canvas.create_text(
        287.0,
        354.0,
        anchor="nw",
        text="Going Bad (feat. Drake)",
        fill="#262626",
        font=("SFProText Regular", 14 * -1)
    )
    
    canvas.create_text(
        657.0,
        355.0,
        anchor="nw",
        text="Meek Mill",
        fill="#7E7E7E",
        font=("SFProText Regular", 12 * -1)
    )
    
    canvas.create_text(
        926.0,
        354.0,
        anchor="nw",
        text="Championships",
        fill="#7E7E7E",
        font=("SFProText Regular", 12 * -1)
    )
    
    canvas.create_text(
        1157.0,
        356.0,
        anchor="nw",
        text="3:01",
        fill="#7E7E7E",
        font=("SFProText Regular", 12 * -1)
    )
    
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        626.0,
        361.0,
        image=image_image_2
    )
    
    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        258.0,
        361.0,
        image=image_image_3
    )
    
    canvas.create_rectangle(
        213.0,
        442.0,
        1200.0,
        497.0,
        fill="#FAFAFA",
        outline="")
    #--------------------------end---------------------
    '''
    canvas.create_rectangle(
        999.638671875,
        677.5,
        1055.505615234375,
        680.5,
        fill="#BFBFBF",
        outline="")
    
    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        1058.66796875,
        678.5,
        image=image_image_13
    )
    
    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        1079.0,
        679.0,
        image=image_image_14
    )
    
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=play_prev_song,
        relief="flat"
    )
    button_3.place(
        x=653.0,
        y=636.0,
        width=48.0,
        height=40.0
    )
    
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=play_next_song,
        relief="flat"
    )
    button_4.place(
        x=755.0,
        y=638.0,
        width=45.0,
        height=38.0
    )
    
    
    
    
    '''button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    button_5.place(
        x=707.0,
        y=629.0,
        width=41.0,
        height=61.0
    )
    
    play_Button = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=play_Button,
        borderwidth=0,
        highlightthickness=0,
        command=play_song,
        relief="flat"
    )
    button_6.place(
        x=707.0,
        y=626.0,
        width=46.0,
        height=61.0
    )'''
    
    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        234.0,
        659.0,
        image=image_image_15
    )
    '''
    #the expict label icon
    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        540.0,
        653.0,
        image=image_image_16
    )'''
    #___________playing song___________________
    
    
    canvas.create_rectangle(
        13.0,
        204.0,
        182.0,
        232.0,
        fill="#DFDFDF",
        outline="")
    #-------------------------------the side bar-------------------------------
    canvas.create_text(
    13.0,
    299.0,
    anchor="nw",
    text="Clean mode",
    fill="#7D7D7D",
    font=("AndadaProRoman Bold", 12 * -1)
    )

    canvas.create_text(
        13.0,
        251.0,
        anchor="nw",
        text="here you can usr the clean\n mode(show non-explict songs \nonly).",
        fill="#9F9E9B",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_text(
        13.0,
        299.0,
        anchor="nw",
        text="Clean mode",
        fill="#7D7D7D",
        font=("AndadaProRoman Bold", 12 * -1)
    )

    
    signOut=canvas.create_text(
    13.0,
    316.0,
    anchor="nw",
    text="Sign out",
    fill="#E76D53",
    font=("AndadaProRoman Bold", 12)
    )
    def on_text_click(event):
        window.destroy()
        openlogin()

    canvas.tag_bind(signOut, '<Button-1>', on_text_click)
    
    
    
    
    canvas.create_text(
        632.0,
        306.0,
        anchor="nw",
        text="artist",
        fill="#7F7F7F",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_text(
        213.0,
        306.0,
        anchor="nw",
        text="Song",
        fill="#7F7F7F",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_text(
        926.0,
        306.0,
        anchor="nw",
        text="label",
        fill="#7F7F7F",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_rectangle(
        617.0,
        304.0,
        618.0,
        320.0,
        fill="#E5E5E5",
        outline="")
    
    canvas.create_rectangle(
        911.0,
        304.0,
        912.0,
        320.0,
        fill="#E5E5E5",
        outline="")
    
    image_image_19 = PhotoImage(
        file=relative_to_assets("image_19.png"))
    image_19 = canvas.create_image(
        351.0,
        193.0,
        image=image_image_19
    )  
 
    button_image_13 = PhotoImage(
        file=relative_to_assets("button_13.png"))
    button_13 = Button(
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_13 clicked"),
        relief="flat"
    )
    button_13.place(
        x=53.0,
        y=14.0,
        width=14.0,
        height=14.0
    )
    
    button_image_14 = PhotoImage(
        file=relative_to_assets("button_14.png"))
    button_14 = Button(
        image=button_image_14,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_14 clicked"),
        relief="flat"
    )
    button_14.place(
        x=33.0,
        y=14.0,
        width=14.0,
        height=14.0
    )
    
    button_image_15 = PhotoImage(
        file=relative_to_assets("button_15.png"))
    button_15 = Button(
        image=button_image_15,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_15 clicked"),
        relief="flat"
    )
    button_15.place(
        x=13.0,
        y=14.0,
        width=14.0,
        height=14.0
    )
    
    button_image_16 = PhotoImage(
        file=relative_to_assets("button_16.png"))
    button_16 = Button(
        image=button_image_16,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_16 clicked"),
        relief="flat"
    )
    button_16.place(
        x=213.0,
        y=16.0,
        width=13.0,
        height=21.0
    )
    
    button_image_17 = PhotoImage(
        file=relative_to_assets("button_17.png"))
    button_17 = Button(
        image=button_image_17,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_17 clicked"),
        relief="flat"
    )
    button_17.place(
        x=247.0,
        y=16.0,
        width=14.0,
        height=22.0
    )
    
    # Create a canvas to contain the treeview and scrollbar
    music_frame = tk.Frame(window, width=970, height=277)
    music_frame.place(x=210.0, y=330)
    
    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(music_frame)
    playList = tk.Listbox(music_frame, width=160, height=17, highlightthickness=0, highlightbackground="white", bd=0, yscrollcommand=scrollbar.set)
    tree = ttk.Treeview(music_frame, columns=("SongName", "ArtistName", "ExplicitLabel"), height=14, show="", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both")
    
    # Function to insert a song entry with custom view
    def insert_song_entry(song_name, artist_name, explicit_label):
        # Insert a new row with the song name, artist name, and explicit label
        tree.insert("", tk.END, values=(song_name, artist_name, explicit_label))
    
    # Adjust the column widths
    tree.column("SongName", width=407)
    tree.column("ArtistName", width=295)
    tree.column("ExplicitLabel", width=270)
    
    
    
    
    
  
    
    # Insert the music files into the Listbox
    for row in rows:
        global current_user
        
        cursor.execute("SELECT Age FROM Users WHERE Email = ? ", (current_user,))
        result = cursor.fetchone()
        user_age = int(result[0])
        
        if user_age >= 18:
            song_name = row[0]
            artist_name = row[1]
            explicit_label = row[2]
            # Concatenate the song name, artist name, and explicit label
            temp=""
            if explicit_label == "1":
                temp="Explicit"
            elif explicit_label == "0":
                temp="Non-Explicit"
            insert_song_entry(song_name, artist_name, temp)
            
        else:
            flag = int(row[2])
            if flag == 0:
                song_name = row[0]
                artist_name = row[1]
                explicit_label = row[2]
                # Concatenate the song name, artist name, and explicit label
                insert_song_entry(song_name, artist_name, "Non-Explicit")
        
    def on_tree_select(column):
        # Get the selected item
        selected_item = tree.selection()[0]
    
        # Get the values of the selected item (song_name, artist_name, explicit_label)
        values = tree.item(selected_item, "values")
    
        # Retrieve the song name, artist name, and explicit label from the values
        song_name = values[0]
        artist_name = values[1]
        explicit_label = values[2]
        
        # Return the value based on the specified column index
        if column == 0:
            return song_name
        elif column == 1:
            return artist_name
        elif column == 2:
            return explicit_label
        
        
    
    '''def song_name_without_extension():
        filename_with_extension = os.path.basename(playList.get(ACTIVE))
        filename, extension = os.path.splitext(filename_with_extension)
        return filename
    
    
    def return_song_name_label():
        #assgin the name of the song
        text = song_name_without_extension()
        song_name_only = os.path.splitext(text)[0]
        # Split the song name into two parts
        split_text = song_name_only.split("-")
        #return the name
        song_name_label = split_text[0]
        return song_name_label
    def return_song_album():
        # assgin the name of the song
        text = song_name_without_extension()
        song_name_only = os.path.splitext(text)[0]
        # Split the song name into two parts
        split_text = song_name_only.split("-")
        #return the album
        song_album = split_text[1]
        return song_album
    
    '''
    
    def return_fist_item_inThe_playList():
        first_item = tree.get_children()[0]
        first_item_values = tree.item(first_item, "values")
        return first_item_values
    return_fist_item_inThe_playList()
    
    def return_songName():
        # Get the selected item
        selected_items = tree.selection()
        if selected_items:
            # Get the values of the selected item (song_name, artist_name, explicit_label)
            selected_item = selected_items[0]
            values = tree.item(selected_item, "values")
        
            # Retrieve the song name, artist name, and explicit label from the values
            song_name = values[0]
            return song_name
        
        else:
            selected_items = return_fist_item_inThe_playList()
            song_name = selected_items[0]
            return song_name
    
    def return_artistName():
        # Get the selected item
        selected_items = tree.selection()
        if selected_items:
            # Get the values of the selected item (song_name, artist_name, explicit_label)
            selected_item = selected_items[0]
            values = tree.item(selected_item, "values")
        
            # Retrieve the song name, artist name, and explicit label from the values
            artist_name = values[1]
            return artist_name
        
        else:
            selected_items = return_fist_item_inThe_playList()
            artist_name = selected_items[1]
            return artist_name
    
    def update_icon_visibility():
        print ("hereeeeeeeeeeeeee")
        explicit_label = return_the_explictLabel()
        print(explicit_label)
        if explicit_label == "Explicit":
            icon_label.place(x=540.0, y=640.0)
            print("nooooooooooooooooooooooooooooooooooooooo")
        else:
            icon_label.place_forget()
            
    def return_the_explictLabel():
        # Get the selected item
        selected_items = tree.selection()
        if selected_items:
            # Get the values of the selected item (song_name, artist_name, explicit_label)
            selected_item = selected_items[0]
            values = tree.item(selected_item, "values")
        
            # Retrieve the song name, artist name, and explicit label from the values
            explict_label = values[2]
            return explict_label
        
        else:
            selected_items = return_fist_item_inThe_playList()
            explict_label = selected_items[2]
            return explict_label
    
    
    
    
    def return_active_song_path():
        song_name = return_songName()
        artist_name = return_artistName()
        # Retrieve the music path from the database based on the selected song
        cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
        result = cursor.fetchone()
        music_path = result[0]
        
        return music_path
        
    
    '''def return_the_songName():
        selected_song = playList.get(playList.curselection())
        print(selected_song)
        
        song_artist, explicit_label = selected_song.split(" (")
        song_name, artist_name = song_artist.split(" - ")
        song_name = song_name.strip()
        artist_name = artist_name.strip()
        return song_name
    
    
    def return_the_artistName():
        selected_song = playList.get(playList.curselection())
        print(selected_song)
        
        song_artist, explicit_label = selected_song.split(" (")
        song_name, artist_name = song_artist.split(" - ")
        song_name = song_name.strip()
        artist_name = artist_name.strip()
        return artist_name
     '''   
    def limit_the_text_length():
        # Truncate the text and add "..." if it's too long
        max_length = 20  # Maximum length of text to show
        if len(return_songName()) > max_length:
            truncated_text = return_songName()[:max_length] + "..."
        else:
            truncated_text = return_songName()
    
        return truncated_text
    
    def limit_the_album_length():
        # Truncate the text and add "..." if it's too long
        max_length = 50  # Maximum length of text to show
        if len(return_artistName()) > max_length:
            truncated_text = return_artistName()[:max_length] + "..."
        else:
            truncated_text = return_artistName()
    
        return truncated_text
    
    def music_duration():
        #select the song
        song_mut=MP3(return_active_song_path())
        #get the song length
        song_mut_lenght = song_mut.info.length
        #convert into mins and secs
        song_mut_lenght_convertion = time.strftime('%M:%S',time.gmtime(song_mut_lenght))
        return song_mut_lenght_convertion
    
    def music_current_time():
        global played_song_time
        #start from 0
        current_time =  mixer.music.get_pos()/1000
        print("the timeeeeeeeeeeeeeeeeeeee is")
        print(current_time)
        #convertion
        current_time_convertion =  time.strftime('%M:%S',time.gmtime(current_time))
        return current_time_convertion
    
    def music_current_time2():
        global played_song_time
        global paused_position
        global is_playing2
        #start from 0
        if is_playing2:
            print("playiiiiiing")
            current_time_obj = music_current_time()
            minutes, seconds = map(int, current_time_obj.split(':'))
            time_is =  minutes * 60 + seconds
            
            print("paused_postition varable is -------")
            print(time_is)
            
            print("timeis varable is -------")
            print(time_is)
            
            current_time = paused_position + time_is
            
        else:
            print("paused")
            current_time = paused_position
            
        print("the timeeeeeeeeeeeeeeeeeeee after addathion is")
        print(current_time)
        #convertion
        current_time_convertion =  time.strftime('%M:%S',time.gmtime(current_time))
        return current_time_convertion
    
    def update_active_song_time():
        global paused_position2
        selected_items = tree.selection()
        if selected_items:
            if music_current_time2() <= music_duration():
                # Update the label text
                active_song_time.config(text=music_current_time2())
            
                # Schedule the function to be called again in 1000 milliseconds (1 second)
                
                active_song_time.after(1000, update_active_song_time)
                
                current_time_obj = music_current_time()
                minutes, seconds = map(int, current_time_obj.split(':'))
                time_is =  minutes * 60 + seconds
                print("hksfasjhadsgfsajfgsdaufhasdfsa")
                print(time_is)
                
                paused_position2 = time_is
            else:
                active_song_time.config(text="00:00")
                paused_position2 = 0
                play_next_song()
        else:
            active_song_time.config(text="00:00")
            paused_position2 = 0
            
            
            
    def update_active_song_time_whensshuffleButton():
        global paused_position2
        selected_items = tree.selection()
        if selected_items:
            if music_current_time2() <= music_duration():
                # Update the label text
                active_song_time.config(text=music_current_time2())
            
                # Schedule the function to be called again in 1000 milliseconds (1 second)
                
                active_song_time.after(1000, update_active_song_time)
                
                current_time_obj = music_current_time()
                minutes, seconds = map(int, current_time_obj.split(':'))
                time_is =  minutes * 60 + seconds
                print("hksfasjhadsgfsajfgsdaufhasdfsa")
                print(time_is)
                
                paused_position2 = time_is
            else:
                active_song_time.config(text="00:00")
                paused_position2 = 0
                play_rondom_song()
                
        else:
            active_song_time.config(text="00:00")
            paused_position2 = 0
            
    
    def update_time_bar():
        global paused_position
        global is_playing2
        #start from 0
        if is_playing2:
            # Get the current time and duration of the music
            current_time = paused_position + mixer.music.get_pos()/1000
            
        else:
            current_time = paused_position
            
        song_mut = MP3(return_active_song_path())
        # get the song length
        song_mut_lenght = song_mut.info.length
        duration = song_mut_lenght
    
        # Calculate the percentage of the music that has been played
        percent_complete = current_time / duration
        print(percent_complete)
    
        # Update the progress bar value
        time_bar.config(value=percent_complete * 100)
    
        # Schedule the function to be called again in 1000 milliseconds (1 second)
        time_bar.after(1000, update_time_bar)
    '''
    active_song = [{
        "name":  song_name_without_extension(),
        "image": "",
        "duration": music_duration(),
        "current_time": music_current_time()
    }]
    print(active_song[0]["name"])
    print(active_song[0]["duration"])
    print(active_song[0]["current_time"])
    '''
    
    
    
    # Create PhotoImage objects for the play and pause button icons
    play_icon = tk.PhotoImage(file=relative_to_assets("button_6.png"))
    pause_icon = tk.PhotoImage(file=relative_to_assets("button_5.png"))
    
    # Create Button widgets with the play and pause icons
    pause_button = tk.Button(window, image=pause_icon, borderwidth=0, highlightthickness=0, command=toggle_playback)
    pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
    
    play_button = tk.Button(window, image=play_icon, borderwidth=0, highlightthickness=0, command=toggle_playback)
    play_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
    
    #active song name and details view
    duration_text = tk.Label(window,font=("SFProText Medium", 12 * -1), fg="#BDBDBD", anchor="nw", text=music_duration(),bg="#FFFFFF")
    duration_text.place(x=1145, y=627)
    
    active_song_name = tk.Label(window,font=("SFProText Semibold", 14 * -1), fg="#262626",anchor="nw", text=limit_the_text_length(),bg="#FFFFFF")
    active_song_name.place(x=403, y=646)
    
    active_song_album = tk.Label(window,font=("ABeeZee Regular", 12 * -1), fg="#808080",anchor="nw", text=limit_the_album_length(),bg="#FFFFFF")
    active_song_album.place(x=288, y=674)
    
    active_song_time = tk.Label(window,font=("SFProText Medium", 12 * -1), fg="#BDBDBD",anchor="nw", text=music_current_time(),bg="#FFFFFF")
    active_song_time.place(x=313, y=627)
    
    update_active_song_time()
    
    
    # Create the icon widget
    icon_image = tk.PhotoImage(file="D:\\college\\GP\\Project\\Home\\frame0\\image_16.png")
    icon_label = tk.Label(window, image=icon_image)
    
    # Pack the icon label widget
    icon_label.place()
    
    # Call the update_icon_visibility function to initially set the icon visibility
    update_icon_visibility()
    
    # Function to update the icon visibility whenever needed
    def on_update_icon_visibility():
        update_icon_visibility()
    
    
    # Create a progress bar widget
    style = ttk.Style()
    style.theme_use('default')
    
    # Override default styles
    style.configure('custom.Horizontal.TProgressbar', troughcolor='#E5E5E5', bordercolor='#E5E5E5',
         background='#737373', lightcolor='#737373', darkcolor='#737373',
        relief='flat', thickness=10)
    
    style.layout('custom.Horizontal.TProgressbar',
        [('Horizontal.Progressbar.trough',
            {'children': [('Horizontal.Progressbar.pbar',
                            {'side': 'left', 'sticky': 'ns'})],
            'sticky': 'nswe',
            'border': '0'}),
        ('Horizontal.Progressbar.label', {'sticky': ''})])
    
    # Raise priority
    style.map('custom.Horizontal.TProgressbar',
        foreground=[('disabled', 'blue')])
    # Create progress bar
    time_bar = tk.ttk.Progressbar(window, orient=tk.HORIZONTAL, mode='determinate', length=1010, style='custom.Horizontal.TProgressbar')
    time_bar.place(x=191, y=602)
    
    canvas.create_rectangle(
        191.0,
        607.0,
        1200.0,
        612.2664184570312,
        fill="#E5E5E5",
        outline="")
    
    canvas.create_rectangle(
        191.0,
        607.0,
        362.93719482421875,
        612.2664184570312,
        fill="#737373",
        outline="")
    #show lyrics
    def get_lyrics():
        selected_item = tree.selection()
        if selected_item:
            songName = return_songName()
            artistName = return_artistName()
            cursor.execute("SELECT Lyrics FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (songName, artistName))
            result = cursor.fetchone()
            music_path = result[0]
            return   music_path,songName
        else:
            music_path = "No song is slected"
            return music_path
    def show_lyrics():
        # Get the lyrics of the current song
        lyrics,songname = get_lyrics()
        lyrics = cleanLyrics(lyrics,songname)

        lyrics_window = tk.Toplevel(window)
        lyrics_window_width = 400
        lyrics_window_height = 600
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - lyrics_window_width) // 2
        y = (screen_height - lyrics_window_height) // 2
        
        lyrics_window.geometry(f"{lyrics_window_width}x{lyrics_window_height}+{x}+{y}")
        lyrics_window.title("Song lyrics")
        
        lyrics_window.configure(bg="#FFFFFF")
        
        lyrics_frame = tk.Frame(lyrics_window)
        lyrics_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(lyrics_frame)
        scrollbar.pack(side="right", fill="y")
        
        lyrics_text = tk.Text(lyrics_frame, font=("Arial", 12), bg="white", fg="black", yscrollcommand=scrollbar.set)
        lyrics_text.pack(fill="both", expand=True)
        
        scrollbar.config(command=lyrics_text.yview)
        
        lyrics_text.insert("1.0", lyrics)
        
        lyrics_window.mainloop()
    
    
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=show_lyrics,
        relief="flat"
    )
    button_11.place(
        x=1160.0,
        y=668.0,
        width=23.0,
        height=25.0
    )
    
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=show_lyrics,
        relief="flat"
    )
    button_11.place(
        x=1160.0,
        y=668.0,
        width=23.0,
        height=25.0
    )
    window.resizable(False, False)
    window.mainloop()


#################################################### HOME ADMIN ######################################################
def AdminHome():
    
    # Create a cursor
    cursor = connection.cursor()
    
    # Retrieve data from the database
    cursor.execute("SELECT SongName, ArtistName, ExplictLabel FROM SongsClassification")
    rows = cursor.fetchall()
    
    # Retrieve data from the database
    cursor.execute("SELECT SongName, ArtistName, ExplictLabel FROM SongsClassification")
    rows = cursor.fetchall()
    
    # Define a function that toggles between the play and pause button icons and controls the playback of the music
    
    def toggle_playback():
        global is_playing2
        global paused_position
        global prev_song_playing
        global paused_position2
        
        selected_item = tree.selection()
        if selected_item:
            if not is_playing2:
                # Get the selected song from the playlist
                song_name = return_songName()
                artist_name = return_artistName()
                
                # Retrieve the music path from the database based on the selected song
                cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
                result = cursor.fetchone()
                print(result)
                if result:
                    music_path = result[0]
                    
                    if not (song_name == prev_song_playing[0] and artist_name == prev_song_playing[1]):
                        paused_position = 0
                   
                    prev_song_playing[0] = song_name
                    prev_song_playing[1] = artist_name
                    # Load and play the music
                    mixer.music.load(music_path)
                    print( "heereee is the pause beforeplay")
                    print(paused_position)
                    mixer.music.play(start=paused_position)
                    
                    # Update the song duration, name, album, time, etc.
                    duration_text.config(text=music_duration())
                    active_song_name.config(text=limit_the_text_length())
                    active_song_album.config(text=limit_the_album_length())
                    

                    
                        
                    
                    
                    # Update the explict icon visibility
                    update_icon_visibility()
                    
                    # Change the button icon to the pause icon
                    play_button.place_forget()
                    pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                    
                    is_playing2 = True
                    update_active_song_time()
                    update_time_bar()
            else:
                
                mixer.music.pause()
                # Store the current position
                print(paused_position2)
                paused_position += paused_position2

                current_time_convertion =  time.strftime('%M:%S',time.gmtime(paused_position))
                active_song_time.config(text = current_time_convertion)
                # Pause the music
                
                current_time_convertion =  time.strftime('%M:%S',time.gmtime(paused_position))
                print("here is when its paused")
                print("")
                active_song_time.config(text= current_time_convertion)
                
                print("this is when the song is paused")
                print(current_time_convertion)
                
                # Change the button icon to the play icon
                pause_button.place_forget()
                play_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = False
                active_song_time.config(text= current_time_convertion)
            
        else:
            item_id = tree.get_children()[0]
            tree.selection_set(item_id)
            tree.focus(item_id)
            
            # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                if not (song_name == prev_song_playing[0] and artist_name == prev_song_playing[1]):
                    paused_position = 0
               
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                # Load and play the music
                mixer.music.load(music_path)
                print( "heereee is the pause beforeplay")
                print(paused_position)
                mixer.music.play(start=paused_position)
                
                # Update the song duration, name, album, time, etc.
                duration_text.config(text=music_duration())
                active_song_name.config(text=limit_the_text_length())
                active_song_album.config(text=limit_the_album_length())
                
                    
                
                
                # Update the explict icon visibility
                update_icon_visibility()
                
                # Change the button icon to the pause icon
                play_button.place_forget()
                pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = True
                
                update_active_song_time()
                update_time_bar()
                
            else:
                # Pause the music
                
                mixer.music.pause()
                paused_position += paused_position2
                # Change the button icon to the play icon
                pause_button.place_forget()
                play_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = False
                
                
    def play_button_playlist():
        global is_playing2
        global paused_position
        
        item_id = tree.get_children()[0]
        tree.selection_set(item_id)
        tree.focus(item_id)
        
        # Load and play the next song in the playlist
        the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
        selected_song = the_nextSong_toPlay
        
        #get the song name and artist name to quary the path of the next song
        song_name = the_nextSong_toPlay["values"][0]
        artist_name = the_nextSong_toPlay["values"][1]
        
        
        
        # Retrieve the music path from the database based on the selected song
        cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
        result = cursor.fetchone()
        print(result)
        if result:
            music_path = result[0]
            
            prev_song_playing[0] = song_name
            prev_song_playing[1] = artist_name
            
            
            paused_position = 0
            
            
            
            
            # Load and play the music
            mixer.music.load(music_path)
            mixer.music.play()
            
            # Update the song duration, name, album, time, etc.
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
                
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            
            update_active_song_time()
            update_time_bar()
        
    
    def play_rondom_song():
        global is_playing2
        global paused_position
        
        # Get all the children (songs) in the tree
        children = tree.get_children()
        
        if children:
            # Select a random song from the tree
            random_song = random.choice(children)
            
            # Select and focus the random song in the tree
            tree.selection_set(random_song)
            tree.focus(random_song)
            
            # Load and play the random song
            selected_song = tree.item(random_song)
            song_name = selected_song["values"][0]
            artist_name = selected_song["values"][1]
            
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
                
                
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
                
                # Update the song duration, name, album, time, etc.
                duration_text.config(text=music_duration())
                active_song_name.config(text=limit_the_text_length())
                active_song_album.config(text=limit_the_album_length())
                
                    
                # Update the explicit icon visibility
                update_icon_visibility()
                
                # Change the button icon to the pause icon
                play_button.place_forget()
                pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
                
                is_playing2 = True
                update_active_song_time_whensshuffleButton()
                update_time_bar()
    
    def play_next_song():
        global prev_song_playing
        global paused_position
        global is_playing2
        # Get the index of the currently selected song in the playlist
        selected_item = tree.selection()
        if selected_item:
            current_song_index = tree.index(selected_item)
            # Increment the index to get the index of the next song
            next_song_index = current_song_index + 1
            # Wrap around to the beginning of the playlist if necessary
            tree_size = len(tree.get_children())
            print("tree size is :::")
            print(tree_size)
            if next_song_index >= tree_size:
                next_song_index = 0
            # Select the next song in the playlist
            tree.selection_remove(tree.selection())
            item_id = tree.get_children()[next_song_index]
            tree.selection_set(item_id)
            tree.focus(item_id)
          # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[next_song_index]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            update_active_song_time()
            update_time_bar()
            
        else:
            
            item_id = tree.get_children()[0]
            tree.selection_set(item_id)
            tree.focus(item_id)
            
            # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            prev_song_playing[0] = song_name
            prev_song_playing[1] = artist_name
            
            
            paused_position = 0
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            update_active_song_time()
            update_time_bar()
    
            
    
    
    def play_prev_song():
        global prev_song_playing
        global paused_position
        global is_playing2
        
        # Get the index of the currently selected song in the playlist
        selected_item = tree.selection()
        if selected_item:
            current_song_index = tree.index(selected_item)
            # Increment the index to get the index of the next song
            next_song_index = current_song_index - 1
            # Wrap around to the beginning of the playlist if necessary
            tree_size = len(tree.get_children())
            print("tree size is :::")
            print(tree_size)
            if next_song_index < 0:
                next_song_index = tree_size-1
            # Select the next song in the playlist
            tree.selection_remove(tree.selection())
            item_id = tree.get_children()[next_song_index]
            tree.selection_set(item_id)
            tree.focus(item_id)
          # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[next_song_index]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                music_path = result[0]
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
            update_active_song_time()
            update_time_bar()
            
        else:
            item_id = tree.get_children()[0]
            tree.selection_set(item_id)
            tree.focus(item_id)
            
            # Load and play the next song in the playlist
            the_nextSong_toPlay = tree.item(tree.get_children()[0]) #get the full row of the song
            selected_song = the_nextSong_toPlay
            print("here is the next song loaded:  ")
            print(selected_song)
        
            #get the song name and artist name to quary the path of the next song
            song_name = the_nextSong_toPlay["values"][0]
            artist_name = the_nextSong_toPlay["values"][1]
            
            
            
            print("here is the next song name:  ")
            print(song_name)
              
            print("here is the next artist name:  ")
            print(artist_name)
        
            # Retrieve the music path from the database based on the selected song
            cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            result = cursor.fetchone()
            print(result)
            if result:
                music_path = result[0]
                
                music_path = result[0]
                prev_song_playing[0] = song_name
                prev_song_playing[1] = artist_name
                
                
                paused_position = 0
        
                # Load and play the music
                mixer.music.load(music_path)
                mixer.music.play()
            
            # update the next song details
            duration_text.config(text=music_duration())
            active_song_name.config(text=limit_the_text_length())
            active_song_album.config(text=limit_the_album_length())
            
            
            # Update the explict icon visibility
            update_icon_visibility()
            
            # Change the button icon to the pause icon
            play_button.place_forget()
            pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
            
            is_playing2 = True
        
            update_active_song_time()
            update_time_bar()
    
    OUTPUT_PATH = os.path.dirname(os.path.abspath("__file__"))
    ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\college\\GP\\Project\\Admin\\build\\assets\\frame0")
    
    
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    class ImageListbox(tk.Listbox):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.images = []
    
        def insert(self, index, *elements, image=None):
            super().insert(index, *elements)
            self.images.insert(index, image)
            self.itemconfig(index, image=image, compound="left")
    
    
    window = Tk()
    
    window.geometry("1200x700")
    window.configure(bg = "#FFFFFF")
    
    # Initialize the mixer module
    mixer.init()
    
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        1.0,
        190.0,
        703.0,
        fill="#EAEAEA",
        outline="")
    
    canvas.create_rectangle(
        190.0,
        97.0,
        191.0,
        897.0,
        fill="#CCCCCC",
        outline="")
    
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        112.0,
        127.0,
        image=image_image_1
    )
    
    canvas.create_rectangle(
        191.0,
        1.0,
        1200.0,
        53.0,
        fill="#F4F4F4",
        outline="")
    
    canvas.create_text(
        640.0,
        21.0,
        anchor="nw",
        text="ROBOFIY",
        fill="#262626",
        font=("SFProDisplay Medium", 16 * -1)
    )
    
    canvas.create_text(
        478.0,
        191.0,
        anchor="nw",
        text="The AI-powered classification algorithm embedded in the music player employs sophisticated techniques to evaluate \nthe lyrics and audio of each song. It utilizes natural language processing (NLP) and machine learning algorithms to \nunderstand the context, tone, and choice of words within the lyrics. By analyzing the song's audio and lyrics, the AI \ncan accurately determine whether the song contains explicit content or is safe for all audiences.",
        fill="#808080",
        font=("SFProDisplay Regular", 13 * -1)
    )
    
    canvas.create_text(
        479.0,
        104.0,
        anchor="nw",
        text="ROBOFIY Music",
        fill="#262626",
        font=("SFProDisplay Medium", 24 * -1)
    )
    
    canvas.create_text(
        473.0,
        135.0,
        anchor="nw",
        text="Robofiy smart music player playList",
        fill="#285689",
        font=("AndadaProRoman Regular", 24 * -1)
    )
    
    
    
    canvas.create_rectangle(
        213.0,
        334.0,
        1200.0,
        389.0,
        fill="#FAFAFA",
        outline="")
    
    
    
    
    
    canvas.create_rectangle(
        999.638671875,
        677.5,
        1055.505615234375,
        680.5,
        fill="#BFBFBF",
        outline="")
    
    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        1058.66796875,
        678.5,
        image=image_image_13
    )
    
    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        1079.0,
        679.0,
        image=image_image_14
    )
    
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=play_prev_song,
        relief="flat"
    )
    button_3.place(
        x=653.0,
        y=636.0,
        width=48.0,
        height=40.0
    )
    
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=play_next_song,
        relief="flat"
    )
    button_4.place(
        x=755.0,
        y=638.0,
        width=45.0,
        height=38.0
    )
    
    
    
    
    
    
    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        234.0,
        659.0,
        image=image_image_15
    )
   
    #___________playing song___________________
    
    
    canvas.create_rectangle(
        13.0,
        204.0,
        182.0,
        232.0,
        fill="#DFDFDF",
        outline="")
    #--------------------------------------------------------------

    canvas.create_text(
    13.0,
    299.0,
    anchor="nw",
    text="Clean mode",
    fill="#7D7D7D",
    font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_text(
        13.0,
        251.0,
        anchor="nw",
        text="here you can usr the clean\n mode(show non-explict songs \nonly).",
        fill="#9F9E9B",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    
    
    signOut=canvas.create_text(
    13.0,
    316.0,
    anchor="nw",
    text="Sign out",
    fill="#E76D53",
    font=("AndadaProRoman Bold", 12)
    )
    def on_text_click(event):
        window.destroy()
        openlogin()

    canvas.tag_bind(signOut, '<Button-1>', on_text_click)
    
    
    

    
    canvas.create_text(
        632.0,
        306.0,
        anchor="nw",
        text="artist",
        fill="#7F7F7F",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_text(
        213.0,
        306.0,
        anchor="nw",
        text="Song",
        fill="#7F7F7F",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_text(
        926.0,
        306.0,
        anchor="nw",
        text="Label",
        fill="#7F7F7F",
        font=("AndadaProRoman Bold", 12 * -1)
    )
    
    canvas.create_rectangle(
        617.0,
        304.0,
        618.0,
        320.0,
        fill="#E5E5E5",
        outline="")
    
    canvas.create_rectangle(
        911.0,
        304.0,
        912.0,
        320.0,
        fill="#E5E5E5",
        outline="")
    
    image_image_19 = PhotoImage(
        file=relative_to_assets("image_19.png"))
    image_19 = canvas.create_image(
        351.0,
        193.0,
        image=image_image_19
    )
    
    
    button_image_13 = PhotoImage(
        file=relative_to_assets("button_13.png"))
    button_13 = Button(
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_13 clicked"),
        relief="flat"
    )
    button_13.place(
        x=53.0,
        y=14.0,
        width=14.0,
        height=14.0
    )
    
    button_image_14 = PhotoImage(
        file=relative_to_assets("button_14.png"))
    button_14 = Button(
        image=button_image_14,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_14 clicked"),
        relief="flat"
    )
    button_14.place(
        x=33.0,
        y=14.0,
        width=14.0,
        height=14.0
    )
    
    button_image_15 = PhotoImage(
        file=relative_to_assets("button_15.png"))
    button_15 = Button(
        image=button_image_15,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_15 clicked"),
        relief="flat"
    )
    button_15.place(
        x=13.0,
        y=14.0,
        width=14.0,
        height=14.0
    )
    
    button_image_16 = PhotoImage(
        file=relative_to_assets("button_16.png"))
    button_16 = Button(
        image=button_image_16,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_16 clicked"),
        relief="flat"
    )
    button_16.place(
        x=213.0,
        y=16.0,
        width=13.0,
        height=21.0
    )
    
    button_image_17 = PhotoImage(
        file=relative_to_assets("button_17.png"))
    button_17 = Button(
        image=button_image_17,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_17 clicked"),
        relief="flat"
    )
    button_17.place(
        x=247.0,
        y=16.0,
        width=14.0,
        height=22.0
    )
    
    # Create a canvas to contain the treeview and scrollbar
    music_frame = tk.Frame(window, width=970, height=277)
    music_frame.place(x=210.0, y=330)
    
    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(music_frame)
    playList = tk.Listbox(music_frame, width=160, height=17, highlightthickness=0, highlightbackground="white", bd=0, yscrollcommand=scrollbar.set)
    tree = ttk.Treeview(music_frame, columns=("SongName", "ArtistName", "ExplicitLabel"), height=14, show="", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both")
    
    # Function to insert a song entry with custom view
    def insert_song_entry(song_name, artist_name, explicit_label):
        # Insert a new row with the song name, artist name, and explicit label
        tree.insert("", tk.END, values=(song_name, artist_name, explicit_label))
    
    # Adjust the column widths
    tree.column("SongName", width=407)
    tree.column("ArtistName", width=295)
    tree.column("ExplicitLabel", width=270)
    
    
    
    
    # Iterate over the files in the directory and print their names
    music_dir = "D:/college/GP/songs"
    
    # Get a list of all the music files in the directory
    music_files = [file for file in os.listdir(music_dir) if file.endswith(".mp3")]
    
    # Insert the music files into the Listbox
    for row in rows:
        song_name = row[0]
        artist_name = row[1]
        explicit_label = row[2]
        temp=""
        # Concatenate the song name, artist name, and explicit label
        item_text = f"{song_name} - {artist_name} ({explicit_label})"
        if explicit_label == "1":
            temp="Explicit"
        elif explicit_label == "0":
            temp="Non-Explicit"
        insert_song_entry(song_name, artist_name, temp)
        playList.insert(tk.END, item_text)
        
    def on_tree_select(column):
        # Get the selected item
        selected_item = tree.selection()[0]
    
        # Get the values of the selected item (song_name, artist_name, explicit_label)
        values = tree.item(selected_item, "values")
    
        # Retrieve the song name, artist name, and explicit label from the values
        song_name = values[0]
        artist_name = values[1]
        explicit_label = values[2]
        
        # Return the value based on the specified column index
        if column == 0:
            return song_name
        elif column == 1:
            return artist_name
        elif column == 2:
            return explicit_label
        
    #delete a song from the database
    
    def delete_song_from_playlist():
        selected_item = tree.selection()
        if selected_item:
            song_name = return_songName()
            artist_name = return_artistName()
            selected_item = tree.selection()[0]
            tree.delete(selected_item)
            tree.update()
            cursor.execute("DELETE FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
            connection.commit()
            
    
    def delete_song_confirm():
        selected_item = tree.selection()
        if selected_item:
            response = messagebox.askyesno("Delete Item", "Are you sure you want to delete " + return_songName() +"?")
            if response:
                # Delete the item
                delete_song_from_playlist()
                print("deleted")
        else:
            response2 = messagebox.askyesno("Delete Item", "You should choose a song first to delete it! ")
    
    #delete button widgets
    
    delete_button_image = PhotoImage(
        file=relative_to_assets("button_1.png"))
    delete_song_button = Button(
        image=delete_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: delete_song_confirm(),
        relief="flat"
    )
    delete_song_button.place(
        x=646.0,
        y=257.0,
        width=153.0,
        height=28.0
    )
    
    #add song to the database
    
    
    def return_lyrics_for_database(songName,Artist):
        song_lyrics = getLyrics(songName, Artist)
        return song_lyrics
        
    def return_explictLabel_for_database(songName,Artist):
        label = classifySong(songName, Artist)
        return label
    
    def add_song():
        def add_song_path():
            song_name = song_entry.get()
            artist_name = artist_entry.get()
    
            if song_name and artist_name and file_path:
                
                lyrics_text = return_lyrics_for_database(song_name,artist_name)
                if lyrics_text=="Not Found":
                    messagebox.showerror("Sorry","Song Wasn't Found")
                else:
                    explict_label =  return_explictLabel_for_database(song_name,artist_name)
                    explict_label2 = int(explict_label)
                    # Insert the song details into the database
        
        
                    cursor.execute("INSERT INTO SongsClassification (SongName, ArtistName, Lyrics, ExplictLabel, MusicPath) VALUES (?, ?, ?, ?, ?)",
                                   (song_name, artist_name, lyrics_text, explict_label, file_path))
                    
                    #insert into the play list
                    temp=""
                    if explict_label2 == 1:
                        temp="Explicit"
                    elif explict_label2 == 0:
                        temp="Non-Explicit"
                    connection.commit()
                    insert_song_entry(song_name, artist_name, temp)
                
    
    
                    # Close the add song window
                add_song_window.destroy()
            else:
                error_label.config(text="Please enter all fields.")
    
        def cancel_add_song():
            add_song_window.destroy()
        
        def choose_file():
            global file_path
            file_path = filedialog.askopenfilename(filetypes=(("MP3 Files", "*.mp3"),))
            file_entry.delete(0, tk.END)
            file_entry.insert(tk.END, file_path)
            add_song_window.lift()
    
        add_song_window = tk.Toplevel()
        add_song_window.geometry("200x200")
        add_song_window.title("Add Song to the database")
        
        # Set the size and position of the add_song_window
        window_width = 200  # Set the desired width of the add_song_window
        window_height = 200  # Set the desired height of the add_song_window
        
        # Set the size and position of the window
        windowApp_width = 1200  # Set the desired width of the add_song_window
        window_Appheight = 700
        
      
        x = (windowApp_width // 2) - (window_width // 2)  # Calculate the x-coordinate for centering the add_song_window
        y = (window_Appheight // 2) - (window_height // 2)  # Calculate the y-coordinate for centering the add_song_window
        
        add_song_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set the size and position of the add_song_window
        
        
        
        
    
        song_label = tk.Label(add_song_window, text="Song Name:")
        song_entry = tk.Entry(add_song_window)
        artist_label = tk.Label(add_song_window, text="Artist Name:")
        artist_entry = tk.Entry(add_song_window)
        file_label = tk.Label(add_song_window, text="File Path:")
        file_entry = tk.Entry(add_song_window, state="readonly")
        file_button = tk.Button(add_song_window, text="Choose File", command=choose_file)
    
        confirm_button = tk.Button(add_song_window, text="Confirm", command=add_song_path)
        cancel_button = tk.Button(add_song_window, text="Cancel", command=cancel_add_song)
        error_label = tk.Label(add_song_window, fg="red")
    
        song_label.pack()
        song_entry.pack()
        artist_label.pack()
        artist_entry.pack()
        file_label.pack()
        file_entry.pack()
        file_button.pack()
        confirm_button.pack()
        cancel_button.pack()
        error_label.pack()
    
        add_song_window.mainloop()
        
        
    
    
    
    
    
      
    #add song wedgits
    add_song_button_image = PhotoImage(
        file=relative_to_assets("button_2.png"))
    add_song_button = Button(
        image=add_song_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: add_song(),
        relief="flat"
    )
    add_song_button.place(
        x=479.0,
        y=257.0,
        width=153.0,
        height=28.0
    )
    
    def return_fist_item_inThe_playList():
        first_item = tree.get_children()[0]
        first_item_values = tree.item(first_item, "values")
        return first_item_values
    return_fist_item_inThe_playList()
    
    def return_songName():
        # Get the selected item
        selected_items = tree.selection()
        if selected_items:
            # Get the values of the selected item (song_name, artist_name, explicit_label)
            selected_item = selected_items[0]
            values = tree.item(selected_item, "values")
        
            # Retrieve the song name, artist name, and explicit label from the values
            song_name = values[0]
            return song_name
        
        else:
            selected_items = return_fist_item_inThe_playList()
            song_name = selected_items[0]
            return song_name
    
    def return_artistName():
        # Get the selected item
        selected_items = tree.selection()
        if selected_items:
            # Get the values of the selected item (song_name, artist_name, explicit_label)
            selected_item = selected_items[0]
            values = tree.item(selected_item, "values")
        
            # Retrieve the song name, artist name, and explicit label from the values
            artist_name = values[1]
            return artist_name
        
        else:
            selected_items = return_fist_item_inThe_playList()
            artist_name = selected_items[1]
            return artist_name
    
    def update_icon_visibility():
        print ("hereeeeeeeeeeeeee")
        explicit_label = return_the_explictLabel()
        print(explicit_label)
        if explicit_label == "Explicit":
            icon_label.place(x=540.0, y=640.0)
            print("nooooooooooooooooooooooooooooooooooooooo")
        else:
            icon_label.place_forget()
            
    def return_the_explictLabel():
        # Get the selected item
        selected_items = tree.selection()
        if selected_items:
            # Get the values of the selected item (song_name, artist_name, explicit_label)
            selected_item = selected_items[0]
            values = tree.item(selected_item, "values")
        
            # Retrieve the song name, artist name, and explicit label from the values
            explict_label = values[2]
            return explict_label
        
        else:
            selected_items = return_fist_item_inThe_playList()
            explict_label = selected_items[2]
            return explict_label
    
    
    
    
    def return_active_song_path():
        song_name = return_songName()
        artist_name = return_artistName()
        # Retrieve the music path from the database based on the selected song
        cursor.execute("SELECT MusicPath FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (song_name, artist_name))
        result = cursor.fetchone()
        music_path = result[0]
        
        return music_path
           
    def limit_the_text_length():
        # Truncate the text and add "..." if it's too long
        max_length = 20  # Maximum length of text to show
        if len(return_songName()) > max_length:
            truncated_text = return_songName()[:max_length] + "..."
        else:
            truncated_text = return_songName()
    
        return truncated_text
    
    def limit_the_album_length():
        # Truncate the text and add "..." if it's too long
        max_length = 50  # Maximum length of text to show
        if len(return_artistName()) > max_length:
            truncated_text = return_artistName()[:max_length] + "..."
        else:
            truncated_text = return_artistName()
    
        return truncated_text
    
    def music_duration():
        #select the song
        song_mut=MP3(return_active_song_path())
        #get the song length
        song_mut_lenght = song_mut.info.length
        #convert into mins and secs
        song_mut_lenght_convertion = time.strftime('%M:%S',time.gmtime(song_mut_lenght))
        return song_mut_lenght_convertion
    
    def music_current_time():
        global played_song_time
        #start from 0
        current_time =  mixer.music.get_pos()/1000
        print("the timeeeeeeeeeeeeeeeeeeee is")
        print(current_time)
        #convertion
        current_time_convertion =  time.strftime('%M:%S',time.gmtime(current_time))
        return current_time_convertion
    
    def music_current_time2():
        global played_song_time
        global paused_position
        global is_playing2
        #start from 0
        if is_playing2:
            print("playiiiiiing")
            current_time_obj = music_current_time()
            minutes, seconds = map(int, current_time_obj.split(':'))
            time_is =  minutes * 60 + seconds
            
            print("paused_postition varable is -------")
            print(time_is)
            
            print("timeis varable is -------")
            print(time_is)
            
            current_time = paused_position + time_is
            
        else:
            print("paused")
            current_time = paused_position
            
        print("the timeeeeeeeeeeeeeeeeeeee after addathion is")
        print(current_time)
        #convertion
        current_time_convertion =  time.strftime('%M:%S',time.gmtime(current_time))
        return current_time_convertion
    
    def update_active_song_time():
        global paused_position2
        selected_items = tree.selection()
        if selected_items:
            if music_current_time2() <= music_duration():
                # Update the label text
                active_song_time.config(text=music_current_time2())
            
                # Schedule the function to be called again in 1000 milliseconds (1 second)
                
                active_song_time.after(1000, update_active_song_time)
                
                current_time_obj = music_current_time()
                minutes, seconds = map(int, current_time_obj.split(':'))
                time_is =  minutes * 60 + seconds
                print("hksfasjhadsgfsajfgsdaufhasdfsa")
                print(time_is)
                
                paused_position2 = time_is
            else:
                active_song_time.config(text="00:00")
                paused_position2 = 0
                play_next_song()
        else:
            active_song_time.config(text="00:00")
            paused_position2 = 0
            
            
            
    def update_active_song_time_whensshuffleButton():
        global paused_position2
        selected_items = tree.selection()
        if selected_items:
            if music_current_time2() <= music_duration():
                # Update the label text
                active_song_time.config(text=music_current_time2())
            
                # Schedule the function to be called again in 1000 milliseconds (1 second)
                
                active_song_time.after(1000, update_active_song_time)
                
                current_time_obj = music_current_time()
                minutes, seconds = map(int, current_time_obj.split(':'))
                time_is =  minutes * 60 + seconds
                print("hksfasjhadsgfsajfgsdaufhasdfsa")
                print(time_is)
                
                paused_position2 = time_is
            else:
                active_song_time.config(text="00:00")
                paused_position2 = 0
                play_rondom_song()
                
        else:
            active_song_time.config(text="00:00")
            paused_position2 = 0
            
    
    def update_time_bar():
        global paused_position
        global is_playing2
        #start from 0
        if is_playing2:
            # Get the current time and duration of the music
            current_time = paused_position + mixer.music.get_pos()/1000
            
        else:
            current_time = paused_position
            
        song_mut = MP3(return_active_song_path())
        # get the song length
        song_mut_lenght = song_mut.info.length
        duration = song_mut_lenght
    
        # Calculate the percentage of the music that has been played
        percent_complete = current_time / duration
        print(percent_complete)
    
        # Update the progress bar value
        time_bar.config(value=percent_complete * 100)
    
        # Schedule the function to be called again in 1000 milliseconds (1 second)
        time_bar.after(1000, update_time_bar)
       
    
    
    # Create PhotoImage objects for the play and pause button icons
    play_icon = tk.PhotoImage(file=relative_to_assets("button_6.png"))
    pause_icon = tk.PhotoImage(file=relative_to_assets("button_5.png"))
    
    # Create Button widgets with the play and pause icons
    pause_button = tk.Button(window, image=pause_icon, borderwidth=0, highlightthickness=0, command=toggle_playback)
    pause_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
    
    play_button = tk.Button(window, image=play_icon, borderwidth=0, highlightthickness=0, command=toggle_playback)
    play_button.place(x=707.0, y=626.0, width=46.0, height=61.0)
    
    #active song name and details view
    duration_text = tk.Label(window,font=("SFProText Medium", 12 * -1), fg="#BDBDBD", anchor="nw", text=music_duration(),bg="#FFFFFF")
    duration_text.place(x=1145, y=627)
    
    active_song_name = tk.Label(window,font=("SFProText Semibold", 14 * -1), fg="#262626",anchor="nw", text=limit_the_text_length(),bg="#FFFFFF")
    active_song_name.place(x=403, y=646)
    
    active_song_album = tk.Label(window,font=("ABeeZee Regular", 12 * -1), fg="#808080",anchor="nw", text=limit_the_album_length(),bg="#FFFFFF")
    active_song_album.place(x=288, y=674)
    
    active_song_time = tk.Label(window,font=("SFProText Medium", 12 * -1), fg="#BDBDBD",anchor="nw", text=music_current_time(),bg="#FFFFFF")
    active_song_time.place(x=313, y=627)
    
    update_active_song_time()
    
    
    # Create the icon widget
    icon_image = tk.PhotoImage(file="D:\\college\\GP\\Project\\Admin\\build\\assets\\frame0\\image_16.png")
    icon_label = tk.Label(window, image=icon_image)
    
    # Pack the icon label widget
    icon_label.place()
    
    # Call the update_icon_visibility function to initially set the icon visibility
    update_icon_visibility()
    
    # Function to update the icon visibility whenever needed
    def on_update_icon_visibility():
        update_icon_visibility()
    
    
    # Create a progress bar widget
    style = ttk.Style()
    style.theme_use('default')
    
    # Override default styles
    style.configure('custom.Horizontal.TProgressbar', troughcolor='#E5E5E5', bordercolor='#E5E5E5',
         background='#737373', lightcolor='#737373', darkcolor='#737373',
        relief='flat', thickness=10)
    
    style.layout('custom.Horizontal.TProgressbar',
        [('Horizontal.Progressbar.trough',
            {'children': [('Horizontal.Progressbar.pbar',
                            {'side': 'left', 'sticky': 'ns'})],
            'sticky': 'nswe',
            'border': '0'}),
        ('Horizontal.Progressbar.label', {'sticky': ''})])
    
    # Raise priority
    style.map('custom.Horizontal.TProgressbar',
        foreground=[('disabled', 'blue')])
    # Create progress bar
    time_bar = tk.ttk.Progressbar(window, orient=tk.HORIZONTAL, mode='determinate', length=1010, style='custom.Horizontal.TProgressbar')
    time_bar.place(x=191, y=602)
    
    canvas.create_rectangle(
        191.0,
        607.0,
        1200.0,
        612.2664184570312,
        fill="#E5E5E5",
        outline="")
    
    canvas.create_rectangle(
        191.0,
        607.0,
        362.93719482421875,
        612.2664184570312,
        fill="#737373",
        outline="")
    #show lyrics
    #show lyrics
    def get_lyrics():
        selected_item = tree.selection()
        if selected_item:
            songName = return_songName()
            artistName = return_artistName()
            cursor.execute("SELECT Lyrics FROM SongsClassification WHERE SongName = ? AND ArtistName = ?", (songName, artistName))
            result = cursor.fetchone()
            music_path = result[0]
            return   music_path,songName
        else:
            music_path = "No song is slected"
            return music_path
        
    def show_lyrics():
        # Get the lyrics of the current song
        lyrics,songname = get_lyrics()
        lyrics = cleanLyrics(lyrics,songname)

        lyrics_window = tk.Toplevel(window)
        lyrics_window_width = 400
        lyrics_window_height = 600
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - lyrics_window_width) // 2
        y = (screen_height - lyrics_window_height) // 2
        
        lyrics_window.geometry(f"{lyrics_window_width}x{lyrics_window_height}+{x}+{y}")
        lyrics_window.title("Song lyrics")
        
        lyrics_window.configure(bg="#FFFFFF")
        
        lyrics_frame = tk.Frame(lyrics_window)
        lyrics_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(lyrics_frame)
        scrollbar.pack(side="right", fill="y")
        
        lyrics_text = tk.Text(lyrics_frame, font=("Arial", 12), bg="white", fg="black", yscrollcommand=scrollbar.set)
        lyrics_text.pack(fill="both", expand=True)
        
        scrollbar.config(command=lyrics_text.yview)
        
        lyrics_text.insert("1.0", lyrics)
        
        lyrics_window.mainloop()



        '''lyrics = get_lyrics()
    
        # Create a new window to display the lyrics
        lyrics_window = tk.Toplevel(window)
        sb = Scrollbar(lyrics_window)  
        sb.pack(side = RIGHT, fill = Y) 
        lyrics_window_width = 400
        lyrics_window_height = 600
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - lyrics_window_width) // 2
        y = (screen_height - lyrics_window_height) // 2
        
        lyrics_window.geometry(f"{lyrics_window_width}x{lyrics_window_height}+{x}+{y}")
        lyrics_window.title("Song lyrics")
        
        lyrics_window.configure(bg="#FFFFFF")
    
        # Limit line length to 40 characters
        #lyrics_lines = [lyrics[i:i+40] for i in range(0, len(lyrics), 40)]
        #lyrics_formatted = "\n".join(lyrics_lines)
        
        lyrics_label = tk.Label(lyrics_window, text=lyrics, font=("Arial", 12), bg="white", fg="black", justify="center")
        lyrics_label.pack(fill="both", expand=True)'''
        
    
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=show_lyrics,
        relief="flat"
    )
    button_11.place(
        x=1160.0,
        y=668.0,
        width=23.0,
        height=25.0
    )
    
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=show_lyrics,
        relief="flat"
    )
    button_11.place(
        x=1160.0,
        y=668.0,
        width=23.0,
        height=25.0
    )
    window.resizable(False, False)
    window.mainloop()
#################################################### BEGINNING ######################################################

def beginning():

    
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
    splash_window = AnimatedSplashWindow(root, "D:\\college\\GP\\Project\\beginning\\build\\assets\\cover.gif")
    
    def mainWindow():
        root.destroy()
        signup()
    
    # Show the splash screen for 5 seconds
    root.after(5000, mainWindow)
    
    # Create the main application window
    main_window = tk.Frame(root)
    main_window.pack(fill=tk.BOTH, expand=tk.YES)
    # Add widgets to the main window here...
    
    # Run the Tkinter event loop
    root.mainloop()
    





#AdminHome()
#signup()
beginning()