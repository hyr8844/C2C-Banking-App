import mysql.connector
import unittest

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="BankSystem"
)
cursor = db.cursor()

# Banking functions
def check_balance(account_number, pin):
    cursor.execute("SELECT balance FROM Accounts WHERE account_number=%s AND pin=%s", (account_number, pin))
    result = cursor.fetchone()
    return f"Balance: ${result[0]}" if result else "Invalid credentials"

def deposit(account_number, amount):
    cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_number=%s", (amount, account_number))
    db.commit()
    log_transaction(account_number, f"Deposit of ${amount}")
    return "Deposit successful!"

def withdraw(account_number, amount):
    cursor.execute("SELECT balance FROM Accounts WHERE account_number=%s", (account_number,))
    result = cursor.fetchone()
    
    if result and result[0] >= amount:
        cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_number=%s", (amount, account_number))
        db.commit()
        log_transaction(account_number, f"Withdrawal of ${amount}")
        return "Withdrawal successful!"
    return "Insufficient funds or invalid account"

def create_account(name, pin, initial_balance=0):
    cursor.execute("INSERT INTO Accounts (pin, name, balance, account_type) VALUES (%s, %s, %s, 'customer')",
                   (pin, name, initial_balance))
    db.commit()
    return "Account created successfully!"

def delete_account(account_number):
    cursor.execute("DELETE FROM Accounts WHERE account_number=%s", (account_number,))
    db.commit()
    return "Account deleted successfully!"

def modify_account(account_number, field, new_value):
    cursor.execute(f"UPDATE Accounts SET {field}=%s WHERE account_number=%s", (new_value, account_number))
    db.commit()
    return f"{field} updated successfully!"

# Transaction logging
def log_transaction(account_number, description):
    cursor.execute("INSERT INTO Transactions (account_number, description) VALUES (%s, %s)", (account_number, description))
    db.commit()

# Text-based UI
def main_menu():
    while True:
        print("\nWelcome to Elite Bank!")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Create Account")
        print("5. Delete Account")
        print("6. Modify Account")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            acc = input("Enter Account Number: ")
            pin = input("Enter PIN: ")
            print(check_balance(acc, pin))
        elif choice == "2":
            acc = input("Enter Account Number: ")
            amt = float(input("Enter amount to deposit: "))
            print(deposit(acc, amt))
        elif choice == "3":
            acc = input("Enter Account Number: ")
            amt = float(input("Enter amount to withdraw: "))
            print(withdraw(acc, amt))
        elif choice == "4":
            name = input("Enter name: ")
            pin = input("Enter PIN: ")
            print(create_account(name, pin))
        elif choice == "5":
            acc = input("Enter Account Number to delete: ")
            print(delete_account(acc))
        elif choice == "6":
            acc = input("Enter Account Number: ")
            field = input("Enter field to modify (name/pin/balance): ")
            new_value = input("Enter new value: ")
            print(modify_account(acc, field, new_value))
        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

# Unit Testing
class TestBankingSystem(unittest.TestCase):
    def test_deposit(self):
        self.assertEqual(deposit(12345, 100), "Deposit successful!")

    def test_insufficient_funds(self):
        self.assertEqual(withdraw(12345, 100000), "Insufficient funds or invalid account")

    def test_create_account(self):
        self.assertEqual(create_account("Alice", 4321), "Account created successfully!")

if __name__ == '__main__':
    main_menu()
    unittest.main()
