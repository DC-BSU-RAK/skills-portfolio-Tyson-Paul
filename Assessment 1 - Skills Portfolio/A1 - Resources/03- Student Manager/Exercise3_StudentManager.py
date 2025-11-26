import tkinter as tk
from tkinter import messagebox
import os

# ---------------- FILE PATH ----------------
# Get the directory of the current script and define the paths for the data file and logo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "studentMarks.txt")  # Student data
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")  # Optional logo image

# ---------------- DATA HANDLING ---------------
# Load student records from file
def load_students():
    students = []
    if not os.path.exists(FILE_PATH):
        return students  # Return empty list if file does not exist
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

# Save student records back to file
def save_students(students):
    with open(FILE_PATH, "w") as f:
        f.write(str(len(students)) + "\n")  # First line: number of students
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

# ---------------- CALCULATIONS ----------------
# Calculate total coursework score (C1 + C2 + C3)
def total_coursework(s):
    return s["c1"] + s["c2"] + s["c3"]

# Calculate overall percentage based on coursework and exam (total out of 160)
def overall_percentage(s):
    return round(((total_coursework(s) + s["exam"]) / 160) * 100, 2)

# Determine grade based on percentage
def grade(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

# Format a single student's info for display
def format_student(s):
    pct = overall_percentage(s)
    return (
        f"Name: {s['name']}\n"
        f"Student #: {s['code']}\n"
        f"Coursework Total: {total_coursework(s)}/60\n"
        f"Exam: {s['exam']}/100\n"
        f"Percentage: {pct}%\n"
        f"Grade: {grade(pct)}\n"
        + "-"*40 + "\n"
    )

# ---------------- GUI APPLICATION ----------------
class StudentManagerHybrid:
    # Define colors for theme and button hover effects
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

    # ---------------- INITIALIZATION ----------------
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("950x600")
        self.root.configure(bg="#f0f0f8")

        # Load students from file
        self.students = load_students()

        # ---------------- TOP AND BOTTOM FRAMES ----------------
        self.top_frame = tk.Frame(root, bg="#031527", height=120)
        self.top_frame.pack(fill="x")
        self.bottom_frame = tk.Frame(root, bg=self.BG_LIGHT)
        self.bottom_frame.pack(fill="both", expand=True)

        # Title with optional logo
        title_frame = tk.Frame(self.top_frame, bg=self.BG_DARK)
        title_frame.pack(pady=10)
        try:
            self.logo_img = tk.PhotoImage(file=LOGO_PATH)
            self.logo_img = self.logo_img.subsample(4, 4)  # Resize logo
            tk.Label(title_frame, image=self.logo_img, bg=self.BG_DARK).pack(side="left", padx=5)
        except:
            pass
        tk.Label(title_frame, text="Bath Spa University - Student Manager",
                 font=("Bungee Inline", 25, "bold"), bg=self.BG_DARK, fg=self.TEXT_WHITE)\
            .pack(side="left", padx=10)

        # Button panel below title
        self.buttons_frame = tk.Frame(self.top_frame, bg=self.BG_DARK)
        self.buttons_frame.pack()

        # Text output area for displaying student info
        self.output_box = tk.Text(self.bottom_frame, font=("Consolas", 11),
                                  bg=self.BG_LIGHT, fg="#2c3e50")
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10, side="left")

        # Scrollbar for text output
        self.scrollbar = tk.Scrollbar(self.bottom_frame, command=self.output_box.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.output_box.config(yscrollcommand=self.scrollbar.set)

        # Create buttons on the panel
        self.create_buttons_grid()

    # ---------------- HELPER FUNCTIONS ----------------
    # Create a styled button
    def create_button(self, text, command, color, hover):
        btn = tk.Button(self.buttons_frame, text=text, command=command,
                        font=("DM Serif Text", 11, "bold"),
                        bg=color, fg="white",
                        activebackground=hover, bd=3, relief="raised",
                        width=16, height=1)
        return btn

    # Display text in the output box
    def display(self, text):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.config(state="disabled")

    # Popup input for getting student number
    def custom_input(self, title, prompt):
        win = tk.Toplevel()
        win.title(title)
        win.geometry("300x150")
        win.configure(bg=self.BG_DARK)
        tk.Label(win, text=prompt, bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 12, "bold")).pack(pady=15)
        entry = tk.Entry(win, bg=self.BG_LIGHT, fg="#2c3e50",
                         font=("Arial", 12), relief="flat")
        entry.pack(pady=5, ipadx=5, ipady=4)
        result = {"value": None}
        def submit():
            try: result["value"] = int(entry.get())
            except: result["value"] = None
            win.destroy()
        tk.Button(win, text="OK", bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 12, "bold"), relief="flat",
                  command=submit).pack(pady=15)
        win.grab_set()
        win.wait_window()
        return result["value"]

    # ---------------- BUTTON GRID ----------------
    def create_buttons_grid(self):
        # Row 0
        self.create_button("View All", self.view_all, self.GREEN, self.GREEN_HOVER).grid(row=0, column=0, padx=5, pady=5)
        self.create_button("View Individual", self.view_individual, self.BLUE, self.BLUE_HOVER).grid(row=0, column=1, padx=5, pady=5)
        self.create_button("Highest Score", self.show_highest, self.PURPLE, self.PURPLE_HOVER).grid(row=0, column=2, padx=5, pady=5)
        self.create_button("Lowest Score", self.show_lowest, self.RED, self.RED_HOVER).grid(row=0, column=3, padx=5, pady=5)
        # Row 1
        self.create_button("Sort Records", self.sort_records, self.ORANGE, self.ORANGE_HOVER).grid(row=1, column=0, padx=5, pady=5)
        self.create_button("Add Student", self.add_student, "#16a085", "#1abc9c").grid(row=1, column=1, padx=5, pady=5)
        self.create_button("Delete Student", self.delete_student, self.RED, self.RED_HOVER).grid(row=1, column=2, padx=5, pady=5)
        self.create_button("Update Student", self.update_student, "#f39c12", "#f1c40f").grid(row=1, column=3, padx=5, pady=5)

    # ---------------- STUDENT FEATURES ----------------
    # View all student records
    def view_all(self):
        text = ""
        total_percent = 0
        for s in self.students:
            text += format_student(s)
            total_percent += overall_percentage(s)
        avg = round(total_percent / len(self.students), 2) if self.students else 0
        text += f"\nClass Average: {avg}%"
        self.display(text)

    # View individual student by student number
    def view_individual(self):
        code = self.custom_input("View Student", "Enter student number:")
        if code is None: return
        for s in self.students:
            if s["code"] == code:
                self.display(format_student(s))
                return
        messagebox.showerror("Error", "Student not found.")

    # Show highest scoring student
    def show_highest(self):
        if not self.students: messagebox.showinfo("Info", "No student records."); return
        best = max(self.students, key=lambda s: overall_percentage(s))
        self.display("Highest Scoring Student:\n\n" + format_student(best))

    # Show lowest scoring student
    def show_lowest(self):
        if not self.students: messagebox.showinfo("Info", "No student records."); return
        worst = min(self.students, key=lambda s: overall_percentage(s))
        self.display("Lowest Scoring Student:\n\n" + format_student(worst))

    # Popup to choose sort order
    def sort_popup(self):
        win = tk.Toplevel()
        win.title("Sort Records"); win.geometry("300x180"); win.configure(bg=self.BG_DARK)
        tk.Label(win, text="Sort by percentage:", bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 12, "bold")).pack(pady=15)
        result = {"choice": None}
        tk.Button(win, text="Ascending", bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 12, "bold"), relief="flat",
                  command=lambda: [result.update({"choice":"asc"}), win.destroy()]).pack(pady=5, ipadx=10, ipady=5)
        tk.Button(win, text="Descending", bg=self.RED, fg=self.TEXT_WHITE,
                  font=("Arial", 12, "bold"), relief="flat",
                  command=lambda: [result.update({"choice":"desc"}), win.destroy()]).pack(pady=5, ipadx=10, ipady=5)
        win.grab_set(); win.wait_window()
        return result["choice"]

    # Sort student records
    def sort_records(self):
        choice = self.sort_popup()
        if not choice: return
        self.students.sort(key=lambda s: overall_percentage(s), reverse=(choice=="desc"))
        save_students(self.students)
        messagebox.showinfo("Sorted", "Records sorted successfully.")
        self.view_all()

    # Add a new student
    def add_student(self):
        win = tk.Toplevel(); win.title("Add Student"); win.geometry("330x480"); win.configure(bg=self.BG_DARK)
        tk.Label(win, text="Add New Student", bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 18, "bold")).pack(pady=10)
        labels = ["Code","Name","C1","C2","C3","Exam"]; entries={}
        for lbl in labels:
            tk.Label(win, text=lbl, bg=self.BG_DARK, fg=self.TEXT_WHITE, font=("Arial", 12, "bold")).pack(pady=5)
            e = tk.Entry(win, bg="#dcdde1", fg="#2f3640", font=("Arial", 12), relief="flat")
            e.pack(pady=2, ipadx=4, ipady=4); entries[lbl]=e

        def save_student():
            try:
                s={"code":int(entries["Code"].get()),"name":entries["Name"].get(),
                   "c1":int(entries["C1"].get()),"c2":int(entries["C2"].get()),
                   "c3":int(entries["C3"].get()),"exam":int(entries["Exam"].get())}
            except: messagebox.showerror("Error","Invalid input."); return
            self.students.append(s); save_students(self.students)
            messagebox.showinfo("Added","Student added successfully."); win.destroy(); self.view_all()

        tk.Button(win, text="SAVE STUDENT", command=save_student, bg=self.GREEN, fg=self.TEXT_WHITE,
                  font=("Arial", 14, "bold"), relief="flat", width=20).pack(pady=20)

    # Delete student by code
    def delete_student(self):
        code = self.custom_input("Delete Student", "Enter student number:")
        if code is None: return
        for s in self.students:
            if s["code"]==code: self.students.remove(s); save_students(self.students); messagebox.showinfo("Deleted","Student removed."); self.view_all(); return
        messagebox.showerror("Error","Student not found.")

    # Update student by code
    def update_student(self):
        code = self.custom_input("Update Student", "Enter student number:")
        if code is None: return
        for s in self.students:
            if s["code"]==code: self.edit_student_window(s); return
        messagebox.showerror("Error","Student not found.")

    # Popup to edit student details
    def edit_student_window(self, s):
        win = tk.Toplevel(); win.title(f"Update {s['name']}"); win.geometry("330x420"); win.configure(bg=self.BG_DARK)
        tk.Label(win, text="Update Student", bg=self.BG_DARK, fg=self.TEXT_WHITE,
                 font=("Arial", 18, "bold")).pack(pady=10)
        labels = ["Name","C1","C2","C3","Exam"]; entries={}
        for lbl in labels:
            tk.Label(win, text=lbl, bg=self.BG_DARK, fg=self.TEXT_WHITE, font=("Arial", 12, "bold")).pack(pady=5)
            e = tk.Entry(win, bg="#dcdde1", fg="#2f3640", font=("Arial", 12), relief="flat"); e.pack(pady=2, ipadx=4, ipady=4)
            entries[lbl]=e

        # Pre-fill current student info
        entries["Name"].insert(0,s["name"]); entries["C1"].insert(0,s["c1"]); entries["C2"].insert(0,s["c2"])
        entries["C3"].insert(0,s["c3"]); entries["Exam"].insert(0,s["exam"])

        # Save changes
        def save_changes():
            try: s["name"]=entries["Name"].get(); s["c1"]=int(entries["C1"].get()); s["c2"]=int(entries["C2"].get()); s["c3"]=int(entries["C3"].get()); s["exam"]=int(entries["Exam"].get())
            except: messagebox.showerror("Error","Invalid input."); return
            save_students(self.students); messagebox.showinfo("Updated","Student updated successfully."); win.destroy(); self.view_all()

        tk.Button(win, text="SAVE CHANGES", command=save_changes, bg=self.BLUE, fg=self.TEXT_WHITE,
                  font=("Arial", 14, "bold"), relief="flat", width=20).pack(pady=20)

# ---------------- RUN APPLICATION ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerHybrid(root)
    root.mainloop()
