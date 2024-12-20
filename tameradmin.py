import tkinter as tk
from tkinter import ttk, messagebox
from datatamer import initialize_database, add_employee, authenticate_user
import tkinter.font as tkfont
from search import AdminGUI  # Import the AdminGUI class

class HotelManagementSystem:
    def __init__(self, root):  # Fixed initialization method
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")
        
        # Custom colors
        self.primary_blue = "#003580"  
        self.light_blue = "#f2f6fa"
        self.white = "#ffffff"
        self.accent_blue = "#1a4fa0"
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root, style="Main.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create frames
        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()
        
        # Initialize with login frame
        self.current_frame = self.login_frame
        self.show_frame(self.login_frame)

    def configure_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.configure("Main.TFrame", background=self.light_blue)
        style.configure("Card.TFrame", background=self.white)
        
        # Custom button style
        style.configure("Custom.TButton",
                       background=self.primary_blue,
                       foreground=self.white,
                       padding=(20, 10),
                       font=('Arial', 11, 'bold'))
        style.map("Custom.TButton",
                 background=[('active', self.accent_blue)])
        
        # Entry style
        style.configure("Custom.TEntry",
                       fieldbackground=self.white,
                       borderwidth=2,
                       relief="solid")
        
        # Label styles
        style.configure("Title.TLabel",
                       background=self.white,
                       foreground=self.primary_blue,
                       font=('Arial', 24, 'bold'))
        style.configure("Header.TLabel",
                       background=self.white,
                       foreground=self.primary_blue,
                       font=('Arial', 12, 'bold'))
        style.configure("Card.TLabel",
                       background=self.white,
                       font=('Arial', 11))
        
        # Radio button style
        style.configure("Card.TRadiobutton",
                       background=self.white,
                       font=('Arial', 11))

    def create_custom_entry(self, parent):
        entry = tk.Entry(parent, font=('Arial', 11), width=40)
        entry.configure(
            relief="solid",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.primary_blue,
            highlightbackground=self.primary_blue
        )
        return entry

    def create_login_frame(self):
        frame = ttk.Frame(self.main_container, style="Card.TFrame", padding=30)
        
        # Title
        title = ttk.Label(frame, text="Welcome Back", style="Title.TLabel")
        title.pack(pady=(0, 30))
        
        # Username
        ttk.Label(frame, text="Username", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.login_username = self.create_custom_entry(frame)
        self.login_username.pack(pady=(0, 15), ipady=8)
        
        # Password
        ttk.Label(frame, text="Password", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.login_password = self.create_custom_entry(frame)
        self.login_password.configure(show="•")
        self.login_password.pack(pady=(0, 15), ipady=8)
        
        # Role selection
        ttk.Label(frame, text="Role", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.login_role = tk.StringVar(value="Employee")
        role_frame = ttk.Frame(frame, style="Card.TFrame")
        role_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Radiobutton(role_frame, text="Employee", variable=self.login_role,
                       value="Employee", style="Card.TRadiobutton").pack(side="left", padx=10)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.login_role,
                       value="Admin", style="Card.TRadiobutton").pack(side="left")
        
        # Login button
        login_button = tk.Button(frame, text="Login",
                               font=('Arial', 11, 'bold'),
                               bg=self.primary_blue,
                               fg=self.white,
                               padx=20,
                               pady=10,
                               relief="flat",
                               command=self.login_user)
        login_button.pack(pady=20, fill="x")
        
        # Register link
        register_frame = ttk.Frame(frame, style="Card.TFrame")
        register_frame.pack(pady=10)
        ttk.Label(register_frame, text="New user? ", style="Card.TLabel").pack(side="left")
        register_link = ttk.Label(register_frame, 
                                text="Register here",
                                foreground=self.primary_blue,
                                cursor="hand2",
                                style="Card.TLabel")
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.show_frame(self.register_frame))
        
        return frame

    def create_register_frame(self):
        frame = ttk.Frame(self.main_container, style="Card.TFrame", padding=30)
        
        # Title
        title = ttk.Label(frame, text="Create Account", style="Title.TLabel")
        title.pack(pady=(0, 30))
        
        # Username
        ttk.Label(frame, text="Username", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.register_username = self.create_custom_entry(frame)
        self.register_username.pack(pady=(0, 15), ipady=8)
        
        # Password
        ttk.Label(frame, text="Password", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.register_password = self.create_custom_entry(frame)
        self.register_password.configure(show="•")
        self.register_password.pack(pady=(0, 15), ipady=8)
        
        # Role selection
        ttk.Label(frame, text="Role", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.register_role = tk.StringVar(value="Employee")
        role_frame = ttk.Frame(frame, style="Card.TFrame")
        role_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Radiobutton(role_frame, text="Employee", variable=self.register_role,
                       value="Employee", style="Card.TRadiobutton",
                       command=self.toggle_admin_id).pack(side="left", padx=10)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.register_role,
                       value="Admin", style="Card.TRadiobutton",
                       command=self.toggle_admin_id).pack(side="left")
        
        # Admin ID (hidden by default)
        self.admin_id_frame = ttk.Frame(frame, style="Card.TFrame")
        ttk.Label(self.admin_id_frame, text="Admin ID", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.admin_id_entry = self.create_custom_entry(self.admin_id_frame)
        self.admin_id_entry.pack(pady=(0, 15), ipady=8)
        
        # Register button
        register_button = tk.Button(frame, text="Register",
                                  font=('Arial', 11, 'bold'),
                                  bg=self.primary_blue,
                                  fg=self.white,
                                  padx=20,
                                  pady=10,
                                  relief="flat",
                                  command=self.register_user)
        register_button.pack(pady=20, fill="x")
        
        # Login link
        login_frame = ttk.Frame(frame, style="Card.TFrame")
        login_frame.pack(pady=10)
        ttk.Label(login_frame, text="Already have an account? ", style="Card.TLabel").pack(side="left")
        login_link = ttk.Label(login_frame, 
                             text="Login here",
                             foreground=self.primary_blue,
                             cursor="hand2",
                             style="Card.TLabel")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_frame(self.login_frame))
        
        return frame

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def toggle_admin_id(self):
        if self.register_role.get() == "Admin":
            self.admin_id_frame.pack(fill="x", before=self.register_frame.winfo_children()[-2])
        else:
            self.admin_id_frame.pack_forget()

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()
        role = self.login_role.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        user = authenticate_user(username, password, role)
        if user:
            messagebox.showinfo("Success", "Welcome back, {0}!".format(username))  # Replaced f-string
            if role == "Admin":
                # Hide the login window
                self.root.withdraw()
                
                # Create new window for admin interface
                admin_window = tk.Toplevel()
                admin_app = AdminGUI(admin_window)
                
                # When admin window is closed, show login window again
                def on_admin_close():
                    admin_window.destroy()
                    self.root.deiconify()
                
                admin_window.protocol("WM_DELETE_WINDOW", on_admin_close)
            else:
                # Handle employee login (implement your employee interface here)
                pass
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def register_user(self):
        username = self.register_username.get()
        password = self.register_password.get()
        role = self.register_role.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if role == "Admin":
            admin_id = self.admin_id_entry.get()
            if admin_id != "123":
                messagebox.showerror("Error", "Invalid Admin ID!")
                return

        if add_employee(username, password, role):
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_frame(self.login_frame)
        else:
            messagebox.showerror("Error", "Username already exists!")

def main():
    initialize_database()
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":  # Fixed the conditional here
    main()
