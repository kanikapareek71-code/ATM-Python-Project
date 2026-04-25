import tkinter as tk
from tkinter import messagebox
from services.atm_service import *

current_user = None

root = tk.Tk()
root.title("ATM System")
root.geometry("400x500")
root.configure(bg="#1e1e2f")


# ---------- COMMON BUTTON STYLE ----------
btn_style = {
    "width": 22,
    "height": 2,
    "fg": "white",
    "font": ("Arial", 10, "bold"),
    "bd": 0
}


# ---------- CLEAR WINDOW ----------
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# ---------- LOGIN ----------
def login_screen():
    clear_window()

    tk.Label(root, text="ATM LOGIN", font=("Arial", 18, "bold"),
             bg="#1e1e2f", fg="white").pack(pady=20)

    tk.Label(root, text="Username", bg="#1e1e2f", fg="white").pack()
    username = tk.Entry(root, font=("Arial", 12))
    username.pack(pady=5)

    tk.Label(root, text="PIN", bg="#1e1e2f", fg="white").pack()
    pin = tk.Entry(root, show="*", font=("Arial", 12))
    pin.pack(pady=5)

    def login():
        global current_user
        if verify_user(username.get(), pin.get()):
            current_user = username.get()
            atm_screen()
        else:
            messagebox.showerror("Error", "Invalid login")

    tk.Button(root, text="Login", bg="#4CAF50",
              command=login, **btn_style).pack(pady=10)

    tk.Button(root, text="Create New Account", bg="#2196F3",
              command=signup_screen, **btn_style).pack()


# ---------- SIGNUP ----------
def signup_screen():
    clear_window()

    tk.Label(root, text="CREATE ACCOUNT", font=("Arial", 16, "bold"),
             bg="#1e1e2f", fg="white").pack(pady=15)

    tk.Label(root, text="Username", bg="#1e1e2f", fg="white").pack()
    username = tk.Entry(root)
    username.pack(pady=5)

    tk.Label(root, text="Set PIN (4 digit)", bg="#1e1e2f", fg="white").pack()
    pin = tk.Entry(root, show="*")
    pin.pack(pady=5)

    tk.Label(root, text="Initial Deposit", bg="#1e1e2f", fg="white").pack()
    amount = tk.Entry(root)
    amount.pack(pady=5)

    def signup():
        try:
            amt = float(amount.get())
            result = create_account(username.get(), pin.get(), amt)
            messagebox.showinfo("Result", result)
            if result == "Account created successfully":
                login_screen()
        except:
            messagebox.showerror("Error", "Invalid amount")

    tk.Button(root, text="Create Account", bg="#4CAF50",
              command=signup, **btn_style).pack(pady=10)

    tk.Button(root, text="Back to Login", bg="gray",
              command=login_screen, **btn_style).pack()


# ---------- ATM ----------
def atm_screen():
    clear_window()

    tk.Label(root, text=f"Welcome, {current_user}",
             font=("Arial", 16, "bold"),
             bg="#1e1e2f", fg="white").pack(pady=15)

    tk.Label(root, text="Enter Amount",
             bg="#1e1e2f", fg="white").pack()

    entry = tk.Entry(root, font=("Arial", 12), justify="center")
    entry.pack(pady=10)

    def show_balance():
        messagebox.showinfo("Balance", f"₹{check_balance(current_user)}")

    def deposit_money():
        try:
            amt = float(entry.get())
            messagebox.showinfo("Deposit", deposit(current_user, amt))
        except:
            messagebox.showerror("Error", "Invalid amount")

    def withdraw_money():
        try:
            amt = float(entry.get())
            messagebox.showinfo("Withdraw", withdraw(current_user, amt))
        except:
            messagebox.showerror("Error", "Invalid amount")

    def show_statement():
        data = get_statement(current_user)
        text = "\n\n".join(
            [f"{t['type']} ₹{t['amount']}\n{t['time']}" for t in data]
        )
        messagebox.showinfo("Statement", text if text else "No transactions")

    def change_pin_screen():
        win = tk.Toplevel(root)
        win.title("Change PIN")
        win.geometry("300x250")
        win.configure(bg="#1e1e2f")

        tk.Label(win, text="Old PIN", bg="#1e1e2f", fg="white").pack(pady=5)
        old = tk.Entry(win, show="*")
        old.pack()

        tk.Label(win, text="New PIN", bg="#1e1e2f", fg="white").pack(pady=5)
        new = tk.Entry(win, show="*")
        new.pack()

        def update():
            result = change_pin(current_user, old.get(), new.get())
            messagebox.showinfo("Result", result)
            if result == "PIN changed successfully":
                win.destroy()

        tk.Button(win, text="Update PIN", bg="#2196F3", fg="white",
                  command=update).pack(pady=15)

    # BUTTONS (Styled)
    tk.Button(root, text="Check Balance", bg="#4CAF50",
              command=show_balance, **btn_style).pack(pady=5)

    tk.Button(root, text="Deposit", bg="#2196F3",
              command=deposit_money, **btn_style).pack(pady=5)

    tk.Button(root, text="Withdraw", bg="#f44336",
              command=withdraw_money, **btn_style).pack(pady=5)

    tk.Button(root, text="Statement", bg="#9C27B0",
              command=show_statement, **btn_style).pack(pady=5)

    tk.Button(root, text="Change PIN", bg="#FF9800",
              command=change_pin_screen, **btn_style).pack(pady=5)

    tk.Button(root, text="Logout", bg="gray",
              command=login_screen, **btn_style).pack(pady=15)


# ---------- START ----------
login_screen()
root.mainloop()