import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# ---------------- GLOBAL VARIABLES ----------------
level = ""                  # Difficulty level selected (Easy, Moderate, Advanced)
score = 0                   # Total score accumulated
correct_answers = 0         # Number of correctly answered questions
wrong_answers = 0           # Number of wrong answers or timed out questions
current_question = 1        # Tracks which question number user is on (1 to 10)
time_left = 20              # Countdown timer for each question
attempt = 1                 # Tracks first or second attempt per question
bg_label = None             # Holds background image label
timer_id = None             # Holds timer callback ID to cancel countdown safely

# ---------------- RESOURCE HANDLING ----------------
def resource_path(filename):
    """
    Get the absolute path for a file in the same folder as the script.
    Useful for images and assets.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

# Paths for background images
START_BG = resource_path("background.jpg")
MAIN_BG = resource_path("main_bg.jpg")

# ---------------- WINDOW UTILITIES ----------------
def clear_window():
    """
    Clear all widgets from the window except the background image.
    This prevents overlapping widgets when switching pages.
    """
    for widget in window.winfo_children():
        if widget != bg_label:
            widget.destroy()

def set_bg(image_path):
    """
    Set a background image for the window.
    If it fails, set a plain black background.
    """
    global bg_label
    try:
        img = Image.open(image_path).resize(
            (window.winfo_screenwidth(), window.winfo_screenheight())
        )
        bg_photo = ImageTk.PhotoImage(img)

        if bg_label:  # Update existing label
            bg_label.config(image=bg_photo)
            bg_label.image = bg_photo
        else:  # Create new label
            bg_label = tk.Label(window, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"[⚠️] Could not load background: {e}")
        window.configure(bg="#000000")

# ---------------- ANIMATION UTILITIES ----------------
def animate_color(label, colors, delay=200):
    """
    Cycle through colors on a label for a glowing or flashing effect.
    label: the tk.Label to animate
    colors: list of color hex codes
    delay: milliseconds between color changes
    """
    def loop(i=0):
        if not label.winfo_exists():  # Stop if label no longer exists
            return
        label.config(fg=colors[i])
        window.after(delay, loop, (i + 1) % len(colors))
    loop()

def typewriter_effect(label, text, delay=80):
    """
    Display text on a label one character at a time (typewriter style).
    label: the tk.Label to show text
    text: the string to display
    delay: milliseconds between characters
    """
    label.config(text="")
    def loop(i=0):
        if not label.winfo_exists():
            return
        if i <= len(text):
            label.config(text=text[:i])
            window.after(delay, loop, i + 1)
    loop()

# ---------------- START PAGE ----------------
def show_start_page():
    """
    Display the main menu with Start, How to Play, and Exit buttons.
    """
    clear_window()
    set_bg(START_BG)
    tk.Label(window, text="", bg="#000000").pack(pady=190)  # Spacer for alignment

    button_style = {"font": ("Segoe UI Semibold", 28), "width": 15, "bd": 0, "fg": "white"}

    # Start button → goes to difficulty selection
    tk.Button(window, text="▶ Start", bg="#4CAF50", command=displayMenu, **button_style).pack(pady=10)
    # How to play → instructions page
    tk.Button(window, text="📘 How to Play", bg="#2196F3", command=show_instructions, **button_style).pack(pady=10)
    # Exit → closes the program
    tk.Button(window, text="🚪 Exit", bg="#f44336", command=window.destroy, **button_style).pack(pady=10)

# ---------------- INSTRUCTIONS PAGE ----------------
def show_instructions():
    """
    Display instructions for the game.
    Explains difficulty, scoring rules, number of questions, and ranks.
    """
    clear_window()
    set_bg(MAIN_BG)

    # Animated title
    title = tk.Label(window, text="", font=("Impact", 50), bg="#000000", fg="white")
    title.pack(pady=80)
    typewriter_effect(title, "📘 HOW TO PLAY 📘", delay=80)

    instructions = (
        "🧮 1️ Choose your difficulty (Easy / Moderate / Advanced)\n\n"
        "⏳ 2️ You get 10 questions with 20 seconds each\n\n"
        "💥 3️ Correct (1st try) = +10 pts | 2nd try = +5 pts\n\n"
        "❌ 4️ Wrong or timeout = 0 pts\n\n"
        "🏆 5️ Final rank based on total score!"
    )

    tk.Label(window, text=instructions, font=("Verdana", 22, "bold"),
             bg="#000000", fg="white", justify="left").pack(pady=20)

    # Back button → return to start page
    tk.Button(window, text="🔙 Back", font=("Segoe UI Semibold", 22),
              bg="#f44336", fg="white", bd=0, command=show_start_page).pack(pady=40)

# ---------------- DIFFICULTY MENU ----------------
def displayMenu():
    """
    Let the player select a difficulty level.
    Starts the quiz with the chosen difficulty.
    """
    clear_window()
    set_bg(MAIN_BG)

    label = tk.Label(window, text="Select Difficulty Level", font=("Impact", 50), bg="#000000", fg="white")
    label.pack(pady=100)
    animate_color(label, ["#FFD700", "#00E5FF", "#FF1493"], delay=300)

    button_style = {"font": ("Segoe UI Semibold", 26), "width": 20, "bd": 0, "fg": "white"}
    tk.Button(window, text="1. Easy 🟢", bg="#4CAF50", command=lambda: start_quiz("Easy"), **button_style).pack(pady=20)
    tk.Button(window, text="2. Moderate 🟡", bg="#FFC107", command=lambda: start_quiz("Moderate"), **button_style).pack(pady=20)
    tk.Button(window, text="3. Advanced 🔴", bg="#f44336", command=lambda: start_quiz("Advanced"), **button_style).pack(pady=20)

    tk.Button(window, text="🔙 Back", font=("Segoe UI Semibold", 22),
              bg="#2196F3", fg="white", bd=0, command=show_start_page).pack(pady=40)

# ---------------- QUIZ GENERATION ----------------
def randomInt(level):
    """
    Generate two random numbers based on difficulty level.
    """
    if level == "Easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)

def decideOperation():
    """
    Randomly return '+' or '-' for addition or subtraction questions.
    """
    return random.choice(["+", "-"])

# ---------------- QUIZ DISPLAY ----------------
def displayProblem():
    """
    Display a single math problem with entry box, timer, feedback, and Quit button.
    Handles first and second attempts.
    """
    global num1, num2, operation, attempt, feedback_label, timer_label, time_left, timer_id
    clear_window()
    set_bg(MAIN_BG)

    attempt = 1
    time_left = 20

    # Cancel previous timer if exists
    if timer_id:
        window.after_cancel(timer_id)

    # Quit button → return to main menu
    tk.Button(window, text="🚪 Quit", font=("Segoe UI Semibold", 18), bg="#f44336", fg="white",
              bd=0, command=show_start_page).place(x=20, y=20)

    # Display question number
    tk.Label(window, text=f"Question {current_question}/10",
             font=("Impact", 60), bg="#000000", fg="#FFD700").pack(pady=40)

    # Display math question
    q_label = tk.Label(window, text=f"{num1} {operation} {num2} = ?",
                       font=("Impact", 70), bg="#000000", fg="#00E5FF")
    q_label.pack(pady=40)
    animate_color(q_label, ["#00E5FF", "#FFD700", "#FF1493"], delay=300)

    # Input frame and entry
    frame = tk.Frame(window, bg="#000000")
    frame.pack(pady=20)
    answer_entry = tk.Entry(frame, font=("Verdana", 40, "bold"), width=10, justify="center")
    answer_entry.pack(side="left", padx=5)
    answer_entry.focus()

    # Submit button → check answer
    tk.Button(frame, text="Submit", font=("Segoe UI Semibold", 24),
              bg="#4CAF50", fg="white", bd=0, command=lambda: check_answer(answer_entry.get())).pack(side="left", padx=5)

    # Feedback label → shows correct/wrong messages
    feedback_label = tk.Label(window, text="", font=("Verdana", 26, "bold"), bg="#000000")
    feedback_label.pack(pady=20)

    # Timer label → shows countdown
    timer_label = tk.Label(window, text=f"⏳ {time_left}s left",
                           font=("Verdana", 30, "bold"), bg="#000000", fg="red")
    timer_label.pack(pady=5)

    countdown()  # Start countdown timer

    # Display score summary
    tk.Label(window, text=f"✅ {correct_answers}   ❌ {wrong_answers}   🏆 {score}",
             font=("Verdana", 22, "bold"), bg="#000000", fg="white").pack(pady=5)

# ---------------- TIMER ----------------
def countdown():
    """
    Countdown timer for the current question.
    Updates timer label every second.
    If time runs out, moves to next question.
    """
    global time_left, timer_id
    if time_left > 0:
        time_left -= 1
        if timer_label.winfo_exists():
            timer_label.config(text=f"⏳ {time_left}s left")
        timer_id = window.after(1000, countdown)
    else:
        feedback_label.config(text="⏰ Time’s up!", fg="orange")
        window.after(1500, next_question)

# ---------------- ANSWER CHECK ----------------
def check_answer(answer):
    """
    Validate the user's answer.
    Update score, feedback, and attempt counter.
    Handles first attempt (10 pts) and second attempt (5 pts).
    """
    global score, attempt, correct_answers, wrong_answers, timer_id

    # Stop timer while checking
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None

    if isCorrect(answer):
        gained = 10 if attempt == 1 else 5
        feedback_label.config(text=f"✅ Correct! +{gained}", fg="lime")
        score += gained
        correct_answers += 1
        window.after(1200, next_question)
    else:
        if attempt == 1:
            attempt += 1
            feedback_label.config(text="❌ Wrong! Try again!", fg="red")
            countdown()  # Restart timer for second attempt
        else:
            feedback_label.config(text="❌ Wrong again!", fg="red")
            wrong_answers += 1
            window.after(1200, next_question)

def isCorrect(user_answer):
    """
    Check if the entered answer is correct.
    Returns True if correct, False otherwise.
    """
    try:
        user_answer = int(user_answer)
    except ValueError:
        return False
    return (num1 + num2 if operation == "+" else num1 - num2) == user_answer

# ---------------- QUESTION FLOW ----------------
def next_question():
    """
    Move to the next question or end the quiz if all 10 questions are done.
    """
    global current_question, num1, num2, operation, timer_id
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None

    current_question += 1
    if current_question <= 10:
        num1, num2 = randomInt(level)
        operation = decideOperation()
        window.after(800, displayProblem)  # Small delay before next question
    else:
        window.after(800, displayResults)  # Show results after last question

# ---------------- RESULTS PAGE ----------------
def displayResults():
    """
    Show final score, correct/wrong answers, and rank.
    Also provides buttons to play again or exit.
    """
    clear_window()
    set_bg(MAIN_BG)

    label = tk.Label(window, text="🎉 QUIZ COMPLETE 🎉", font=("Impact", 60),
                     bg="#000000", fg="white")
    label.pack(pady=60)
    animate_color(label, ["#FFD700", "#FF1493", "lime"], delay=300)

    # Display final score
    tk.Label(window, text=f"🏆 Score: {score}/100", font=("Verdana", 36, "bold"),
             bg="#000000", fg="white").pack(pady=10)
    tk.Label(window, text=f"✅ Correct: {correct_answers}   ❌ Wrong: {wrong_answers}",
             font=("Verdana", 28, "bold"), bg="#000000", fg="#00E5FF").pack(pady=10)

    # Assign rank based on score
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

    # Buttons to restart quiz or exit
    tk.Button(window, text="🔁 Play Again", font=("Segoe UI Semibold", 24),
              bg="#4CAF50", fg="white", bd=0, command=show_start_page).pack(pady=15)
    tk.Button(window, text="🚪 Exit", font=("Segoe UI Semibold", 24),
              bg="#f44336", fg="white", bd=0, command=window.destroy).pack(pady=10)

# ---------------- START QUIZ ----------------
def start_quiz(chosen_level):
    """
    Initialize all quiz variables and start the first question.
    chosen_level: difficulty selected by user
    """
    global level, score, correct_answers, wrong_answers, current_question, num1, num2, operation
    level = chosen_level
    score = 0
    correct_answers = 0
    wrong_answers = 0
    current_question = 1
    num1, num2 = randomInt(level)
    operation = decideOperation()
    displayProblem()

# ---------------- MAIN WINDOW ----------------
window = tk.Tk()
window.title("Ultimate Maths Quiz")
window.attributes("-fullscreen", True)  # Fullscreen mode

# Show start page initially
set_bg(START_BG)
show_start_page()

# Run the main Tkinter loop
window.mainloop()
