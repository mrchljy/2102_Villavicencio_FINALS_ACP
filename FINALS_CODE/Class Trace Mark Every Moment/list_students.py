import logging
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox
from tkinter import ttk  # Import for ComboBox

class List_users:
    def __init__(self, connection):
        self.connection = connection
        self.all_users_data = []

    def fetch_all_users(self):
        """Fetch all users (students and instructors) from the database."""
        if not self.connection:
            print("Error: No valid database connection.")
            return None, 0

        try:
            query = """
                SELECT id, fname, mname, lname, username, role FROM users
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            if result:
                self.all_users_data = result
                total_users = len(result)  # Count total users
                return result, total_users
            else:
                print("No users found in the database.")
                return [], 0

        except Exception as e:
            logging.error(f"Error fetching all users: {e}")
            print(f"Error fetching all users: {e}")
            return [], 0


            
    def show_users(self):
        """Display the list of all users in a new window."""
        print('click')
        
        user_list_window = Toplevel()
        user_list_window.title("User List")
        
        # Fetch data and total count of users
        users, total_users = self.fetch_all_users()
        
        # Display user list
        if users:
            self.all_users_table(user_list_window)
        
        # Display total user count
        total_label = Label(user_list_window, text=f"Total Users: {total_users}")
        total_label.pack(pady=10)



    def add_user(self, first_name, middle_name, last_name, username, password, role):
        """Add a new user to the database."""
        try:
            check_query = """
                SELECT 1 FROM users WHERE username = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(check_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
                cursor.close()
                return False
            
            query = """
                INSERT INTO users (fname, mname, lname, username, password, role) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (first_name, middle_name, last_name, username, password, role)

            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            
            return True
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            print(f"Error adding user: {e}")
            return False

    def update_user(self, user_id, first_name, middle_name, last_name, username, password, role):
        """Update user details in the database."""
        try:
            # Handle the optional middle name by checking if it's empty
            if middle_name:  # If middle name is provided
                query = """
                    UPDATE users
                    SET fname = %s, mname = %s, lname = %s, username = %s, password = %s, role = %s
                    WHERE id = %s
                """
                params = (first_name, middle_name, last_name, username, password, role, user_id)
            else:  # If middle name is empty, don't update it
                query = """
                    UPDATE users
                    SET fname = %s, mname = NULL, lname = %s, username = %s, password = %s, role = %s
                    WHERE id = %s
                """
                params = (first_name, last_name, username, password, role, user_id)

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id):
        """Delete user from the database."""
        try:
            query = """
                DELETE FROM users WHERE id = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            print(f"Error deleting user: {e}")
            return False

    def all_users_table(self, parent_frame):
        """Add a table displaying all users in the given parent window, including total user count."""
        print("Adding all users table...")  # Debugging
        for widget in parent_frame.winfo_children():
            widget.destroy()

        all_users_frame = Frame(parent_frame)
        all_users_frame.pack(pady=30, anchor="w")

        # Title Label
        title_label = Label(all_users_frame, text="List of All Users", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=9, pady=10)

        # Total Users Label
        total_users = len(self.all_users_data)  # Get the total user count
        total_users_label = Label(all_users_frame, text=f"Total Users: {total_users}", font=("Arial", 12, "bold"))
        total_users_label.grid(row=1, column=0, columnspan=9, pady=10)

        # Table Headers
        headers = ["ID", "First Name", "Middle Name", "Last Name", "Username", "Role", "View", "Update", "Delete"]
        for idx, header in enumerate(headers):
            Label(all_users_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=2, column=idx)

        # Table Rows
        for i, user in enumerate(self.all_users_data, start=3):
            for j, value in enumerate(user[:5]):
                Label(all_users_frame, text=value, borderwidth=1, relief="solid", width=20).grid(row=i, column=j)

            role = user[5]  # Assuming the role column is part of the fetched data
            Label(all_users_frame, text=role, borderwidth=1, relief="solid", width=20).grid(row=i, column=5)

            # Buttons for View, Update, Delete
            view_button = Button(
                all_users_frame,
                text="View",
                bg="blue",
                fg="white",
                command=lambda u=user: self.view_user_details(u),
            )
            view_button.grid(row=i, column=6)

            update_button = Button(
                all_users_frame,
                text="Update",
                bg="orange",
                fg="white",
                command=lambda u=user: self.update_user_form(u, parent_frame),
            )
            update_button.grid(row=i, column=7)

            delete_button = Button(
                all_users_frame,
                text="Delete",
                bg="red",
                fg="white",
                command=lambda u=user: self.delete_user_confirm(u[0], parent_frame),
            )
            delete_button.grid(row=i, column=8)

        # Add User Button
        add_user_button = Button(
            all_users_frame, text="Add User", bg="green", fg="white", command=lambda: self.add_user_form(parent_frame)
        )
        add_user_button.grid(row=len(self.all_users_data) + 3, column=0, columnspan=9, pady=20)


    def add_user_form(self, parent_window):
        """Open a form to add a new user ."""
        add_user_window = Toplevel(parent_window)  # Use the passed parent_window as the master
        add_user_window.title("Add New User")
        add_user_window.geometry("400x450")

        # Labels and input fields
        labels = ["First Name", "Middle Name", "Last Name", "Username", "Password", "Role"]
        entries = {}

        for idx, label in enumerate(labels[:-1]):  # Exclude Role from labels that need text entry
            Label(add_user_window, text=label).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(add_user_window, show="*" if label == "Password" else None)
            entry.grid(row=idx, column=1, padx=10, pady=10)
            entries[label] = entry

        # Role dropdown (ComboBox)
        # role_label = Label(add_user_window, text="Role")
        # role_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        # role_combobox = ttk.Combobox(add_user_window, values=["Student", "Instructor"])
        # role_combobox.grid(row=5, column=1, padx=10, pady=10)
        # role_combobox.set("Student")  # Default to "Student"
        # entries["Role"] = role_combobox

        # Submit button
        submit_button = Button(add_user_window, text="Submit", bg="blue", fg="white", 
                               command=lambda: self.submit_user(entries, add_user_window))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    def submit_user(self, entries, add_user_window):
        """Submit the form to add the user data ."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()
        role = "Student"

        if not all([first_name, last_name, username, password]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Call the add_user method, passing the role as a parameter
        if self.add_user(first_name, middle_name, last_name, username, password, role):
            messagebox.showinfo("Success", "User added successfully.")
            self.fetch_all_users()
            self.all_users_table(add_user_window.master)
            add_user_window.destroy()  # Close the form window
        else:
            messagebox.showerror("Error", "Failed to add user.")

    def update_user_form(self, user, parent_window):
        """Open a form to update user details ."""
        user_id, first_name, middle_name, last_name, username, role = user

        # Create the update window
        update_window = Toplevel(parent_window)
        update_window.title("Update User Details")
        update_window.geometry("400x450")

        # List of labels and dictionary for storing entry fields
        labels = ["First Name", "Middle Name", "Last Name", "Username", "Password", "Role"]
        entries = {}

        # Create entry fields for first name, middle name, last name, username, and password
        for idx, label in enumerate(labels[:-1]):  # Exclude Role from labels that need text entry
            Label(update_window, text=label).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(update_window, show="*" if label == "Password" else None)
            entry.grid(row=idx, column=1, padx=10, pady=10)

            # Set default values for the entry fields
            if label == "First Name":
                entry.insert(0, first_name)
            elif label == "Middle Name":
                entry.insert(0, middle_name if middle_name else "")  # Handle None for middle name
            elif label == "Last Name":
                entry.insert(0, last_name)
            elif label == "Username":
                entry.insert(0, username)
            
            entries[label] = entry

        # Role dropdown (ComboBox)
        # role_label = Label(update_window, text="Role")
        # role_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        # role_combobox = ttk.Combobox(update_window, values=["Student", "Instructor"])
        # role_combobox.grid(row=5, column=1, padx=10, pady=10)

        # # Set default value for role combobox
        # role_combobox.set(role)  # Pre-set the current role
        # entries["Role"] = role_combobox

        # Submit button
        submit_button = Button(update_window, text="Submit", bg="blue", fg="white", 
                            command=lambda: self.submit_update(user_id, entries, update_window))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)


    def submit_update(self, user_id, entries, update_window):
        """Submit the form to update the user's data."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()  # This can be empty
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()
        role = "Student"

        if not all([first_name, last_name, username, password]):
            messagebox.showerror("Error", "First Name, Last Name, Username, and Password must be filled out.")
            return

        if self.update_user(user_id, first_name, middle_name, last_name, username, password, role):
            messagebox.showinfo("Success", "User updated successfully.")
            self.fetch_all_users()
            self.all_users_table(update_window.master)
            update_window.destroy()  # Close the update form window
        else:
            messagebox.showerror("Error", "Failed to update user.")

    def delete_user_confirm(self, user_id, parent_window):
        """Confirm before deleting the user."""
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if response:
            if self.delete_user(user_id):
                messagebox.showinfo("Success", "User deleted successfully.")
                self.fetch_all_users()
                self.all_users_table(parent_window)
            else:
                messagebox.showerror("Error", "Failed to delete user.")

    def view_user_details(self, user):
        """Show detailed user information and their attendance records."""
        user_id, fname, mname, lname, username, role = user

        # Display user details in a message box (you can modify this as needed)
        user_details = f"ID: {user_id}\nName: {fname} {mname} {lname}\nUsername: {username}\nRole: {role}"
        messagebox.showinfo("User Details", user_details)

        # Fetch attendance records for the selected user
        self.show_user_attendance(user_id, fname, lname)
    
    def show_user_attendance(self, user_id, first_name, last_name):
        """Fetch and display the attendance records for a user."""
        # Create a new window for the attendance records
        attendance_window = Toplevel()
        attendance_window.title(f"Attendance Records for {first_name} {last_name}")

        try:
            # Query to fetch attendance records for the specific user (including reason and approval)
            query = """
                SELECT a_date, a_status, a_reason, a_approval FROM attendance WHERE a_student_id = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (user_id,))
            attendance_records = cursor.fetchall()
            cursor.close()

            # If records are found, display them in a table
            if attendance_records:
                # Create column headers
                Label(attendance_window, text="Date", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, padx=10, pady=10)
                Label(attendance_window, text="Status", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=1, padx=10, pady=10)
                Label(attendance_window, text="Reason", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=30).grid(row=0, column=2, padx=10, pady=10)
                Label(attendance_window, text="Approval", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=3, padx=10, pady=10)

                # Display attendance records in rows
                for i, (date, status, reason, approval) in enumerate(attendance_records, start=1):
                    Label(attendance_window, text=date, font=("Arial", 12), borderwidth=1, relief="solid", width=20).grid(row=i, column=0, padx=10, pady=10)
                    Label(attendance_window, text=status, font=("Arial", 12), borderwidth=1, relief="solid", width=20).grid(row=i, column=1, padx=10, pady=10)
                    Label(attendance_window, text=reason or "N/A", font=("Arial", 12), borderwidth=1, relief="solid", width=30).grid(row=i, column=2, padx=10, pady=10)
                    Label(attendance_window, text=approval or "N/A", font=("Arial", 12), borderwidth=1, relief="solid", width=20).grid(row=i, column=3, padx=10, pady=10)
            else:
                Label(attendance_window, text="No attendance records found.", font=("Arial", 12)).pack(pady=20)

        except Exception as e:
            logging.error(f"Error fetching attendance records: {e}")
            messagebox.showerror("Error", "Failed to fetch attendance records.")