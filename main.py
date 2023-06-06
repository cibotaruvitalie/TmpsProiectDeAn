from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel
import re
import json
import subprocess

# Solid: Create a user class
class User:
    def __init__(self, name, contact, address, username, password):
        self.name = name
        self.contact = contact
        self.address = address
        self.username = username
        self.password = password

    def __str__(self):
        return f"Name: {self.name}\nContact: {self.contact}\nAddress: {self.address}\nUsername: {self.username}\nPassword: {self.password}"

    def to_dict(self):
        return {
            "name": self.name,
            "contact": self.contact,
            "address": self.address,
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, user_data):
        return cls(
            user_data["name"],
            user_data["contact"],
            user_data["address"],
            user_data["username"],
            user_data["password"]
        )

# Solid: Create a user builder class
class UserBuilder:
    def __init__(self):
        self.name = ""
        self.contact = ""
        self.address = ""
        self.username = ""
        self.password = ""

    def set_name(self, name):
        self.name = name
        return self

    def set_contact(self, contact):
        self.contact = contact
        return self

    def set_address(self, address):
        self.address = address
        return self

    def set_username(self, username):
        self.username = username
        return self

    def set_password(self, password):
        self.password = password
        return self

    def build(self):
        return User(self.name, self.contact, self.address, self.username, self.password)

# Solid: Create a user data manager class
class UserDataManager:
    FILE_NAME = "users.json"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def save_users_to_file(self):
        user_data = [user.to_dict() for user in self.users]
        with open(UserDataManager.FILE_NAME, "w") as file:
            json.dump(user_data, file, indent=4)

    def load_users_from_file(self):
        try:
            with open(UserDataManager.FILE_NAME, "r") as file:
                user_data = json.load(file)
                self.users = [User.from_dict(data) for data in user_data]
        except FileNotFoundError:
            self.users = []

# Chain of Responsibility: Create handler classes for authentication
class AuthHandler:
    def set_next_handler(self, handler):
        self.next_handler = handler

    def handle_request(self, username, password):
        pass

class UserAuthHandler(AuthHandler):
    def handle_request(self, username, password):
        user_data_manager = UserDataManager.get_instance()
        for user in user_data_manager.users:
            if user.username == username and user.password == password:
                return True
        if self.next_handler:
            return self.next_handler.handle_request(username, password)
        return False

class ManagerAuthHandler(AuthHandler):
    def handle_request(self, username, password):
        if username == "manager" and password == "pass":
            return True
        if self.next_handler:
            return self.next_handler.handle_request(username, password)
        return False

# Solid: Create a command class for registration
class RegisterCommand:
    def __init__(self, builder):
        self.builder = builder

    def execute(self):
        user_data_manager = UserDataManager.get_instance()
        user = self.builder.build()
        user_data_manager.add_user(user)
        user_data_manager.save_users_to_file()
        messagebox.showinfo("Registration", "Registration Successful")

# Solid: Create a GUI class for user authentication
class UserAuthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication")
        self.root.geometry("300x200")

        self.username_label = Label(self.root, text="Username")
        self.username_label.pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        self.password_label = Label(self.root, text="Password")
        self.password_label.pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = Button(self.root, text="Register", command=self.open_register_window)
        self.register_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_auth_handler = UserAuthHandler()
        manager_auth_handler = ManagerAuthHandler()
        user_auth_handler.set_next_handler(manager_auth_handler)

        if user_auth_handler.handle_request(username, password):
            # Open another Python file (replace 'path/to/your_file.py' with the actual file path)
            subprocess.Popen(["python", "food_delivery.py"])
            self.root.destroy()  # Close the login window
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def open_register_window(self):
        register_window = Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("300x300")

        self.register_username_label = Label(register_window, text="Username")
        self.register_username_label.pack()
        self.register_username_entry = Entry(register_window)
        self.register_username_entry.pack()

        self.register_password_label = Label(register_window, text="Password")
        self.register_password_label.pack()
        self.register_password_entry = Entry(register_window, show="*")
        self.register_password_entry.pack()

        self.register_name_label = Label(register_window, text="Name")
        self.register_name_label.pack()
        self.register_name_entry = Entry(register_window)
        self.register_name_entry.pack()

        self.register_contact_label = Label(register_window, text="Contact")
        self.register_contact_label.pack()
        self.register_contact_entry = Entry(register_window)
        self.register_contact_entry.pack()

        self.register_address_label = Label(register_window, text="Address")
        self.register_address_label.pack()
        self.register_address_entry = Entry(register_window)
        self.register_address_entry.pack()

        self.register_button = Button(register_window, text="Register", command=self.register)
        self.register_button.pack()

    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        name = self.register_name_entry.get()
        contact = self.register_contact_entry.get()
        address = self.register_address_entry.get()

        if not re.match("^[a-zA-Z0-9]*$", username):
            messagebox.showerror("Registration", "Invalid Username")
            return
        if len(password) < 6:
            messagebox.showerror("Registration", "Password should be at least 6 characters long")
            return

        builder = UserBuilder()
        builder.set_username(username)
        builder.set_password(password)
        builder.set_name(name)
        builder.set_contact(contact)
        builder.set_address(address)

        register_command = RegisterCommand(builder)
        register_command.execute()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

# Solid: Load user data from file on startup
user_data_manager = UserDataManager.get_instance()
user_data_manager.load_users_from_file()

# Solid: Create the main application window
root = Tk()
app = UserAuthGUI(root)
root.mainloop()