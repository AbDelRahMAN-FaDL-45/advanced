import sqlite3
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
from tkinter import ttk

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Interface - Customer Search")
        self.root.geometry("800x600")
        
        # Custom colors
        self.primary_blue = "#003580"  
        self.light_blue = "#f2f6fa"
        self.white = "#ffffff"
        self.accent_blue = "#1a4fa0"

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        """Configure the styles for the widgets."""
        self.style = ttk.Style()
        self.style.configure("Main.TFrame", background=self.light_blue)
        self.style.configure("Card.TFrame", background=self.white)
        
        # Custom button style (consistent button colors)
        self.style.configure("Custom.TButton",
                             background=self.primary_blue,
                             foreground=self.white,
                             padding=(20, 10),
                             font=('Arial', 11, 'bold'))
        self.style.map("Custom.TButton",
                       background=[('active', self.accent_blue)])

        # Entry style
        self.style.configure("Custom.TEntry",
                             fieldbackground=self.white,
                             borderwidth=2,
                             relief="solid")

        # Label styles
        self.style.configure("Header.TLabel",
                             background=self.white,
                             foreground=self.primary_blue,
                             font=('Arial', 12, 'bold'))
        self.style.configure("Card.TLabel",
                             background=self.white,
                             font=('Arial', 11))

    def create_widgets(self):
        """Create the GUI components."""
        # Search Frame
        search_frame = Frame(self.root, bg=self.light_blue, bd=2, relief="solid")
        search_frame.place(x=20, y=20, width=760, height=150)

        Label(search_frame, text="Search Customer", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 16, "bold")).pack(pady=10)

        # Customer ID Entry
        self.search_id = StringVar()
        id_label = Label(search_frame, text="Customer ID:", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12, "bold"))
        id_label.pack(side=LEFT, padx=10)

        id_entry = Entry(search_frame, textvariable=self.search_id, font=("Arial", 12), bg=self.white, fg=self.primary_blue, bd=2, relief="solid")
        id_entry.pack(side=LEFT, fill=X, padx=10, expand=True)

        # Buttons: Search, Clear, Delete
        button_frame = Frame(search_frame, bg=self.light_blue)
        button_frame.pack(pady=20)

        search_button = Button(button_frame, text="Search", command=self.search_customer, font=("Arial", 12), bg=self.primary_blue, fg='white', relief="flat", width=12, height=2)
        search_button.pack(side=LEFT, padx=10)

        clear_button = Button(button_frame, text="Clear", command=self.clear_results, font=("Arial", 12), bg=self.primary_blue, fg='white', relief="flat", width=12, height=2)
        clear_button.pack(side=LEFT, padx=10)

        delete_button = Button(button_frame, text="Delete", command=self.delete_customer, font=("Arial", 12), bg=self.primary_blue, fg='white', relief="flat", width=12, height=2)
        delete_button.pack(side=LEFT, padx=10)

        # Result Frame - Split into two sections (Left and Right)
        result_frame = Frame(self.root, bg=self.light_blue)
        result_frame.place(x=20, y=200, width=760, height=350)

        left_frame = Frame(result_frame, bg=self.light_blue, width=380, height=350)
        left_frame.pack(side=LEFT, fill=Y, padx=10)

        right_frame = Frame(result_frame, bg=self.light_blue, width=380, height=350)
        right_frame.pack(side=RIGHT, fill=Y, padx=10)

        # Labels for the left section (titles)
        self.result_labels_left = {
            "Customer_Name": Label(left_frame, text="Customer Name: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Customer_ID": Label(left_frame, text="Customer ID: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Phone": Label(left_frame, text="Phone: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Email": Label(left_frame, text="Email: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
        }

        # Labels for the right section (data)
        self.result_labels_right = {
            "Check_In": Label(right_frame, text="Check-in Date: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Check_Out": Label(right_frame, text="Check-out Date: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Room_Type": Label(right_frame, text="Room Type: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Room_Price": Label(right_frame, text="Room Price: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
            "Total_Price": Label(right_frame, text="Total Booking Price: ", bg=self.light_blue, fg=self.primary_blue, font=("Arial", 12)),
        }

        # Place the left section labels
        y_offset = 20
        for key, label in self.result_labels_left.items():
            label.place(x=20, y=y_offset)
            y_offset += 40

        # Place the right section labels
        y_offset = 20
        for key, label in self.result_labels_right.items():
            label.place(x=20, y=y_offset)
            y_offset += 40

    def search_customer(self):
        """Search for a customer by ID and display their details."""
        customer_id = self.search_id.get()
        if not customer_id:
            messagebox.showerror("Error", "Please enter a Customer ID.")
            return

        try:
            # Open the database connection
            db = sqlite3.connect("Hotel management system.db")
            cursor = db.cursor()

            # Query customer information
            cursor.execute(""" 
                SELECT First_Name, Last_Name, Customer_id, phone, email, 
                       check_in_date, check_out_date, Room_Type, Room_Price, 
                       Total_Booking_Price
                FROM customers 
                WHERE Customer_id = ?
            """, (customer_id,))
            
            customer = cursor.fetchone()

            if not customer:
                messagebox.showinfo("Not Found", "No customer found with ID: {}".format(customer_id))
                self.clear_results()
                return

            # Display customer details with correct indices
            self.result_labels_left["Customer_Name"].config(text="Customer Name: {} {}".format(customer[0], customer[1]))
            self.result_labels_left["Customer_ID"].config(text="Customer ID: {}".format(customer[2]))
            self.result_labels_left["Phone"].config(text="Phone: {}".format(customer[3]))
            self.result_labels_left["Email"].config(text="Email: {}".format(customer[4]))

            self.result_labels_right["Check_In"].config(text="Check-in Date: {}".format(customer[5]))
            self.result_labels_right["Check_Out"].config(text="Check-out Date: {}".format(customer[6]))
            self.result_labels_right["Room_Type"].config(text="Room Type: {}".format(customer[7]))
            self.result_labels_right["Room_Price"].config(text="Room Price: ${}".format(customer[8]))
            self.result_labels_right["Total_Price"].config(text="Total Booking Price: ${}".format(customer[9]))

            db.close()  # Close the database connection

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", "Error fetching data: {}".format(str(e)))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred: {}".format(str(e)))

    def delete_customer(self):
        """Delete a customer from the database by ID."""
        customer_id = self.search_id.get()
        if not customer_id:
            messagebox.showerror("Error", "Please enter a Customer ID.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete customer with ID: {}".format(customer_id))
        if confirm:
            try:
                # Open the database connection
                db = sqlite3.connect("Hotel management system.db")
                cursor = db.cursor()

                # Delete the customer from the database
                cursor.execute(""" 
                    DELETE FROM customers 
                    WHERE Customer_id = ?
                """, (customer_id,))

                db.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Deleted", "Customer with ID {} has been deleted.".format(customer_id))
                    self.clear_results()
                else:
                    messagebox.showinfo("Not Found", "No customer found with ID: {}".format(customer_id))

                db.close()  # Close the database connection

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", "Error deleting data: {}".format(str(e)))
            except Exception as e:
                messagebox.showerror("Error", "An error occurred: {}".format(str(e)))

    def clear_results(self):
        """Clear search results."""
        for label in self.result_labels_left.values():
            label.config(text="{}:".format(label.cget('text').split(': ')[0]))
        for label in self.result_labels_right.values():
            label.config(text="{}:".format(label.cget('text').split(': ')[0]))
        self.search_id.set("")

if __name__ == "__main__":
    root = Tk()
    app = AdminGUI(root)
    root.mainloop()
