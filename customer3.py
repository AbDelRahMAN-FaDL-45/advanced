import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("900x600")
        self.root.configure(bg='lightblue')

        self.selected_customer_id = None

        # Variables
        self.First_Name = StringVar()
        self.Last_Name = StringVar()
        self.Customer_id = StringVar()  # Added Customer_id variable
        self.phone = StringVar()
        self.email = StringVar()
        self.Room_Price = StringVar()
        self.Total_Booking_Price = StringVar()
        self.Room_Type = StringVar()
        self.check_in_date = StringVar()
        self.check_out_date = StringVar()

        # Database Initialization
        self.initialize_database()

        # UI Components
        self.create_widgets()

    def initialize_database(self):
        with sqlite3.connect("hotel_management_system.db") as conn:
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
        # Input Form
        Label(self.root, text="First Name:", bg='lightblue').grid(row=0, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.First_Name).grid(row=0, column=1, padx=10, pady=5)

        Label(self.root, text="Last Name:", bg='lightblue').grid(row=1, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.Last_Name).grid(row=1, column=1, padx=10, pady=5)

        Label(self.root, text="Customer ID:", bg='lightblue').grid(row=2, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.Customer_id, state='readonly').grid(row=2, column=1, padx=10, pady=5)

        Label(self.root, text="Phone:", bg='lightblue').grid(row=3, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.phone).grid(row=3, column=1, padx=10, pady=5)

        Label(self.root, text="Email:", bg='lightblue').grid(row=4, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.email).grid(row=4, column=1, padx=10, pady=5)

        Label(self.root, text="Room Price:", bg='lightblue').grid(row=5, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.Room_Price).grid(row=5, column=1, padx=10, pady=5)

        Label(self.root, text="Total Booking Price:", bg='lightblue').grid(row=6, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.Total_Booking_Price).grid(row=6, column=1, padx=10, pady=5)

        Label(self.root, text="Room Type:", bg='lightblue').grid(row=7, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.Room_Type).grid(row=7, column=1, padx=10, pady=5)

        Label(self.root, text="Check-in Date:", bg='lightblue').grid(row=8, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.check_in_date).grid(row=8, column=1, padx=10, pady=5)

        Label(self.root, text="Check-out Date:", bg='lightblue').grid(row=9, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.check_out_date).grid(row=9, column=1, padx=10, pady=5)

        # Buttons
        Button(self.root, text="Add Customer", command=self.add_customer, bg='green').grid(row=10, column=0, padx=10, pady=5)
        Button(self.root, text="Edit Customer", command=self.edit_customer, bg='orange').grid(row=10, column=1, padx=10, pady=5)
        Button(self.root, text="Update Customer", command=self.update_customer, bg='blue').grid(row=10, column=2, padx=10, pady=5)
        Button(self.root, text="Clear Fields", command=self.clear_fields, bg='gray').grid(row=10, column=3, padx=10, pady=5)

        # Customer Table
        self.customer_table = ttk.Treeview(
            self.root,
            columns=("First_Name", "Last_Name", "Customer_id", "phone", "email", "Room_Price", "Total_Booking_Price", "Room_Type", "check_in_date", "check_out_date"),
            show="headings"
        )
        self.customer_table.grid(row=11, column=0, columnspan=4, padx=10, pady=10)

        # Table Column Configurations
        for col in self.customer_table["columns"]:
            self.customer_table.heading(col, text=col)
            self.customer_table.column(col, width=100)

        # Event Binding
        self.customer_table.bind("<ButtonRelease-1>", self.select_customer)

        # Load Data
        self.fetch_data()

    def fetch_data(self):
        with sqlite3.connect("hotel_management_system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()

            # Clear existing table data
            for row in self.customer_table.get_children():
                self.customer_table.delete(row)

            # Insert fetched data into table
            for row in rows:
                self.customer_table.insert("", "end", values=row)

    def add_customer(self):
        if not self.First_Name.get() or not self.Last_Name.get():
            messagebox.showerror("Error", "First Name and Last Name are required!")
            return

        with sqlite3.connect("hotel_management_system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.First_Name.get(),
                self.Last_Name.get(),
                self.phone.get(),
                self.email.get(),
                self.Room_Price.get(),
                self.Total_Booking_Price.get(),
                self.Room_Type.get(),
                self.check_in_date.get(),
                self.check_out_date.get()
            ))
            conn.commit()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Customer added successfully!")

    def select_customer(self, event):
        selected_row = self.customer_table.focus()
        data = self.customer_table.item(selected_row)["values"]
        if data:
            self.First_Name.set(data[0])
            self.Last_Name.set(data[1])
            self.Customer_id.set(data[2])  # Customer_id is now at index 2
            self.phone.set(data[3])
            self.email.set(data[4])
            self.Room_Price.set(data[5])
            self.Total_Booking_Price.set(data[6])
            self.Room_Type.set(data[7])
            self.check_in_date.set(data[8])
            self.check_out_date.set(data[9])
            self.selected_customer_id = data[2]  # Update selected_customer_id

    def update_customer(self):
        if not self.selected_customer_id:
            messagebox.showerror("Error", "No customer selected to update!")
            return

        with sqlite3.connect("hotel_management_system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET First_Name=?, Last_Name=?, phone=?, email=?, Room_Price=?, Total_Booking_Price=?, Room_Type=?, check_in_date=?, check_out_date=?
                WHERE Customer_id=?
            """, (
                self.First_Name.get(),
                self.Last_Name.get(),
                self.phone.get(),
                self.email.get(),
                self.Room_Price.get(),
                self.Total_Booking_Price.get(),
                self.Room_Type.get(),
                self.check_in_date.get(),
                self.check_out_date.get(),
                self.selected_customer_id
            ))
            conn.commit()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Customer updated successfully!")

    def edit_customer(self):
        if not self.selected_customer_id:
            messagebox.showerror("Error", "No customer selected to edit!")
            return

    def clear_fields(self):
        self.First_Name.set("")
        self.Last_Name.set("")
        self.Customer_id.set("")  # Clear Customer_id
        self.phone.set("")
        self.email.set("")
        self.Room_Price.set("")
        self.Total_Booking_Price.set("")
        self.Room_Type.set("")
        self.check_in_date.set("")
        self.check_out_date.set("")
        self.selected_customer_id = None


if __name__ == "__main__":
    root = Tk()
    app = CustomerApp(root)
    root.mainloop()