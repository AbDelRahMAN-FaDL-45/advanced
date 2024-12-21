from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1200x800")
        
        # Configure modern color scheme
        self.bg_color = "#f0f8ff"  # Light blue background
        self.accent_color = "#4a90e2"  # Modern blue
        self.button_bg = "#2c3e50"  # Dark blue-gray
        self.button_fg = "white"
        
        self.root.configure(bg=self.bg_color)
        
        # Apply modern style to ttk elements
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="#ffffff")
        style.configure("Treeview.Heading",
                       background=self.button_bg,
                       foreground="white",
                       relief="flat")
        style.map("Treeview.Heading",
                 background=[('active', self.accent_color)])

        self.selected_customer_id = None

        # Variables
        self.First_Name = StringVar()
        self.Last_Name = StringVar()
        self.Customer_id = StringVar()
        self.phone = StringVar()
        self.email = StringVar()
        self.Room_Price = StringVar()
        self.Total_Booking_Price = StringVar()
        self.Room_Type = StringVar()
        self.check_in_date = StringVar()
        self.check_out_date = StringVar()

        # Initialize database and create UI
        self.initialize_database()
        self.create_widgets()

    def initialize_database(self):
        with sqlite3.connect("Hotel management system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers(
                    First_Name text,
                    Last_Name text,
                    Customer_id integer primary key autoincrement,
                    phone text,
                    email text,
                    Room_Price real,
                    Total_Booking_Price real,
                    Room_Type text,
                    check_in_date date,
                    check_out_date date
                )
            """)
            conn.commit()

    def create_widgets(self):
        # Create main frames
        input_frame = Frame(self.root, bg=self.bg_color, pady=20)
        input_frame.pack(fill=X, padx=20)
        
        button_frame = Frame(self.root, bg=self.bg_color, pady=20)
        button_frame.pack(fill=X, padx=20)
        
        table_frame = Frame(self.root, bg=self.bg_color)
        table_frame.pack(fill=BOTH, expand=True, padx=20)

        # Input fields with modern styling
        entries = [
            ("First Name:", self.First_Name),
            ("Last Name:", self.Last_Name),
            ("Phone:", self.phone),
            ("Email:", self.email),
            ("Room Price:", self.Room_Price),
            ("Total Booking Price:", self.Total_Booking_Price),
            ("Room Type:", self.Room_Type),
            ("Check-in Date:", self.check_in_date),
            ("Check-out Date:", self.check_out_date)
        ]

        for i, (text, var) in enumerate(entries):
            Label(input_frame, text=text, bg=self.bg_color, font=('Helvetica', 10, 'bold')).grid(row=i//3, column=(i%3)*2, padx=10, pady=5, sticky='e')
            Entry(input_frame, textvariable=var, font=('Helvetica', 10), width=20).grid(row=i//3, column=(i%3)*2+1, padx=10, pady=5, sticky='w')

        #  style buttons
        buttons = [
            ("Add Customer", self.add_customer),
            ("Update Customer", self.update_customer),
            ("Clear Fields", self.clear_fields)
        ]

        for i, (text, command) in enumerate(buttons):
            Button(button_frame, 
                   text=text,
                   command=command,
                   bg=self.button_bg,
                   fg=self.button_fg,
                   font=('Helvetica', 10, 'bold'),
                   width=15,
                   relief='flat',
                   padx=20,
                   pady=10).pack(side=LEFT, padx=10)

        # Customer Table
        self.customer_table = ttk.Treeview(
            table_frame,
            columns=("First_Name", "Last_Name", "Customer_id", "phone", "email", 
                    "Room_Price", "Total_Booking_Price", "Room_Type", "check_in_date", "check_out_date"),
            show="headings"
        )
        self.customer_table.pack(fill=BOTH, expand=True)

        # Configure columns
        for col in self.customer_table["columns"]:
            self.customer_table.heading(col, text=col.replace("_", " ").title())
            self.customer_table.column(col, width=100)

        # Add scrollbars
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.customer_table.xview)
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.customer_table.yview)
        self.customer_table.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        x_scrollbar.pack(side='bottom', fill='x')
        y_scrollbar.pack(side='right', fill='y')

        # Event Binding
        self.customer_table.bind("<ButtonRelease-1>", self.select_customer)

        # Load initial data
        self.fetch_data()

    # [Rest of the methods remain the same as in your original code]
    def add_customer(self):
        if not self.First_Name.get() or not self.Last_Name.get():
            messagebox.showerror("Error", "First Name and Last Name are required!")
            return

        with sqlite3.connect("Hotel management system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (First_Name, Last_Name, phone, email, Room_Price, 
                                    Total_Booking_Price, Room_Type, check_in_date, check_out_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.First_Name.get(), self.Last_Name.get(), self.phone.get(),
                self.email.get(), self.Room_Price.get(), self.Total_Booking_Price.get(),
                self.Room_Type.get(), self.check_in_date.get(), self.check_out_date.get()
            ))
            conn.commit()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Customer added successfully!")

    def update_customer(self):
        if not self.selected_customer_id:
            messagebox.showerror("Error", "No customer selected to update!")
            return

        with sqlite3.connect("Hotel management system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET First_Name=?, Last_Name=?, phone=?, email=?, Room_Price=?, 
                    Total_Booking_Price=?, Room_Type=?, check_in_date=?, check_out_date=?
                WHERE Customer_id=?
            """, (
                self.First_Name.get(), self.Last_Name.get(), self.phone.get(),
                self.email.get(), self.Room_Price.get(), self.Total_Booking_Price.get(),
                self.Room_Type.get(), self.check_in_date.get(), self.check_out_date.get(),
                self.selected_customer_id
            ))
            conn.commit()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Customer updated successfully!")

    def clear_fields(self):
        for var in [self.First_Name, self.Last_Name, self.Customer_id, self.phone,
                   self.email, self.Room_Price, self.Total_Booking_Price,
                   self.Room_Type, self.check_in_date, self.check_out_date]:
            var.set("")
        self.selected_customer_id = None

    def fetch_data(self):
        with sqlite3.connect("Hotel management system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()

            self.customer_table.delete(*self.customer_table.get_children())
            for row in rows:
                self.customer_table.insert("", "end", values=row)

    def select_customer(self, event):
        selected_row = self.customer_table.focus()
        data = self.customer_table.item(selected_row)["values"]
        if data:
            self.First_Name.set(data[0])
            self.Last_Name.set(data[1])
            self.Customer_id.set(data[2])
            self.phone.set(data[3])
            self.email.set(data[4])
            self.Room_Price.set(data[5])
            self.Total_Booking_Price.set(data[6])
            self.Room_Type.set(data[7])
            self.check_in_date.set(data[8])
            self.check_out_date.set(data[9])
            self.selected_customer_id = data[2]

# Create and run the application
if __name__ == "__main__":
    root = Tk()
    app = CustomerApp(root)
    root.mainloop()