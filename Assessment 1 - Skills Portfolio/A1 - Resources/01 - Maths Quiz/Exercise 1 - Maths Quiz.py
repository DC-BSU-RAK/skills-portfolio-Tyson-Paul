import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# Global variables to track quiz state
level = ""
score = 0
correct_answers = 0
wrong_answers = 0
current_question = 1
time_left = 20
attempt = 1
bg_label = None
timer_id = None  # Used to cancel active countdown timer safely

# Function to automatically locate resources (e.g., images) regardless of where script is run
def resource_path(filename):
    # Get the folder where this Python file is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Return the full path to the file in the same directory
    return os.path.join(base_dir, filename)

# Image file paths (stored in the same folder as this Python file)
START_BG = resource_path("background.jpg")
MAIN_BG = resource_path("main_bg.jpg")

# Function to clear all widgets from the window except the background image
def clear_window():
    for widget in window.winfo_children():
        if widget != bg_label:
            widget.destroy()

# Function to set or update background image safely
def set_bg(image_path):
    global bg_label
    try:
        # Load and resize background image to full screen
        img = Image.open(image_path).resize(
            (window.winfo_screenwidth(), window.winfo_screenheight())
        )
        bg_photo = ImageTk.PhotoImage(img)

        # Update the background if it already exists, else create a new one
        if bg_label:
            bg_label.config(image=bg_photo)
            bg_label.image = bg_photo
        else:
            bg_label = tk.Label(window, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"[⚠️] Could not load background: {e}")
        window.configure(bg="#000000")

# Function to animate text color (used for titles and glowing effects)
def animate_color(label, colors, delay=200):
    def loop(i=0):
        if not label.winfo_exists():
            return
        label.config(fg=colors[i])
        window.after(delay, loop, (i + 1) % len(colors))
    loop()

# Function to display text using a typewriter-style animation
def typewriter_effect(label, text, delay=80):
    label.config(text="")
    def loop(i=0):
        if not label.winfo_exists():
            return
        if i <= len(text):
            label.config(text=text[:i])
            window.after(delay, loop, i + 1)
    loop()

# Function to show the start page with options
def show_start_page():
    clear_window()
    set_bg(START_BG)

    # Spacer label for layout
    tk.Label(window, text="", bg="#000000").pack(pady=190)

    # Button style used for main menu buttons
    button_style = {"font": ("Segoe UI Semibold", 28), "width": 15, "bd": 0, "fg": "white"}

    # Main buttons: Start, How to Play, Exit
    tk.Button(window, text="▶ Start", bg="#4CAF50", command=displayMenu, **button_style).pack(pady=10)
    tk.Button(window, text="📘 How to Play", bg="#2196F3", command=show_instructions, **button_style).pack(pady=10)
    tk.Button(window, text="🚪 Exit", bg="#f44336", command=window.destroy, **button_style).pack(pady=10)

# Function to display the “How to Play” instructions screen
def show_instructions():
    clear_window()
    set_bg(MAIN_BG)

    # Animated title
    title = tk.Label(window, text="", font=("Impact", 50), bg="#000000", fg="white")
    title.pack(pady=80)
    typewriter_effect(title, "📘 HOW TO PLAY 📘", delay=80)

    # Game rules text
    instructions = (
        "🧮 1️ Choose your difficulty (Easy / Moderate / Advanced)\n\n"
        "⏳ 2️ You get 10 questions with 20 seconds each\n\n"
        "💥 3️ Correct (1st try) = +10 pts | 2nd try = +5 pts\n\n"
        "❌ 4️ Wrong or timeout = 0 pts\n\n"
        "🏆 5️ Final rank based on total score!"
    )

    # Display the rules
    tk.Label(window, text=instructions, font=("Verdana", 22, "bold"),
             bg="#000000", fg="white", justify="left").pack(pady=20)

    # Back button to return to main screen
    tk.Button(window, text="🔙 Back", font=("Segoe UI Semibold", 22),
              bg="#f44336", fg="white", bd=0, command=show_start_page).pack(pady=40)

# Function to display difficulty selection menu
def displayMenu():
    clear_window()
    set_bg(MAIN_BG)

    # Title
    label = tk.Label(window, text="Select Difficulty Level", font=("Impact", 50), bg="#000000", fg="white")
    label.pack(pady=100)
    animate_color(label, ["#FFD700", "#00E5FF", "#FF1493"], delay=300)

    # Difficulty buttons
    button_style = {"font": ("Segoe UI Semibold", 26), "width": 20, "bd": 0, "fg": "white"}
    tk.Button(window, text="1. Easy 🟢", bg="#4CAF50", command=lambda: start_quiz("Easy"), **button_style).pack(pady=20)
    tk.Button(window, text="2. Moderate 🟡", bg="#FFC107", command=lambda: start_quiz("Moderate"), **button_style).pack(pady=20)
    tk.Button(window, text="3. Advanced 🔴", bg="#f44336", command=lambda: start_quiz("Advanced"), **button_style).pack(pady=20)

    # Back button to go to start screen
    tk.Button(window, text="🔙 Back", font=("Segoe UI Semibold", 22),
              bg="#2196F3", fg="white", bd=0, command=show_start_page).pack(pady=40)

# Function to generate random numbers based on difficulty
def randomInt(level):
    if level == "Easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)

# Function to randomly select operation (+ or -)
def decideOperation():
    return random.choice(["+", "-"])

# Function to display a math question
def displayProblem():
    global num1, num2, operation, attempt, feedback_label, timer_label, time_left, timer_id
    clear_window()
    set_bg(MAIN_BG)

    attempt = 1
    time_left = 20

    # Cancel any previous timer if active
    if timer_id:
        window.after_cancel(timer_id)

    # Display question number
    tk.Label(window, text=f"Question {current_question}/10",
             font=("Impact", 60), bg="#000000", fg="#FFD700").pack(pady=40)

    # Display the question
    q_label = tk.Label(window, text=f"{num1} {operation} {num2} = ?",
                       font=("Impact", 70), bg="#000000", fg="#00E5FF")
    q_label.pack(pady=40)
    animate_color(q_label, ["#00E5FF", "#FFD700", "#FF1493"], delay=300)

    # Input field for user's answer
    frame = tk.Frame(window, bg="#000000")
    frame.pack(pady=20)

    answer_entry = tk.Entry(frame, font=("Verdana", 40, "bold"), width=10, justify="center")
    answer_entry.pack(side="left", padx=5)
    answer_entry.focus()

    # Submit button to check answer
    tk.Button(frame, text="Submit", font=("Segoe UI Semibold", 24),
              bg="#4CAF50", fg="white", bd=0, command=lambda: check_answer(answer_entry.get())).pack(side="left", padx=5)

    # Feedback label (shows correct/wrong messages)
    feedback_label = tk.Label(window, text="", font=("Verdana", 26, "bold"), bg="#000000")
    feedback_label.pack(pady=20)

    # Timer display
    timer_label = tk.Label(window, text=f"⏳ {time_left}s left",
                           font=("Verdana", 30, "bold"), bg="#000000", fg="red")
    timer_label.pack(pady=5)

    # Start countdown timer
    countdown()

    # Display current score summary (bottom)
    tk.Label(window, text=f"✅ {correct_answers}   ❌ {wrong_answers}   🏆 {score}",
             font=("Verdana", 22, "bold"), bg="#000000", fg="white").pack(pady=5)

# Function to handle countdown timer
def countdown():
    global time_left, timer_id
    if time_left > 0:
        time_left -= 1
        if timer_label.winfo_exists():
            timer_label.config(text=f"⏳ {time_left}s left")
        timer_id = window.after(1000, countdown)
    else:
        feedback_label.config(text="⏰ Time’s up!", fg="orange")
        window.after(1500, next_question)

# Function to check user’s submitted answer
def check_answer(answer):
    global score, attempt, correct_answers, wrong_answers, timer_id

    # Stop current timer
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None

    # If answer is correct
    if isCorrect(answer):
        gained = 10 if attempt == 1 else 5
        feedback_label.config(text=f"✅ Correct! +{gained}", fg="lime")
        score += gained
        correct_answers += 1
        window.after(1200, next_question)

    # If answer is wrong
    else:
        if attempt == 1:
            attempt += 1
            feedback_label.config(text="❌ Wrong! Try again!", fg="red")
            countdown()  # Restart timer for second attempt
        else:
            feedback_label.config(text="❌ Wrong again!", fg="red")
            wrong_answers += 1
            window.after(1200, next_question)

# Function to verify correctness of the answer
def isCorrect(user_answer):
    try:
        user_answer = int(user_answer)
    except ValueError:
        return False
    return (num1 + num2 if operation == "+" else num1 - num2) == user_answer

# Function to move to the next question or end the quiz
def next_question():
    global current_question, num1, num2, operation, timer_id
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None

    current_question += 1
    if current_question <= 10:
        num1, num2 = randomInt(level)
        operation = decideOperation()
        window.after(800, displayProblem)
    else:
        window.after(800, displayResults)

# Function to display the results page at the end of the quiz
def displayResults():
    clear_window()
    set_bg(MAIN_BG)

    # Animated “Quiz Complete” title
    label = tk.Label(window, text="🎉 QUIZ COMPLETE 🎉", font=("Impact", 60),
                     bg="#000000", fg="white")
    label.pack(pady=60)
    animate_color(label, ["#FFD700", "#FF1493", "lime"], delay=300)

    # Display final score and correct/wrong counts
    tk.Label(window, text=f"🏆 Score: {score}/100", font=("Verdana", 36, "bold"),
             bg="#000000", fg="white").pack(pady=10)
    tk.Label(window, text=f"✅ Correct: {correct_answers}   ❌ Wrong: {wrong_answers}",
             font=("Verdana", 28, "bold"), bg="#000000", fg="#00E5FF").pack(pady=10)

    # Rank based on total score
    if score >= 100:
        rank, color = "A+ 🌟", "gold"
    elif score >= 85:
        rank, color = "A 🏅", "#61dafb"
    elif score >= 75:
        rank, color = "B 👍", "lime"
    elif score >= 60:
        rank, color = "C 🙂", "orange"
    else:
        rank, color = "D 😢", "red"

    tk.Label(window, text=f"Rank: {rank}", font=("Impact", 45),
             bg="#000000", fg=color).pack(pady=30)

    # Buttons for replay or exit
    tk.Button(window, text="🔁 Play Again", font=("Segoe UI Semibold", 24),
              bg="#4CAF50", fg="white", bd=0, command=show_start_page).pack(pady=15)
    tk.Button(window, text="🚪 Exit", font=("Segoe UI Semibold", 24),
              bg="#f44336", fg="white", bd=0, command=window.destroy).pack(pady=10)

# Function to start a new quiz after difficulty is selected
def start_quiz(chosen_level):
    global level, score, correct_answers, wrong_answers, current_question, num1, num2, operation
    level = chosen_level
    score = 0
    correct_answers = 0
    wrong_answers = 0
    current_question = 1
    num1, num2 = randomInt(level)
    operation = decideOperation()
    displayProblem()

# Create and configure main window
window = tk.Tk()
window.title("Ultimate Maths Quiz")
window.attributes("-fullscreen", True)

# Show the start screen when the program begins
set_bg(START_BG)
show_start_page()

# Run the tkinter event loop
window.mainloop()
