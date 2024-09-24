import tkinter as tk
import datetime
import random
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore

# database
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# class for login page gui
class AdminLogin:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x850")
        self.master.title("Admin Login")
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.login_frame, text="Admin Login")
        self.label.grid(row=0, column=0, columnspan=2)

        # gui section for username entry
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=1, column=0, pady=5, sticky='e')
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, pady=5)

        # gui section for password entry
        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=2, column=0, pady=5, sticky='e')
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        # button for login
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.check_credentials)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def check_credentials(self):
        # hardcoded credentials for simplicity (replace with secure handling in real cases)
        admin_username = "admin"
        admin_password = "password"

        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        # if login credentials match, then allow user access to admin panel
        if entered_username == admin_username and entered_password == admin_password:
            messagebox.showinfo("Login Success", "Access Granted")
            self.master.destroy()  # Close the login window

            # run the admin panel gui
            root = tk.Tk()
            app = AdminGUI(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")


# class for admin panel gui
class AdminGUI:
    def __init__(self, master):
        # master controls
        self.master = master
        master.geometry("1000x850")
        master.title("SUN Lab Access System")
        self.label = tk.Label(master, text="Admin Panel", font=("Arial", 16))
        self.label.grid(row=0, column=0, columnspan=3, pady=20)

        # button to fetch and display all access logs
        self.fetch_all_button = tk.Button(master, text="Fetch All Access Logs", command=self.fetch_all_logs, width=20,
                                          height=2)
        self.fetch_all_button.grid(row=0, column=3, padx=10, pady=10)

        # button to simulate entry
        self.simulate_entry_button = tk.Button(master, text="Simulate Entry", command=self.simulate_entry, width=20,
                                               height=2)
        self.simulate_entry_button.grid(row=0, column=4, padx=10, pady=10)

        # access log filtering controls:
        # gui section to filter by date
        self.sort_by_date_var = tk.IntVar()
        self.sort_by_date_checkbox = tk.Checkbutton(master, text="Sort by Earliest Date",
                                                    variable=self.sort_by_date_var)
        self.sort_by_date_checkbox.grid(row=1, column=3, padx=10, pady=5)

        # gui section to filter by time range
        self.filter_time_start_label = tk.Label(master, text="Start Time (HH:MM):")
        self.filter_time_start_label.grid(row=2, column=2, padx=1, pady=1, sticky='e')
        self.filter_time_start_entry = tk.Entry(master, width=10)
        self.filter_time_start_entry.grid(row=2, column=3, padx=1, pady=1)

        self.filter_time_end_label = tk.Label(master, text="End Time (HH:MM):")
        self.filter_time_end_label.grid(row=2, column=3, padx=1, pady=1, sticky='e')
        self.filter_time_end_entry = tk.Entry(master, width=10)
        self.filter_time_end_entry.grid(row=2, column=4, padx=1, pady=1)

        # gui section for filtering by id
        self.filter_id_label = tk.Label(master, text="Filter by User ID:")
        self.filter_id_label.grid(row=3, column=2, padx=2, pady=5, sticky='e')
        self.filter_id_entry = tk.Entry(master, width=30)
        self.filter_id_entry.grid(row=3, column=3, padx=2, pady=5)

        self.filter_button = tk.Button(master, text="Filter Logs", command=self.filter_logs, width=20,
                                       height=2)
        self.filter_button.grid(row=3, column=4, padx=10, pady=5)

        # gui section to display the access logs
        self.logs_label = tk.Label(master, text="Access Logs")
        self.logs_label.grid(row=4, column=3, columnspan=2)
        self.logs_display = tk.Listbox(master, height=10, width=70)
        self.logs_display.grid(row=5, column=3, columnspan=2, pady=20)

        # gui section to display users
        self.users_label = tk.Label(master, text="Users")
        self.users_label.grid(row=6, column=3, columnspan=2)
        self.users_display = tk.Listbox(master, height=10, width=70)
        self.users_display.grid(row=7, column=3, columnspan=2, pady=20)
        self.fetch_all_users()

        # gui section to suspend a user
        self.suspend_id_label = tk.Label(master, text="Enter User ID to Suspend:")
        self.suspend_id_label.grid(row=8, column=2, padx=10, pady=5, sticky='e')
        self.suspend_id_entry = tk.Entry(master, width=30)
        self.suspend_id_entry.grid(row=8, column=3, padx=10, pady=5)
        self.suspend_button = tk.Button(master, text="Suspend User", command=self.suspend_student, width=20, height=2)
        self.suspend_button.grid(row=8, column=4, padx=10, pady=5)

        # gui section to reactivate a user
        self.reactivate_id_label = tk.Label(master, text="Enter User ID to Reactivate:")
        self.reactivate_id_label.grid(row=9, column=2, padx=10, pady=5, sticky='e')
        self.reactivate_id_entry = tk.Entry(master, width=30)
        self.reactivate_id_entry.grid(row=9, column=3, padx=10, pady=5)
        self.reactivate_button = tk.Button(master, text="Reactivate User", command=self.reactivate_user, width=20,
                                           height=2)
        self.reactivate_button.grid(row=9, column=4, padx=10, pady=5)

        # gui section to activate a user
        self.activate_id_label = tk.Label(master, text="Enter User ID to Activate:")
        self.activate_id_label.grid(row=10, column=2, padx=10, pady=5, sticky='e')
        self.activate_id_entry = tk.Entry(master, width=30)
        self.activate_id_entry.grid(row=10, column=3, padx=10, pady=5)
        self.activate_button = tk.Button(master, text="Activate User", command=self.activate_user, width=20, height=2)
        self.activate_button.grid(row=10, column=4, padx=10, pady=5)

    # method to display the access logs to the display
    def fetch_all_logs(self):
        self.logs_display.delete(0, tk.END)
        logs = self.get_all_access_logs()

        if logs:
            for log in logs:
                self.logs_display.insert(tk.END, f"{log}\n")
        else:
            self.logs_display.insert(tk.END, "No Access Logs\n")

    # method to format the access logs
    def get_all_access_logs(self):
        logs_ref = db.collection('access_logs')
        docs = logs_ref.stream()

        logs = []
        for doc in docs:
            log_data = doc.to_dict()
            log_entry = f"userID: {log_data['userID']}, Timestamp: {log_data['timestamp'].isoformat()}\n"
            logs.append(log_entry)

        return logs

    # method to display the user list to the display box
    def fetch_all_users(self):
        self.users_display.delete(0, tk.END)
        users = self.get_user_list()

        if users:
            for user in users:
                self.users_display.insert(tk.END, f"{user}\n")
        else:
            self.users_display.insert(tk.END, "No Users Found\n")

    # method to format the users list
    def get_user_list(self):
        users_ref = db.collection('users')
        docs = users_ref.stream()
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            user_entry = f"ID: {doc.id}, Name: {user_data['name']}, status: {user_data['status']}, type: {user_data['type']}\n"
            users.append(user_entry)

        return users

    # method to get user id's from the users collection and store in a list
    def get_user_ids(self):
        users_ref = db.collection('users')
        docs = users_ref.stream()
        user_ids = [doc.id for doc in docs]
        return user_ids

    # method to check the status of a user
    def check_user_status(self, user_id):
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            status = user_data.get('status', 'No status')
            return status
        else:
            return "User Not Found"

    # method to simulate an entry into the sun lab since i do not have a card reader
    def simulate_entry(self):
        # get the user ids
        user_ids = self.get_user_ids()
        if not user_ids:
            messagebox.showwarning("Error", "No student ID's found")
            return

        # picking a random user to simulate
        random_user = random.choice(user_ids)
        user_status = self.check_user_status(random_user)

        # check user status before allowing access
        if user_status == "suspended":
            messagebox.showwarning("Error", "User is suspended")
            return

        # add new data to the db
        entry_data = {
            "userID": random_user,
            "timestamp": datetime.datetime.now(),
            "entry_type": "in"
        }
        db.collection('access_logs').add(entry_data)

        self.fetch_all_logs()  # show updated logs

    # method to change the user status to suspended
    def suspend_student(self):
        user_id = self.suspend_id_entry.get().strip()  # Get input from the text entry
        if user_id:
            try:
                student_ref = db.collection('users').document(user_id)
                user_status = self.check_user_status(user_id)
                # check user status
                if user_status == "suspended":
                    messagebox.showwarning("Error", "User is already suspended")
                    return
                else:
                    student_ref.update({'status': 'suspended'})
                    messagebox.showinfo("Success", f"Student ID {user_id} suspended successfully.")
                    self.fetch_all_users()  # update users list
            except Exception as e:
                messagebox.showerror("Error", f"Could not suspend student: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid student ID.")

    # method to reactivate a user if their status is suspended
    def reactivate_user(self):
        user_id = self.reactivate_id_entry.get().strip()
        if user_id:
            try:
                student_ref = db.collection('users').document(user_id)
                user_status = self.check_user_status(user_id)
                # check status of user
                if user_status == "active":
                    messagebox.showwarning("Error", "User is already active")
                    return
                else:
                    student_ref.update({'status': 'active'})
                    messagebox.showinfo("Success", f"User ID {user_id} reactivated successfully.")
                    self.fetch_all_users()  # update users list
            except Exception as e:
                messagebox.showerror("Error", f"Could not reactivate user: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid user ID.")

    # method to activate a user by ID
    def activate_user(self):
        user_id = self.activate_id_entry.get().strip()
        if user_id:
            try:
                student_ref = db.collection('users').document(user_id)
                user_status = self.check_user_status(user_id)
                # check status of user
                if user_status == "active":
                    messagebox.showwarning("Error", "User is already active")
                    return
                else:
                    student_ref.update({'status': 'active'})
                    messagebox.showinfo("Success", f"User ID {user_id} activated successfully.")
                    self.fetch_all_users()  # update users list to show new status
            except Exception as e:
                messagebox.showerror("Error", f"Could not activate user: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid user ID.")

    # method to filter the access log display based on the inputs
    def filter_logs(self):
        self.logs_display.delete(0, tk.END)

        # get filter values from entry fields
        user_id = self.filter_id_entry.get().strip()
        time_start_filter = self.filter_time_start_entry.get().strip()
        time_end_filter = self.filter_time_end_entry.get().strip()
        sort_by_date = self.sort_by_date_var.get()

        try:
            logs_ref = db.collection('access_logs')

            # filter by id
            if user_id:
                logs_ref = logs_ref.where('userID', '==', user_id)

            # filter by date
            if sort_by_date:
                logs_ref = logs_ref.order_by('timestamp', direction='ASCENDING')
            else:
                logs_ref = logs_ref.order_by('timestamp', direction='DESCENDING')

            logs = logs_ref.get()
            filtered_logs = []

            # filter access logs by time range if provided
            if time_start_filter and time_end_filter:
                time_start = datetime.datetime.strptime(time_start_filter, '%H:%M').time()
                time_end = datetime.datetime.strptime(time_end_filter, '%H:%M').time()

                for log in logs:
                    log_data = log.to_dict()
                    log_time = log_data['timestamp'].time()
                    if time_start <= log_time <= time_end:
                        filtered_logs.append(log_data)
            else:
                filtered_logs = [log.to_dict() for log in logs]

            if filtered_logs:
                for log_data in filtered_logs:
                    self.logs_display.insert(tk.END, f"ID: {log_data['userID']}, Time: {log_data['timestamp']}")
            else:
                messagebox.showinfo("No Records", "No access logs found for the given criteria.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch access logs: {e}")


# run the login page first
root = tk.Tk()
my_gui = AdminLogin(root)
root.mainloop()
