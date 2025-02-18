# Import necessary modules
from tkinter import *
import sqlite3
import tkinter.messagebox
import os

# Dynamically resolve the database path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
database_path = os.path.join(project_root, "database", "store.db")

# Ensure that the database directory exists
if not os.path.exists(os.path.dirname(database_path)):
    os.makedirs(os.path.dirname(database_path))

# Connect to the database
try:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    print("Database connected successfully!")
except sqlite3.OperationalError as e:
    print(f"Database connection failed: {e}")
    exit(1)

# Ensure the inventory table exists
try:
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        stock INTEGER NOT NULL,
        cp REAL NOT NULL,
        sp REAL NOT NULL,
        totalcp REAL NOT NULL,
        totalsp REAL NOT NULL,
        assumed_profit REAL NOT NULL,
        vendor TEXT NOT NULL,
        vendor_phoneno TEXT NOT NULL
    )
    """)
    conn.commit()
except sqlite3.Error as e:
    print(f"Database schema creation failed: {e}")
    exit(1)

# Fetch the current maximum ID
try:
    result = c.execute("SELECT MAX(id) FROM inventory")
    max_id = result.fetchone()[0] or 0
except sqlite3.Error as e:
    print(f"Failed to fetch max ID: {e}")
    max_id = 0


class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.heading = Label(master, text="Add to the Database", font=('arial 40 bold'), fg='steelblue')
        self.heading.place(x=400, y=0)

        # Labels
        self.name_l = Label(master, text="Enter Product Name", font=('arial 18 bold'))
        self.name_l.place(x=0, y=70)

        self.stock_l = Label(master, text="Enter Stocks", font=('arial 18 bold'))
        self.stock_l.place(x=0, y=120)

        self.cp_l = Label(master, text="Enter Cost Price", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=170)

        self.sp_l = Label(master, text="Enter Selling Price", font=('arial 18 bold'))
        self.sp_l.place(x=0, y=220)

        self.vendor_l = Label(master, text="Enter Vendor Name", font=('arial 18 bold'))
        self.vendor_l.place(x=0, y=270)

        self.vendor_phone_l = Label(master, text="Enter Vendor Phone Number", font=('arial 18 bold'))
        self.vendor_phone_l.place(x=0, y=320)

        # Entry Fields
        self.name_e = Entry(master, width=25, font=('arial 18 bold'))
        self.name_e.place(x=380, y=70)

        self.stock_e = Entry(master, width=25, font=('arial 18 bold'))
        self.stock_e.place(x=380, y=120)

        self.cp_e = Entry(master, width=25, font=('arial 18 bold'))
        self.cp_e.place(x=380, y=170)

        self.sp_e = Entry(master, width=25, font=('arial 18 bold'))
        self.sp_e.place(x=380, y=220)

        self.vendor_e = Entry(master, width=25, font=('arial 18 bold'))
        self.vendor_e.place(x=380, y=270)

        self.vendor_phone_e = Entry(master, width=25, font=('arial 18 bold'))
        self.vendor_phone_e.place(x=380, y=320)

        # Buttons
        self.btn_add = Button(master, text="Add To Database", width=25, height=2, bg='steelblue', fg='white',
                              command=self.get_items)
        self.btn_add.place(x=520, y=420)

        self.btn_clear = Button(master, text="Clear All Fields", width=18, height=2, bg='lightgreen',
                                command=self.clear_all)
        self.btn_clear.place(x=350, y=420)

        # Text Box for Logs
        self.tBox = Text(master, width=60, height=18)
        self.tBox.place(x=750, y=70)
        self.tBox.insert(END, "ID has reached upto: " + str(max_id))

    def get_items(self):
        try:
            # Fetch input values
            name = self.name_e.get()
            stock = self.stock_e.get()
            cp = self.cp_e.get()
            sp = self.sp_e.get()
            vendor = self.vendor_e.get()
            vendor_phone = self.vendor_phone_e.get()

            # Validate the inputs
            if not all([name, stock, cp, sp, vendor, vendor_phone]):
                tkinter.messagebox.showinfo("Error", "Please fill all the fields!")
                return

            # Convert numeric fields to appropriate types
            stock = int(stock)
            cp = float(cp)
            sp = float(sp)
            totalcp = cp * stock
            totalsp = sp * stock
            assumed_profit = totalsp - totalcp

            # Insert into the database
            sql = """INSERT INTO inventory (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            c.execute(sql, (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phone))
            conn.commit()

            # Log success and clear fields
            max_id = c.lastrowid
            self.tBox.insert(END, f"\nInserted {name} into the database with ID {max_id}")
            tkinter.messagebox.showinfo("Success", f"Added {name} to the database!")
            self.clear_all()
        except ValueError:
            tkinter.messagebox.showinfo("Error",
                                        "Please enter valid numeric values for stock, cost price, and selling price!")
        except sqlite3.Error as e:
            tkinter.messagebox.showinfo("Error", f"Failed to insert data: {e}")

    def clear_all(self):
        # Clear all input fields
        self.name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.cp_e.delete(0, END)
        self.sp_e.delete(0, END)
        self.vendor_e.delete(0, END)
        self.vendor_phone_e.delete(0, END)


root = Tk()
b = Database(root)

root.geometry("1280x1024+0+0")
root.title("Add to the Database")
root.mainloop()
