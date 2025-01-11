import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os

# File paths
INVENTORY_FILE = "inventory.csv"
TRANSACTIONS_FILE = "transactions.csv"
ACCOUNTING_FILE = "accounting.csv"
USERS_FILE = "users.csv"

# Initialize files if they do not exist
def initialize_file(file_path, columns):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

# Initialize all required files
initialize_file(INVENTORY_FILE, ["Item ID", "Name", "Brand", "Type", "Functionality Type", "Stock Quantity", "Low Stock Threshold", "Unit Price", "Last Updated", "Location"])
initialize_file(TRANSACTIONS_FILE, ["Transaction ID", "Date", "Customer Name", "Total Amount", "Notes"])
initialize_file(ACCOUNTING_FILE, ["Entry ID", "Date", "Type", "Description", "Amount"])
initialize_file(USERS_FILE, ["User ID", "Username", "Pin", "Role"])

ROLE_PERMISSIONS = {
    "Master Admin": {
        "can_add_transaction": True,
        "can_update_item_price": True,
        "can_restock": True,
        "can_view_transactions": True,
        "can_update_password": True,
        "can_delete_inventory": True,
        "can_delete_transaction": True,
    },
    "Admin": {
        "can_add_transaction": True,
        "can_update_item_price": True,
        "can_restock": True,
        "can_view_transactions": True,
        "can_update_password": False,
        "can_delete_inventory": False,
        "can_delete_transaction": False,
    },
    "Staff": {
        "can_add_transaction": True,
        "can_update_item_price": False,
        "can_restock": False,
        "can_view_transactions": True,
        "can_update_password": False,
        "can_delete_inventory": False,
        "can_delete_transaction": False,
    },
}

# Load data from CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Save data to CSV
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# Application class
class InventoryManagementSystem: #InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")

        # Login frame
        self.setup_login()
        # self.login_frame = ttk.Frame(root)
        # self.login_frame.pack(fill="both", expand=True)

        # ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        # self.username_entry = ttk.Entry(self.login_frame)
        # self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # ttk.Label(self.login_frame, text="Pin:").grid(row=1, column=0, padx=10, pady=10)
        # self.pin_entry = ttk.Entry(self.login_frame, show="*")
        # self.pin_entry.grid(row=1, column=1, padx=10, pady=10)

        # ttk.Button(self.login_frame, text="Login", command=self.authenticate_user).grid(row=2, columnspan=2, pady=20)

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.inventory_tab = ttk.Frame(self.tab_control)
        self.transactions_tab = ttk.Frame(self.tab_control)
        self.accounting_tab = ttk.Frame(self.tab_control)
        self.user_management_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.inventory_tab, text="Inventory")
        self.tab_control.add(self.transactions_tab, text="Transactions")
        self.tab_control.add(self.accounting_tab, text="Accounting")
        self.tab_control.add(self.user_management_tab, text="User Management")

        # Load data
        self.inventory_data = load_data(INVENTORY_FILE)
        self.transactions_data = load_data(TRANSACTIONS_FILE)
        self.accounting_data = load_data(ACCOUNTING_FILE)
        self.users_data = load_data(USERS_FILE)

    def setup_login(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.login_frame, text="Pin:").grid(row=1, column=0, padx=10, pady=10)
        self.pin_entry = ttk.Entry(self.login_frame, show="*")
        self.pin_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.login_frame, text="Login", command=self.authenticate_user).grid(row=2, columnspan=2, pady=20)


    def authenticate_user(self):
        # username = self.username_entry.get().strip()
        # pin = self.pin_entry.get().strip()

        # user = self.users_data[(self.users_data['Username'] == username) & (self.users_data['Pin'] == pin)]

        # if not user.empty:
        #     self.role = user.iloc[0]['Role']
        #     self.permissions = ROLE_PERMISSIONS[self.role]
        #     self.login_frame.destroy()
        #     self.tab_control.pack(expand=1, fill="both")
        #     self.setup_tabs()
        # else:
        #     messagebox.showerror("Error", "Invalid username or pin")

        username = self.username_entry.get()
        pin = self.pin_entry.get()

        # Ensure the Pin is treated as a string and whitespace is removed
        self.users_data['Username'] = self.users_data['Username'].str.strip()
        self.users_data['Pin'] = self.users_data['Pin'].astype(str).str.strip()


        user = self.users_data[(self.users_data['Username'] == username) & (self.users_data['Pin'] == pin)]

        if not user.empty:
            role = user.iloc[0]['Role']
            self.login_frame.destroy()
            self.tab_control.pack(expand=1, fill="both")
            self.role = role
            self.setup_tabs()
        else:
            messagebox.showerror("Error", "Invalid username or pin")

    def setup_tabs(self):
        if self.role == "Master Admin":
            self.setup_inventory_tab()
            self.setup_transactions_tab()
            self.setup_accounting_tab()
            self.setup_user_management_tab()
        elif self.role == "Admin":
            self.setup_inventory_tab(admin=True)
            self.setup_transactions_tab()
            self.setup_accounting_tab()
        elif self.role == "Staff":
            self.setup_transactions_tab()
        
        # Add "Log Out" button
        logout_button = ttk.Button(self.root, text="Log Out", command=self.logout)
        logout_button.pack(side="bottom", pady=10)
    
    def logout(self):
        """Logs out the user and returns to the login screen."""
        self.tab_control.pack_forget()
        self.setup_login()

    def setup_inventory_tab(self, admin=False):
        # Inventory table
        self.inventory_tree = ttk.Treeview(self.inventory_tab, columns=("Item ID", "Name", "Brand", "Type", "Stock Quantity", "Low Stock Threshold"), show="headings")
        self.inventory_tree.heading("Item ID", text="Item ID")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Brand", text="Brand")
        self.inventory_tree.heading("Type", text="Type")
        self.inventory_tree.heading("Stock Quantity", text="Stock Quantity")
        self.inventory_tree.heading("Low Stock Threshold", text="Low Stock Threshold")
        self.inventory_tree.pack(fill="both", expand=True)

        self.load_inventory_tree()

        # Buttons
        if not admin:
            button_frame = ttk.Frame(self.inventory_tab)
            button_frame.pack(fill="x")

            ttk.Button(button_frame, text="Add Item", command=self.add_inventory_item).pack(side="left")
            ttk.Button(button_frame, text="Delete Item", command=self.delete_inventory_item).pack(side="left")
            ttk.Button(button_frame, text="Save Changes", command=self.save_inventory_changes).pack(side="right")

    def setup_transactions_tab(self):
        ttk.Label(self.transactions_tab, text="Transaction Management Coming Soon").pack()

    def setup_accounting_tab(self):
        ttk.Label(self.accounting_tab, text="Accounting Module Coming Soon").pack()

    def setup_user_management_tab(self):
        ttk.Label(self.user_management_tab, text="User Management Coming Soon").pack()

    def load_inventory_tree(self):
        # Clear the tree
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)

        # Add data to the tree
        for _, row in self.inventory_data.iterrows():
            self.inventory_tree.insert("", "end", values=row.tolist())

    def add_inventory_item(self):
        def save_new_item():
            new_item = {
                "Item ID": item_id_entry.get(),
                "Name": name_entry.get(),
                "Brand": brand_entry.get(),
                "Type": type_entry.get(),
                "Stock Quantity": int(stock_entry.get()),
                "Low Stock Threshold": int(threshold_entry.get()),
                "Unit Price": float(price_entry.get()),
                "Last Updated": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "Location": location_entry.get()
            }
            self.inventory_data = self.inventory_data.append(new_item, ignore_index=True)
            self.load_inventory_tree()
            new_item_window.destroy()

        new_item_window = tk.Toplevel(self.root)
        new_item_window.title("Add Inventory Item")

        ttk.Label(new_item_window, text="Item ID:").grid(row=0, column=0)
        item_id_entry = ttk.Entry(new_item_window)
        item_id_entry.grid(row=0, column=1)

        ttk.Label(new_item_window, text="Name:").grid(row=1, column=0)
        name_entry = ttk.Entry(new_item_window)
        name_entry.grid(row=1, column=1)

        ttk.Label(new_item_window, text="Brand:").grid(row=2, column=0)
        brand_entry = ttk.Entry(new_item_window)
        brand_entry.grid(row=2, column=1)

        ttk.Label(new_item_window, text="Type:").grid(row=3, column=0)
        type_entry = ttk.Entry(new_item_window)
        type_entry.grid(row=3, column=1)

        ttk.Label(new_item_window, text="Stock Quantity:").grid(row=4, column=0)
        stock_entry = ttk.Entry(new_item_window)
        stock_entry.grid(row=4, column=1)

        ttk.Label(new_item_window, text="Low Stock Threshold:").grid(row=5, column=0)
        threshold_entry = ttk.Entry(new_item_window)
        threshold_entry.grid(row=5, column=1)

        ttk.Label(new_item_window, text="Unit Price:").grid(row=6, column=0)
        price_entry = ttk.Entry(new_item_window)
        price_entry.grid(row=6, column=1)

        ttk.Label(new_item_window, text="Location:").grid(row=7, column=0)
        location_entry = ttk.Entry(new_item_window)
        location_entry.grid(row=7, column=1)

        ttk.Button(new_item_window, text="Save", command=save_new_item).grid(row=8, columnspan=2)

    def delete_inventory_item(self):
        # Get selected item
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
        if confirm:
            # Delete selected item from the tree and dataframe
            for item in selected_item:
                values = self.inventory_tree.item(item, "values")
                self.inventory_data = self.inventory_data[self.inventory_data["Item ID"] != values[0]]
                self.inventory_tree.delete(item)

    def save_inventory_changes(self):
        # Save updated inventory data to CSV
        save_data(self.inventory_data, INVENTORY_FILE)
        messagebox.showinfo("Success", "Inventory changes have been saved.")
        
    def setup_transactions_tab(self):
        # Transactions table
        self.transactions_tree = ttk.Treeview(
            self.transactions_tab,
            columns=("Transaction ID", "Date", "Customer Name", "Total Amount", "Notes"),
            show="headings"
        )
        self.transactions_tree.heading("Transaction ID", text="Transaction ID")
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Customer Name", text="Customer Name")
        self.transactions_tree.heading("Total Amount", text="Total Amount")
        self.transactions_tree.heading("Notes", text="Notes")
        self.transactions_tree.pack(fill="both", expand=True)

        # Load existing transactions
        self.load_transactions_tree()

        # Add buttons for managing transactions
        button_frame = ttk.Frame(self.transactions_tab)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction).pack(side="left")
        ttk.Button(button_frame, text="Delete Transaction", command=self.delete_transaction).pack(side="left")
        ttk.Button(button_frame, text="Save Changes", command=self.save_transactions_changes).pack(side="right")

    def load_transactions_tree(self):
        # Clear the tree
        for row in self.transactions_tree.get_children():
            self.transactions_tree.delete(row)

        # Add data to the tree
        for _, row in self.transactions_data.iterrows():
            self.transactions_tree.insert("", "end", values=row.tolist())

    def add_transaction(self):
        def save_new_transaction():
            new_transaction = {
                "Transaction ID": transaction_id_entry.get(),
                "Date": date_entry.get(),
                "Customer Name": customer_name_entry.get(),
                "Total Amount": float(total_amount_entry.get()),
                "Notes": notes_entry.get()
            }
            self.transactions_data = self.transactions_data.append(new_transaction, ignore_index=True)
            self.load_transactions_tree()
            new_transaction_window.destroy()

        new_transaction_window = tk.Toplevel(self.root)
        new_transaction_window.title("Add Transaction")

        ttk.Label(new_transaction_window, text="Transaction ID:").grid(row=0, column=0)
        transaction_id_entry = ttk.Entry(new_transaction_window)
        transaction_id_entry.grid(row=0, column=1)

        ttk.Label(new_transaction_window, text="Date:").grid(row=1, column=0)
        date_entry = ttk.Entry(new_transaction_window)
        date_entry.grid(row=1, column=1)

        ttk.Label(new_transaction_window, text="Customer Name:").grid(row=2, column=0)
        customer_name_entry = ttk.Entry(new_transaction_window)
        customer_name_entry.grid(row=2, column=1)

        ttk.Label(new_transaction_window, text="Total Amount:").grid(row=3, column=0)
        total_amount_entry = ttk.Entry(new_transaction_window)
        total_amount_entry.grid(row=3, column=1)

        ttk.Label(new_transaction_window, text="Notes:").grid(row=4, column=0)
        notes_entry = ttk.Entry(new_transaction_window)
        notes_entry.grid(row=4, column=1)

        ttk.Button(new_transaction_window, text="Save", command=save_new_transaction).grid(row=5, columnspan=2)

    def delete_transaction(self):
        selected_item = self.transactions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?")
        if confirm:
            for item in selected_item:
                values = self.transactions_tree.item(item, "values")
                self.transactions_data = self.transactions_data[self.transactions_data["Transaction ID"] != values[0]]
                self.transactions_tree.delete(item)

    def save_transactions_changes(self):
        save_data(self.transactions_data, TRANSACTIONS_FILE)
        messagebox.showinfo("Success", "Transaction changes have been saved.")
        
    def setup_accounting_tab(self):
        # Tabs for accounting
        self.accounting_notebook = ttk.Notebook(self.accounting_tab)
        self.balance_sheet_tab = ttk.Frame(self.accounting_notebook)
        self.profit_loss_tab = ttk.Frame(self.accounting_notebook)

        self.accounting_notebook.add(self.balance_sheet_tab, text="Balance Sheet")
        self.accounting_notebook.add(self.profit_loss_tab, text="Profit & Loss")
        self.accounting_notebook.pack(fill="both", expand=True)

        # Balance Sheet
        self.balance_sheet_tree = ttk.Treeview(
            self.balance_sheet_tab,
            columns=("Account", "Debit", "Credit"),
            show="headings"
        )
        self.balance_sheet_tree.heading("Account", text="Account")
        self.balance_sheet_tree.heading("Debit", text="Debit")
        self.balance_sheet_tree.heading("Credit", text="Credit")
        self.balance_sheet_tree.pack(fill="both", expand=True)

        self.load_balance_sheet()

        # Profit & Loss
        self.profit_loss_tree = ttk.Treeview(
            self.profit_loss_tab,
            columns=("Category", "Amount"),
            show="headings"
        )
        self.profit_loss_tree.heading("Category", text="Category")
        self.profit_loss_tree.heading("Amount", text="Amount")
        self.profit_loss_tree.pack(fill="both", expand=True)

        self.load_profit_loss()

    def load_balance_sheet(self):
        # Placeholder: Replace with real calculations
        balance_sheet_data = [
            {"Account": "Cash", "Debit": 5000, "Credit": 0},
            {"Account": "Inventory", "Debit": 2000, "Credit": 0},
            {"Account": "Accounts Payable", "Debit": 0, "Credit": 1000},
        ]
        for row in balance_sheet_data:
            self.balance_sheet_tree.insert("", "end", values=(row["Account"], row["Debit"], row["Credit"]))

    def load_profit_loss(self):
        # Placeholder: Replace with real calculations
        profit_loss_data = [
            {"Category": "Sales Revenue", "Amount": 10000},
            {"Category": "Cost of Goods Sold", "Amount": -4000},
            {"Category": "Net Profit", "Amount": 6000},
        ]
        for row in profit_loss_data:
            self.profit_loss_tree.insert("", "end", values=(row["Category"], row["Amount"]))

    def setup_user_management_tab(self):
        # User management table
        self.user_tree = ttk.Treeview(
            self.user_management_tab,
            columns=("User ID", "Username", "Role"),
            show="headings"
        )
        self.user_tree.heading("User ID", text="User ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Role", text="Role")
        self.user_tree.pack(fill="both", expand=True)

        # Load existing users
        self.load_user_tree()

        # Buttons for managing users
        button_frame = ttk.Frame(self.user_management_tab)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Add User", command=self.add_user).pack(side="left")
        ttk.Button(button_frame, text="Delete User", command=self.delete_user).pack(side="left")
        ttk.Button(button_frame, text="Save Changes", command=self.save_user_changes).pack(side="right")

    def load_user_tree(self):
        for row in self.user_data.iterrows():
            self.user_tree.insert("", "end", values=row[1].tolist())

    def add_user(self):
        def save_new_user():
            new_user = {
                "User ID": user_id_entry.get(),
                "Username": username_entry.get(),
                "Role": role_combobox.get(),
            }
            self.user_data = self.user_data.append(new_user, ignore_index=True)
            self.load_user_tree()
            new_user_window.destroy()

        new_user_window = tk.Toplevel(self.root)
        new_user_window.title("Add User")

        ttk.Label(new_user_window, text="User ID:").grid(row=0, column=0)
        user_id_entry = ttk.Entry(new_user_window)
        user_id_entry.grid(row=0, column=1)

        ttk.Label(new_user_window, text="Username:").grid(row=1, column=0)
        username_entry = ttk.Entry(new_user_window)
        username_entry.grid(row=1, column=1)

        ttk.Label(new_user_window, text="Role:").grid(row=2, column=0)
        role_combobox = ttk.Combobox(new_user_window, values=["Master", "Admin"])
        role_combobox.grid(row=2, column=1)

        ttk.Button(new_user_window, text="Save", command=save_new_user).grid(row=3, columnspan=2)

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        if confirm:
            for item in selected_item:
                values = self.user_tree.item(item, "values")
                self.user_data = self.user_data[self.user_data["User ID"] != values[0]]
                self.user_tree.delete(item)

    def save_user_changes(self):
        save_data(self.user_data, USERS_FILE)
        messagebox.showinfo("Success", "User changes have been saved.")
    
    def on_close(self):
        if messagebox.askokcancel("Logout", "Do you want to logout and exit?"):
            self.logout()

    # def logout(self):
    #     self.tab_control.forget(self.inventory_tab)
    #     self.tab_control.forget(self.transactions_tab)
    #     self.tab_control.forget(self.accounting_tab)
    #     self.tab_control.forget(self.user_management_tab)
    #     self.setup_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root) #InventoryApp(root)
    root.mainloop()
