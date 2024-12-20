import sqlite3
from tkinter import *
from tkinter import messagebox

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Interface - Customer Search")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')

        self.create_widgets()

    def create_widgets(self):
        """Create GUI components."""
        search_frame = LabelFrame(self.root, text="Search Customer", bg='#f0f8ff', fg='black', font=("Arial", 14))
        search_frame.place(x=20, y=20, width=840, height=150)

        Label(search_frame, text="Customer ID:", bg='#f0f8ff', fg='black', font=("Arial", 12)).place(x=20, y=30)
        self.search_id = StringVar()
        Entry(search_frame, textvariable=self.search_id, font=("Arial", 12), bg='white', fg='black').place(x=150, y=30, width=200)

        Button(search_frame, text="Search", command=self.search_customer, font=("Arial", 12), bg='#4CAF50', fg='white').place(x=400, y=30, width=100, height=30)
        Button(search_frame, text="Clear", command=self.clear_results, font=("Arial", 12), bg='#F44336', fg='white').place(x=520, y=30, width=100, height=30)
        Button(search_frame, text="Delete", command=self.delete_customer, font=("Arial", 12), bg='#FF5722', fg='white').place(x=640, y=30, width=100, height=30)

        result_frame = LabelFrame(self.root, text="Customer Details", bg='#f0f8ff', fg='black', font=("Arial", 14))
        result_frame.place(x=20, y=200, width=840, height=450)

        self.result_labels = {
            "Customer_Name": Label(result_frame, text="Customer Name: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Customer_ID": Label(result_frame, text="Customer ID: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Phone": Label(result_frame, text="Phone: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Email": Label(result_frame, text="Email: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Check_In": Label(result_frame, text="Check-in Date: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Check_Out": Label(result_frame, text="Check-out Date: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Room_Type": Label(result_frame, text="Room Type: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Room_Price": Label(result_frame, text="Room Price: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
            "Total_Price": Label(result_frame, text="Total Booking Price: ", bg='#f0f8ff', fg='black', font=("Arial", 12)),
        }

        y_offset = 20
        for key, label in self.result_labels.items():
            label.place(x=20, y=y_offset)
            y_offset += 40

    def search_customer(self):
        """Search for a customer by ID and display their details."""
        customer_id = self.search_id.get()
        if not customer_id:
            messagebox.showerror("Error", "Please enter a Customer ID.")
            return

        try:
            # Open the database connection (for Python 3.4 compatibility)
            db = sqlite3.connect("Hotel management system.db")
            cursor = db.cursor()

            # Query customer information using the correct column name (Customer_id)
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
            self.result_labels["Customer_Name"].config(text="Customer Name: {} {}".format(customer[0], customer[1]))
            self.result_labels["Customer_ID"].config(text="Customer ID: {}".format(customer[2]))
            self.result_labels["Phone"].config(text="Phone: {}".format(customer[3]))
            self.result_labels["Email"].config(text="Email: {}".format(customer[4]))
            self.result_labels["Check_In"].config(text="Check-in Date: {}".format(customer[5]))
            self.result_labels["Check_Out"].config(text="Check-out Date: {}".format(customer[6]))
            self.result_labels["Room_Type"].config(text="Room Type: {}".format(customer[7]))
            self.result_labels["Room_Price"].config(text="Room Price: ${}".format(customer[8]))
            self.result_labels["Total_Price"].config(text="Total Booking Price: ${}".format(customer[9]))

            db.close()  # Close the database connection manually

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
                # Open the database connection (for Python 3.4 compatibility)
                db = sqlite3.connect("hotel_management_system.db")
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

                db.close()  # Close the database connection manually

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", "Error deleting data: {}".format(str(e)))
            except Exception as e:
                messagebox.showerror("Error", "An error occurred: {}".format(str(e)))

    def clear_results(self):
        """Clear search results."""
        for label in self.result_labels.values():
            label.config(text="{}:".format(label.cget('text').split(': ')[0]))
        self.search_id.set("")

if __name__ == "__main__":
    root = Tk()
    app = AdminGUI(root)
    root.mainloop()
