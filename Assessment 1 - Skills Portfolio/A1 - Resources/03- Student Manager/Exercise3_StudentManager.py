import tkinter as tk
from tkinter import messagebox
import os

# ---------------- FILE PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get directory of current script
FILE_PATH = os.path.join(BASE_DIR, "studentMarks.txt")  # Path to data file
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")  # Path to logo image
PERSON_ICON_PATH = os.path.join(BASE_DIR, "person.png")  # Path to person icon image

# ---------------- DATA HANDLING ----------------
def load_students():
    # Load students data from the text file into a list of dictionaries
    students = []
    if not os.path.exists(FILE_PATH):
        return students  # Return empty list if file doesn't exist
    with open(FILE_PATH, "r") as f:
        lines = f.read().strip().split("\n")
        for line in lines[1:]:  # Skip first line (count)
            parts = line.split(",")
            students.append({
                "code": int(parts[0]),
                "name": parts[1],
                "c1": int(parts[2]),
                "c2": int(parts[3]),
                "c3": int(parts[4]),
                "exam": int(parts[5])
            })
    return students

def save_students(students):
    # Save the students list back to the text file in the expected format
    with open(FILE_PATH, "w") as f:
        f.write(str(len(students)) + "\n")  # First line is total count
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

def total_coursework(s):
    # Calculate total coursework marks from 3 components
    return s["c1"] + s["c2"] + s["c3"]

def overall_percentage(s):
    # Calculate overall percentage out of 160 (60 coursework + 100 exam)
    return round(((total_coursework(s) + s["exam"]) / 160) * 100, 2)

def grade(p):
    # Return grade based on percentage boundaries
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

# ---------------- GUI APPLICATION ----------------
class StudentManagerHybrid:
    # Define color constants for the UI
    BG_LIGHT = "#ecf0f1"
    BG_DARK = "#2c3e50"
    TEXT_WHITE = "white"
    GREEN = "#27ae60"
    GREEN_HOVER = "#2ecc71"
    RED = "#c0392b"
    RED_HOVER = "#e74c3c"
    ORANGE = "#d35400"
    ORANGE_HOVER = "#e67e22"
    BLUE = "#2980b9"
    BLUE_HOVER = "#3498db"
    PURPLE = "#8e44ad"
    PURPLE_HOVER = "#9b59b6"
    BOX_HOVER = "#d1e7ff"

    def __init__(self, root):
        # Initialize main window and UI components
        self.root = root
        self.root.title("BSU Student Manager")
        self.root.state("zoomed")  # Maximize window
        self.root.configure(bg=self.BG_LIGHT)

        # Try to set main window icon if logo exists
        try:
            self.icon_img = tk.PhotoImage(file=LOGO_PATH)
            self.root.iconphoto(False, self.icon_img)
        except:
            pass

        # Load student records from file
        self.students = load_students()

        # Load person icon for student display boxes
        try:
            self.person_img = tk.PhotoImage(file=PERSON_ICON_PATH)
            self.person_img_small = self.person_img.subsample(20, 20)  # Make icon smaller
        except:
            self.person_img_small = None

        # Create top frame with title and buttons
        self.top_frame = tk.Frame(root, bg=self.BG_DARK, height=120)
        self.top_frame.pack(fill="x")

        title_frame = tk.Frame(self.top_frame, bg=self.BG_DARK)
        title_frame.pack(pady=10)

        # Display logo in title bar if available
        try:
            self.logo_img = tk.PhotoImage(file=LOGO_PATH)
            self.logo_img_small = self.logo_img.subsample(4, 4)
            tk.Label(title_frame, image=self.logo_img_small, bg=self.BG_DARK).pack(side="left", padx=5)
        except:
            self.logo_img_small = None

        # University title label
        tk.Label(title_frame, text="Bath Spa University - Student Manager",
                 font=("Bungee Inline", 25, "bold"), bg=self.BG_DARK, fg=self.TEXT_WHITE)\
            .pack(side="left", padx=10)

        # Buttons frame below title for operations
        self.buttons_frame = tk.Frame(self.top_frame, bg=self.BG_DARK)
        self.buttons_frame.pack()
        self.create_buttons_grid()

        # Bottom frame to display student info or lists
        self.bottom_frame = tk.Frame(root, bg=self.BG_LIGHT)
        self.bottom_frame.pack(fill="both", expand=True)

    # ---------------- BUTTON CREATION ----------------
    def create_button(self, text, command, color, hover):
        # Helper function to create styled buttons with hover color
        btn = tk.Button(self.buttons_frame, text=text, command=command,
                        font=("DM Serif Text", 11, "bold"),
                        bg=color, fg="white", activebackground=hover, bd=3, relief="raised",
                        width=16, height=1)
        return btn

    def create_buttons_grid(self):
        # Create and place all main buttons on the top panel grid
        self.create_button("View All", self.view_all, self.GREEN, self.GREEN_HOVER).grid(row=0, column=0, padx=5, pady=5)
        self.create_button("View Individual", self.view_individual, self.BLUE, self.BLUE_HOVER).grid(row=0, column=1, padx=5, pady=5)
        self.create_button("Highest Score", self.show_highest, self.PURPLE, self.PURPLE_HOVER).grid(row=0, column=2, padx=5, pady=5)
        self.create_button("Lowest Score", self.show_lowest, self.RED, self.RED_HOVER).grid(row=0, column=3, padx=5, pady=5)
        self.create_button("Sort Records", self.sort_records, self.ORANGE, self.ORANGE_HOVER).grid(row=1, column=0, padx=5, pady=5)
        self.create_button("Add Student", self.add_student, "#16a085", "#1abc9c").grid(row=1, column=1, padx=5, pady=5)
        self.create_button("Delete Student", self.delete_student, self.RED, self.RED_HOVER).grid(row=1, column=2, padx=5, pady=5)
        self.create_button("Update Student", self.update_student, "#f39c12", "#f1c40f").grid(row=1, column=3, padx=5, pady=5)

    # ---------------- INPUT VALIDATION POPUP ----------------
    def custom_input(self, title, prompt):
        # Pop-up window to get integer input with validation
        win = tk.Toplevel()
        win.title(title)
        win.geometry("300x150")
        win.configure(bg=self.BG_DARK)
        
        # ------------------ Set popup icon ------------------
        try:
            logo_img = tk.PhotoImage(file=LOGO_PATH)  # Load logo.png
            win.iconphoto(False, logo_img)            # Set as window icon
        except Exception as e:
            print(f"[⚠️] Could not load popup icon: {e}")

        tk.Label(win, text=prompt, bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 12, "bold")).pack(pady=15)

        entry = tk.Entry(win, bg=self.BG_LIGHT, fg="#2c3e50",
                         font=("Arial", 12), relief="flat")
        entry.pack(pady=5, ipadx=5, ipady=4)

        result = {"value": None}  # Mutable container to store input

        def submit():
            val = entry.get()
            if val.strip() == "":
                messagebox.showerror("Error", "Input cannot be empty.")
                return
            try:
                result["value"] = int(val)  # Try converting to integer
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer.")
                return

        tk.Button(win, text="OK", bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 12, "bold"), relief="flat",
                  command=submit).pack(pady=15)

        win.grab_set()  # Make this popup modal
        win.wait_window()  # Wait until closed
        return result["value"]

    # ---------------- STUDENT DISPLAY BOX ----------------
    def create_student_box(self, parent, student):
        # Create a box widget displaying the student's details with hover effect
        box_width = 280
        box_height = 200

        box = tk.Frame(parent, bg="white", bd=2, relief="groove", padx=10, pady=10, width=box_width, height=box_height)
        box.pack_propagate(False)  # Fix box size

        # Display person icon if available
        if self.person_img_small:
            tk.Label(box, image=self.person_img_small, bg="white").pack(pady=(0,5))

        # Display student info labels
        tk.Label(box, text=f"Name: {student['name']}", font=("Arial", 12, "bold"), bg="white", fg="#2980b9").pack(anchor="center")
        tk.Label(box, text=f"Student #: {student['code']}", font=("Arial",11), bg="white").pack(anchor="center")
        tk.Label(box, text=f"Coursework Total: {total_coursework(student)}/60", font=("Arial",11), bg="white").pack(anchor="center")
        tk.Label(box, text=f"Exam: {student['exam']}/100", font=("Arial",11), bg="white").pack(anchor="center")
        pct = overall_percentage(student)
        tk.Label(box, text=f"Percentage: {pct}%", font=("Arial",11), bg="white").pack(anchor="center")
        tk.Label(box, text=f"Grade: {grade(pct)}", font=("Arial",11,"bold"), bg="white").pack(anchor="center")

        # Hover effect: change background on mouse enter/leave
        def on_enter(e): box.config(bg=self.BOX_HOVER)
        def on_leave(e): box.config(bg="white")
        box.bind("<Enter>", on_enter)
        box.bind("<Leave>", on_leave)
        return box

    def view_all(self):
        # Display all students in a scrollable grid of boxes
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()  # Clear previous content

        canvas = tk.Canvas(self.bottom_frame, bg=self.BG_LIGHT)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.bottom_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas, bg=self.BG_LIGHT)
        canvas.create_window((0,0), window=frame, anchor="nw")

        max_cols = 4  # Number of columns in grid
        row = col = 0
        for s in self.students:
            box = self.create_student_box(frame, s)
            box.grid(row=row, column=col, padx=10, pady=10)
            frame.grid_columnconfigure(col, weight=1)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # ---------------- STUDENT VIEW/SEARCH ----------------
    def view_individual(self):
        # Prompt for student number and display individual student's info
        code = self.custom_input("View Student", "Enter student number:")
        if code is None:  # Cancelled or invalid input
            return
        for s in self.students:
            if s["code"] == code:
                self.view_single_student(s)
                return
        messagebox.showerror("Error", "Student not found.")

    def view_single_student(self, student):
        # Display single student box on bottom frame
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        box = self.create_student_box(self.bottom_frame, student)
        box.pack(padx=20, pady=20)

    # ---------------- HIGHEST / LOWEST SCORER ----------------
    def show_highest(self):
        # Show student with highest overall percentage
        if not self.students: return
        best = max(self.students, key=lambda s: overall_percentage(s))
        self.view_single_student(best)

    def show_lowest(self):
        # Show student with lowest overall percentage
        if not self.students: return
        worst = min(self.students, key=lambda s: overall_percentage(s))
        self.view_single_student(worst)

    # ---------------- SORTING RECORDS ----------------
    def sort_popup(self):
        # Popup window to choose ascending or descending sorting
        win = tk.Toplevel()
        win.title("Sort Records")
        win.geometry("300x180")
        win.configure(bg=self.BG_DARK)
        
        # ------------------ Set popup icon ------------------
        try:
            logo_img = tk.PhotoImage(file=LOGO_PATH)  # Load logo.png
            win.iconphoto(False, logo_img)            # Set as window icon
        except Exception as e:
            print(f"[⚠️] Could not load popup icon: {e}")

        tk.Label(win, text="Sort by percentage:", bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 12, "bold")).pack(pady=15)

        result = {"choice": None}

        tk.Button(win, text="Ascending", bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 12, "bold"), relief="flat",
                  command=lambda: [result.update({"choice":"asc"}), win.destroy()]).pack(pady=5, ipadx=10, ipady=5)

        tk.Button(win, text="Descending", bg=self.RED, fg=self.TEXT_WHITE,
                  font=("Arial", 12, "bold"), relief="flat",
                  command=lambda: [result.update({"choice":"desc"}), win.destroy()]).pack(pady=5, ipadx=10, ipady=5)

        win.grab_set()
        win.wait_window()

        return result["choice"]

    def sort_records(self):
        # Sort student list by overall percentage and save
        choice = self.sort_popup()
        if not choice: return
        self.students.sort(key=lambda s: overall_percentage(s), reverse=(choice=="desc"))
        save_students(self.students)
        messagebox.showinfo("Sorted", "Records sorted successfully.")
        self.view_all()

    # ---------------- ADD NEW STUDENT ----------------
    def add_student(self):
        # Popup window to add new student details
        win = tk.Toplevel()
        win.title("Add Student")
        win.geometry("330x480")
        win.configure(bg=self.BG_DARK)
        
        # ------------------ Set popup icon ------------------
        try:
            logo_img = tk.PhotoImage(file=LOGO_PATH)
            win.iconphoto(False, logo_img)
        except Exception as e:
            print(f"[⚠️] Could not load popup icon: {e}")

        tk.Label(win, text="Add New Student", bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 18, "bold")).pack(pady=10)

        labels = ["Code","Name","C1","C2","C3","Exam"]
        entries = {}

        # Create entry widgets for each field
        for lbl in labels:
            tk.Label(win, text=lbl, bg=self.BG_DARK, fg=self.TEXT_WHITE, font=("Arial", 12, "bold")).pack(pady=5)
            e = tk.Entry(win, bg="#dcdde1", fg="#2f3640", font=("Arial", 12), relief="flat")
            e.pack(pady=2, ipadx=4, ipady=4)
            entries[lbl] = e

        def save_student():
            # Validate and save new student data
            try:
                code_val = int(entries["Code"].get())
                c1_val = int(entries["C1"].get())
                c2_val = int(entries["C2"].get())
                c3_val = int(entries["C3"].get())
                exam_val = int(entries["Exam"].get())
                name_val = entries["Name"].get().strip()
                if name_val == "":
                    messagebox.showerror("Error", "Name cannot be empty.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Code, C1, C2, C3, and Exam must be integers.")
                return

            s = {"code": code_val, "name": name_val, "c1": c1_val, "c2": c2_val, "c3": c3_val, "exam": exam_val}
            self.students.append(s)
            save_students(self.students)
            messagebox.showinfo("Added","Student added successfully.")
            win.destroy()
            self.view_all()

        # Save button
        tk.Button(win, text="SAVE STUDENT", command=save_student, bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 14, "bold"), relief="flat", width=20).pack(pady=20)

    # ---------------- DELETE STUDENT ----------------
    def delete_student(self):
        # Prompt for student number, remove if found
        code = self.custom_input("Delete Student", "Enter student number:")
        if code is None: return
        for s in self.students:
            if s["code"]==code:
                self.students.remove(s)
                save_students(self.students)
                messagebox.showinfo("Deleted","Student removed.")
                self.view_all()
                return
        messagebox.showerror("Error","Student not found.")

    # ---------------- UPDATE STUDENT ----------------
    def update_student(self):
        # Prompt for student number, open update window if found
        code = self.custom_input("Update Student", "Enter student number:")
        if code is None: return
        for s in self.students:
            if s["code"]==code:
                self.edit_student_window(s)
                return
        messagebox.showerror("Error","Student not found.")

    def edit_student_window(self, student):
        # Popup window to edit existing student info
        win = tk.Toplevel()
        win.title("Edit Student")
        win.geometry("330x480")
        win.configure(bg=self.BG_DARK)

        # ------------------ Set popup icon ------------------
        try:
            logo_img = tk.PhotoImage(file=LOGO_PATH)
            win.iconphoto(False, logo_img)
        except Exception as e:
            print(f"[⚠️] Could not load popup icon: {e}")

        tk.Label(win, text=f"Edit Student #{student['code']}", bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 18, "bold")).pack(pady=10)

        labels = ["Name","C1","C2","C3","Exam"]
        entries = {}

        # Create entry widgets with pre-filled values
        for lbl in labels:
            tk.Label(win, text=lbl, bg=self.BG_DARK, fg=self.TEXT_WHITE, font=("Arial", 12, "bold")).pack(pady=5)
            e = tk.Entry(win, bg="#dcdde1", fg="#2f3640", font=("Arial", 12), relief="flat")
            e.pack(pady=2, ipadx=4, ipady=4)
            entries[lbl] = e

        # Pre-fill existing values
        entries["Name"].insert(0, student["name"])
        entries["C1"].insert(0, str(student["c1"]))
        entries["C2"].insert(0, str(student["c2"]))
        entries["C3"].insert(0, str(student["c3"]))
        entries["Exam"].insert(0, str(student["exam"]))

        def save_edit():
            # Save edited data back to student object
            try:
                student["name"] = entries["Name"].get().strip()
                student["c1"] = int(entries["C1"].get())
                student["c2"] = int(entries["C2"].get())
                student["c3"] = int(entries["C3"].get())
                student["exam"] = int(entries["Exam"].get())
                if student["name"] == "":
                    messagebox.showerror("Error","Name cannot be empty.")
                    return
            except ValueError:
                messagebox.showerror("Error","C1, C2, C3, Exam must be integers.")
                return
            save_students(self.students)
            messagebox.showinfo("Updated","Student updated successfully.")
            win.destroy()
            self.view_all()

        tk.Button(win, text="SAVE CHANGES", command=save_edit, bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 14, "bold"), relief="flat", width=20).pack(pady=20)

# ---------------- RUN APPLICATION ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerHybrid(root)
    root.mainloop()
