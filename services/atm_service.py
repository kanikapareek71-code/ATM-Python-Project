from models.account import load_data, save_data
from datetime import datetime


def create_account(username, pin, amount):
    data = load_data()

    if username in data:
        return "User already exists"

    if len(pin) != 4 or not pin.isdigit():
        return "PIN must be 4 digits"

    data[username] = {
        "pin": pin,
        "balance": amount,
        "transactions": []
    }

    save_data(data)
    return "Account created successfully"


def verify_user(username, pin):
    data = load_data()
    return username in data and data[username]["pin"] == pin


def change_pin(username, old_pin, new_pin):
    data = load_data()

    if data[username]["pin"] != old_pin:
        return "Wrong old PIN"

    if len(new_pin) != 4 or not new_pin.isdigit():
        return "PIN must be 4 digits"

    data[username]["pin"] = new_pin
    save_data(data)
    return "PIN changed successfully"


def check_balance(username):
    data = load_data()
    return data[username]["balance"]


def deposit(username, amount):
    data = load_data()

    if amount <= 0:
        return "Invalid amount"

    data[username]["balance"] += amount

    data[username]["transactions"].append({
        "type": "Deposit",
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    return f"Deposited ₹{amount}"


def withdraw(username, amount):
    data = load_data()

    if amount <= 0:
        return "Invalid amount"

    if amount > data[username]["balance"]:
        return "Insufficient balance"

    data[username]["balance"] -= amount

    data[username]["transactions"].append({
        "type": "Withdraw",
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    return f"Withdrawn ₹{amount}"


def get_statement(username):
    data = load_data()
    return data[username]["transactions"]
