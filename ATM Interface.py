import tkinter as tk
from tkinter import simpledialog, messagebox

class Account:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def record_transaction(self, description):
        self.transactions.append(description)

class TransactionHistory:
    @staticmethod
    def show_history(account):
        trans = "\n".join(account.transactions)
        messagebox.showinfo("Transaction History", f"Transactions:\n{trans}")

class TransactionHandler:
    @staticmethod
    def handle_transaction(account, amount, transaction_type, other_account=None):
        if transaction_type == "withdraw":
            if account.balance >= amount:
                account.balance -= amount
                account.record_transaction(f"Withdrew ₹{amount:.2f}")
                messagebox.showinfo("Success", f"₹{amount:.2f} has been withdrawn.")
            else:
                messagebox.showerror("Error", "Insufficient funds")
        elif transaction_type == "deposit":
            account.balance += amount
            account.record_transaction(f"Deposited ₹{amount:.2f}")
            messagebox.showinfo("Success", f"₹{amount:.2f} has been deposited.")
        elif transaction_type == "transfer":
            if account.balance >= amount:
                account.balance -= amount
                other_account.balance += amount
                account.record_transaction(f"Transferred ₹{amount:.2f} to {other_account.user_id}")
                other_account.record_transaction(f"Received ₹{amount:.2f} from {account.user_id}")
                messagebox.showinfo("Success", f"Transferred ₹{amount:.2f} to {other_account.user_id}")
            else:
                messagebox.showerror("Error", "Insufficient funds")

class ATMApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM")
        self.master.geometry("600x400")
        self.master.configure(bg="#E0E0E0") 

        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)

        self.accounts = {
            "ABCD@123": Account("ABCD@123", "1010", 5000),
            "PQR@456": Account("PQR@456", "2202", 1000)
        }

        self.create_login_window()

    def create_login_window(self):
        title = tk.Label(self.master, text="ATM", font=("Helvetica", 16), bg="#E0E0E0", fg="#4E342E")  
        title.grid(row=0, column=0, columnspan=5, pady=20)

        tk.Label(self.master, text="User ID", bg="#E0E0E0", fg="#4E342E").grid(row=1, column=1, padx=20, pady=10)
        tk.Label(self.master, text="PIN", bg="#E0E0E0", fg="#4E342E").grid(row=2, column=1, padx=20, pady=10)

        self.e1 = tk.Entry(self.master)
        self.e2 = tk.Entry(self.master, show="*")

        self.e1.grid(row=1, column=2, padx=20, pady=10, columnspan=2)
        self.e2.grid(row=2, column=2, padx=20, pady=10, columnspan=2)

        tk.Button(self.master, text="Quit", command=self.master.destroy, width=15, bg="#FFAB91", fg="#4E342E").grid(row=5, column=2, pady=5)
        tk.Button(self.master, text="Login", command=self.login, width=15, bg="#81C784", fg="#4E342E").grid(row=4, column=2, pady=5)

    def login(self):
        user_id = self.e1.get()
        pin = self.e2.get()

        if user_id in self.accounts and self.accounts[user_id].pin == pin:
            self.current_account = self.accounts[user_id]
            messagebox.showinfo("Success", "ATM functionality unlocked.")
            self.show_options()
        else:
            messagebox.showerror("Error", "Invalid User ID or PIN")

    def show_options(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.configure(bg="#FFFFFF")  

        title = tk.Label(self.master, text="ATM", font=("Helvetica", 16), bg="#FFFFFF", fg="#4E342E")
        title.grid(row=0, column=0, columnspan=5, pady=20)

        options = [
            ("Withdraw", lambda: self.handle_transaction_gui("withdraw")),
            ("Deposit", lambda: self.handle_transaction_gui("deposit")),
            ("Transfer", lambda: self.handle_transaction_gui("transfer")),
            ("Transactions History", lambda: TransactionHistory.show_history(self.current_account)),
            ("Quit", self.master.destroy)
        ]

        for i, (text, command) in enumerate(options, start=1):
            tk.Button(self.master, text=text, command=command, width=20, bg="#90CAF9", fg="#4E342E").grid(row=i, column=1, columnspan=3, padx=20, pady=5)

        # Additional Buttons
        tk.Button(self.master, text="Check Balance", command=self.check_balance_gui, width=20, bg="#FFD54F", fg="#4E342E").grid(row=5, column=1, columnspan=3, padx=20, pady=5)
        tk.Button(self.master, text="Change PIN", command=self.change_pin_gui, width=20, bg="#A5D6A7", fg="#4E342E").grid(row=6, column=1, columnspan=3, padx=20, pady=5)

    def handle_transaction_gui(self, transaction_type):
        if transaction_type == "transfer":
            self.handle_transfer()
        else:
            amount = simpledialog.askfloat(transaction_type.capitalize(), f"Enter amount to {transaction_type}:")
            if amount is not None:
                TransactionHandler.handle_transaction(self.current_account, amount, transaction_type)

    def handle_transfer(self):
        transfer_id = simpledialog.askstring("Transfer", "Enter User ID to transfer to:")
        if transfer_id in self.accounts:
            amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
            if amount is not None:
                TransactionHandler.handle_transaction(
                    self.current_account, amount, "transfer", self.accounts[transfer_id]
                )
        else:
            messagebox.showerror("Error", "Invalid User ID")

    def check_balance_gui(self):
        messagebox.showinfo("Balance", f"Your current balance is ₹{self.current_account.balance:.2f}")

    def change_pin_gui(self):
        new_pin = simpledialog.askstring("Change PIN", "Enter new PIN:")
        if new_pin is not None:
            self.current_account.pin = new_pin
            messagebox.showinfo("Success", "PIN has been changed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
