import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import datetime
import os
print("Current working directory:", os.getcwd())


# Helper Functions
def read_csv(file_name):
    data = []
    if os.path.exists(file_name):
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data


def write_csv(file_name, fieldnames, data):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def generate_transaction_id():
    now = datetime.datetime.now()
    date_part = now.strftime("%Y%m%d")
    transactions = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/transaction.csv')
    daily_count = len([t for t in transactions if t['date'] == now.strftime('%Y-%m-%d')]) + 1
    return f"{date_part}{daily_count:04d}"


# Authentication
def authenticate_user(username, pin):
    users = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/users.csv')
    print("Loaded users:", users)  # Debugging: Show loaded users
    for user in users:
        print(f"Checking {user['username']} against {username}, PIN {pin}")  # Debugging
        if user['username'] == username and user['pin'] == pin:
            return user
    return None



# Inventory Management
def update_inventory(item_name, quantity_sold):
    inventory = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/inventory.csv')
    for item in inventory:
        if item['item_name'] == item_name:
            item['current_quantity'] = str(int(item['current_quantity']) - quantity_sold)
    write_csv('inventory.csv', inventory[0].keys(), inventory)


# Application Class
class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("800x600")
        self.user = None

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()

        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self)
        username_entry.pack()

        tk.Label(self, text="PIN:").pack()
        pin_entry = tk.Entry(self, show="*")
        pin_entry.pack()

        def handle_login():
            username = username_entry.get()
            pin = pin_entry.get()

            user = authenticate_user(username, pin)
            if user:
                self.user = user
                self.create_main_screen()
            else:
                messagebox.showerror("Error", "Invalid username or PIN.")

        tk.Button(self, text="Login", command=handle_login).pack(pady=10)

    def create_main_screen(self):
        self.clear_window()

        tk.Label(self, text=f"Welcome, {self.user['username']}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Manage Inventory", command=self.create_inventory_screen).pack(pady=5)
        tk.Button(self, text="Record Transaction", command=self.create_transaction_screen).pack(pady=5)
        tk.Button(self, text="Generate Report", command=self.create_report_screen).pack(pady=5)
        tk.Button(self, text="Logout", command=self.create_login_screen).pack(pady=5)

    def create_inventory_screen(self):
        self.clear_window()
        inventory = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/inventory.csv')

        tk.Label(self, text="Inventory Management", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self, columns=list(inventory[0].keys()), show="headings")
        for col in inventory[0].keys():
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in inventory:
            tree.insert('', 'end', values=list(row.values()))
        tree.pack(expand=True, fill='both')

        tk.Button(self, text="Back", command=self.create_main_screen).pack(pady=10)

    def create_transaction_screen(self):
        self.clear_window()
        inventory = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/inventory.csv')

        tk.Label(self, text="Record Transaction", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Item Name:").pack()
        item_name_combo = ttk.Combobox(self, values=[item['item_name'] for item in inventory])
        item_name_combo.pack()

        tk.Label(self, text="Quantity:").pack()
        quantity_entry = tk.Entry(self)
        quantity_entry.pack()

        def handle_transaction():
            item_name = item_name_combo.get()
            quantity = int(quantity_entry.get())

            for item in inventory:
                if item['item_name'] == item_name:
                    if quantity > int(item['current_quantity']):
                        messagebox.showerror("Error", "Not enough stock.")
                        return
                    total_value = quantity * int(item['unit_cost'])
                    transaction_id = generate_transaction_id()
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                    time = datetime.datetime.now().strftime("%H:%M:%S")
                    transaction = {
                        "transaction_id": transaction_id,
                        "date": date,
                        "time": time,
                        "total_value": total_value,
                        "item_name": item_name,
                        "quantity": quantity,
                    }
                    transactions = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/transactions.csv')
                    transactions.append(transaction)
                    write_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/transactions.csv', transactions[0].keys(), transactions)
                    update_inventory(item_name, quantity)
                    messagebox.showinfo("Success", "Transaction recorded.")
                    return

        tk.Button(self, text="Record", command=handle_transaction).pack(pady=10)
        tk.Button(self, text="Back", command=self.create_main_screen).pack(pady=10)

    def create_report_screen(self):
        self.clear_window()
        transactions = read_csv('C:/Users/user/OneDrive/Documents/GitHub/Workshop/(2)/transactions.csv')

        tk.Label(self, text="Transaction Report", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self, columns=list(transactions[0].keys()), show="headings")
        for col in transactions[0].keys():
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in transactions:
            tree.insert('', 'end', values=list(row.values()))
        tree.pack(expand=True, fill='both')

        tk.Button(self, text="Back", command=self.create_main_screen).pack(pady=10)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
