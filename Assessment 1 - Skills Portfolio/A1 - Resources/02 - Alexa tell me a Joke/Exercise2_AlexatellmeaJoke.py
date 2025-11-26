import os
import tkinter as tk
import random
import pygame  # for sound
from PIL import Image, ImageTk  # Needed for resizing background

# ---- FIXED BASE PATH ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOKES_FILE = os.path.join(BASE_DIR, "randomJokes.txt")
BG_IMAGE = os.path.join(BASE_DIR, "background.png")
LAUGH_SOUND = os.path.join(BASE_DIR, "laugh.wav")  # put your laugh.wav here

# Initialize pygame mixer
pygame.mixer.init()

# ---- FONTS ----
FONT_MAIN = ("Comic Sans MS", 22, "bold")      # setup text font
FONT_PUNCH = ("Comic Sans MS", 24, "bold")     # punchline text font
FONT_BUTTON = ("Comic Sans MS", 22, "bold")    # button text font

# ---------------- LOAD JOKES ----------------
def load_jokes():
    # Load jokes from the text file
    # Each joke must have a question mark separating setup and punchline
    # Returns a list of tuples: (setup, punchline)
    jokes = []
    with open(JOKES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline.strip()))
    return jokes

# ---------------- TEXT FADE ANIMATION ----------------
def fade_in_label(label, text, step=10, alpha=0):
    # Fade in text for a label by gradually changing its color from gray to black
    label.config(text=text, fg=f"#{alpha:02x}{alpha:02x}{alpha:02x}")
    if alpha < 255:
        label.after(10, lambda: fade_in_label(label, text, step, min(alpha + step, 255)))
    else:
        label.config(fg="black")

# ---------------- JOKE FUNCTIONS ----------------
def new_joke():
    # Select a new random joke and display the setup
    global current_joke
    current_joke = random.choice(jokes)
    fade_in_label(setup_label, current_joke[0])
    punchline_label.config(text="")  # hide punchline until button is clicked

def show_punchline():
    # Display the punchline and play laugh sound
    if current_joke[1]:
        fade_in_label(punchline_label, current_joke[1])
        pygame.mixer.Sound(LAUGH_SOUND).play()

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()  # create main window
root.title("Alexa Joke Teller")
root.attributes("-fullscreen", True)  # fullscreen mode
root.attributes("-alpha", 0.0)        # start with invisible window for fade-in

# ---------------- BACKGROUND IMAGE (RESIZED TO SCREEN) ----------------
screen_w = root.winfo_screenwidth()  # get screen width
screen_h = root.winfo_screenheight() # get screen height

# Load and resize background image
img = Image.open(BG_IMAGE)
img = img.resize((screen_w, screen_h), Image.LANCZOS)
bg_img = ImageTk.PhotoImage(img)

# Place background image as a label covering entire window
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relwidth=1, relheight=1)

# ---------------- WHITE BOXES ----------------
# Frame for joke setup
setup_frame = tk.Frame(root, bg="white", bd=4, relief="ridge",
                       highlightbackground="black", highlightcolor="black", highlightthickness=2)
setup_frame.place(relx=0.5, rely=0.14, anchor="center", width=780, height=92)

setup_label = tk.Label(setup_frame, text="", bg="white", fg="black",
                       font=FONT_MAIN, wraplength=740)
setup_label.pack(expand=True)

# Frame for punchline
punch_frame = tk.Frame(root, bg="white", bd=4, relief="ridge",
                       highlightbackground="black", highlightcolor="black", highlightthickness=2)
punch_frame.place(relx=0.5, rely=0.46, anchor="center", width=780, height=92)

punchline_label = tk.Label(punch_frame, text="", bg="white", fg="black",
                           font=FONT_PUNCH, wraplength=740)
punchline_label.pack(expand=True)

# ---------------- BUTTON ANIMATIONS ----------------
def animate_enter(btn):
    # Button hover effect when mouse enters
    btn.config(bg=btn.hover_color, font=("Comic Sans MS", 24, "bold"), bd=8)
    btn.place_configure(relx=btn.relx, rely=btn.rely - 0.005)

def animate_leave(btn):
    # Restore button to original size when mouse leaves
    btn.config(bg=btn.default_color, font=FONT_BUTTON, bd=5)
    btn.place_configure(relx=btn.relx, rely=btn.rely)

# ---------------- BUTTON CREATOR ----------------
def make_button(text, cmd, x, y, color, hover="#ff6f6f"):
    # Create a styled button with hover effect
    btn = tk.Button(root, text=text, command=cmd, font=FONT_BUTTON,
                    width=19, height=1, bg=color, fg="white",
                    activebackground=hover, bd=5, relief="ridge")
    btn.default_color = color
    btn.hover_color = hover
    btn.relx = x
    btn.rely = y
    btn.place(relx=x, rely=y, anchor="center")
    btn.bind("<Enter>", lambda e: animate_enter(btn))
    btn.bind("<Leave>", lambda e: animate_leave(btn))
    return btn

# ---------------- BUTTONS ----------------
make_button("Alexa tell me a Joke", new_joke, 0.50, 0.30, "#ff3b3b")  # tell joke button
make_button("Show Punchline", show_punchline, 0.50, 0.60, "#ff3b3b")   # show punchline button

# Next Joke button (wider)
btn_next = make_button("Next Joke", new_joke, 0.50, 0.72, "#0077ff", hover="#3399ff")
btn_next.config(width=25)

# Quit button
make_button("Quit🚪", lambda: (root.attributes("-fullscreen", False), root.destroy()), 0.50, 0.88, "#333333")

# ---------------- FADE IN ----------------
def fade_in(alpha=0.0):
    # Gradually fade in the main window
    if alpha < 1.0:
        root.attributes("-alpha", alpha)
        root.after(20, lambda: fade_in(alpha + 0.02))
    else:
        root.attributes("-alpha", 1.0)

# ---------------- START ----------------
jokes = load_jokes()  # load jokes from file
current_joke = ("Click the button!", "")  # default text before first joke
fade_in()  # start fade-in animation
root.mainloop()  # run the Tkinter main loop
