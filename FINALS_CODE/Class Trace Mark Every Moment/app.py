# app.py
from tkinter import *
from tkinter import messagebox
from database import db_instance  # Import the global db_instance from database.py
from instructor_landing import InstructorLanding  # Assuming you have this class defined
from student_landing import StudentLanding  # Assuming you have this class defined
from login import login  # Import the login function

# GUI Setup for Login
app = Tk()
app.title("Login System")
app.geometry("500x300")
app.configure(bg="#ffe4e1")  # Set a light pink background color

# Add a welcome message
Label(app, text="Welcome to Class Trace: Mark Every Moment", 
font=("Arial", 14, "bold"), bg="#ffe4e1", fg="#8b4513").pack(pady=10)  # Brown text

# Username Label and Entry
Label(app, text="Username:", bg="#ffe4e1", fg="#8b4513").pack(pady=5)  # Brown text
username_entry = Entry(app)
username_entry.pack(pady=5)

# Password Label and Entry
Label(app, text="Password:", bg="#ffe4e1", fg="#8b4513").pack(pady=5)  # Brown text
password_entry = Entry(app, show="*")
password_entry.pack(pady=5)

# Login Button
Button(app, text="Login", command=lambda: login(app, username_entry, password_entry)).pack(pady=10)

# Run the main application loop
app.mainloop()