import argparse
from datetime import datetime
import csv
from tkinter import filedialog
import tkinter as tk

print ("Expenses")

expenses = []

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%m-%d-%Y')
        return True
    except ValueError:
        return False

def add_expense(description, amount, date):
    try:
        amount = int(amount)
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
        if not validate_date(date):
            print("Invalid date format. Please use MM-DD-YYYY format (e.g., 03-15-2024).")
            return
        expenses.append({"description": description, "amount": amount, "date": date})
        print(f"Added expense: {description} - ${amount} - {date}")
    except ValueError:
        print("Invalid amount. Please enter a whole number.")

def view_expenses():
    print("Expenses:")
    if not expenses:
        print("No expenses recorded yet.")
    else:
        for i, expense in enumerate(expenses, 1):
            print(f"{i}. {expense['description']} - ${expense['amount']} - {expense['date']}")

def update_expense(index, description, amount, date):
    if index < 1 or index > len(expenses):
        print("Invalid expense index.")
        return
    try:
        amount = int(amount)
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
        if not validate_date(date):
            print("Invalid date format. Please use MM-DD-YYYY format (e.g., 03-15-2024).")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    index = int(index)
    expenses[index-1] = {"description": description, "amount": amount, "date": date}
    print(f"Updated expense {index}: {description} - ${amount} - {date}")

def delete_expense(index):
    try:
        if 1 <= index <= len(expenses):
            deleted_expense = expenses.pop(index - 1)
            print(f"Deleted expense: {deleted_expense['description']} - ${deleted_expense['amount']} - {deleted_expense['date']}")
        else:
            print("Invalid expense index.")
    except IndexError:
        print("Invalid expense index.")
    
def view_summary():
    print("Summary:")
    Total = 0
    for expense in expenses:
        Total += expense['amount']
    print(f"Total expenses: ${Total}")
    return Total

def view_summary_month(month):
    Total = 0
    current_year = datetime.now().year
    for expense in expenses:
        # Split date into MM-DD-YYYY
        date_parts = expense['date'].split('-')
        expense_month = date_parts[0]
        expense_year = int(date_parts[2])
        if expense_month == month and expense_year == current_year:
            Total += expense['amount']
    print(f"Total expenses for {month}/{current_year}: ${Total}")
    return Total
    
def export_expenses():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Open file dialog to choose save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save Expenses as CSV"
    )
    
    if file_path:  # If user didn't cancel
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(['Description', 'Amount', 'Date'])
                # Write expenses
                for expense in expenses:
                    writer.writerow([expense['description'], expense['amount'], expense['date']])
            print(f"Expenses exported successfully to {file_path}")
        except Exception as e:
            print(f"Error exporting expenses: {e}")
    else:
        print("Export cancelled")

def format_date_input(date_str):
    # Remove any existing dashes
    date_str = date_str.replace('-', '')
    
    # Add dashes after every 2 digits
    if len(date_str) >= 2:
        date_str = date_str[:2] + '-' + date_str[2:]
    if len(date_str) >= 5:
        date_str = date_str[:5] + '-' + date_str[5:]
    
    return date_str

def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. View Summary")
        print("6. Export Expenses")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Add Expense:")
            description = input("Enter expense description: ")
            amount = input("Enter expense amount: $")
            date = ""
            while len(date) < 8:  # Keep accepting input until we have 8 digits
                new_digit = input("Enter date (MMDDYYYY): ")
                if new_digit.isdigit():
                    date += new_digit
                    formatted_date = format_date_input(date)
                    print(f"Current date: {formatted_date}")
            add_expense(description, amount, formatted_date)
        elif choice == "2":
            print ("View Expenses:")
            view_expenses()
        elif choice == "3":
            print ("Update Expense:")
            index = int(input("Enter the index of the expense to update: "))
            description = input("Enter new description: ")
            amount = input("Enter new amount: $")
            date = ""
            while len(date) < 8:  # Keep accepting input until we have 8 digits
                new_digit = input("Enter date (MMDDYYYY): ")
                if new_digit.isdigit():
                    date += new_digit
                    formatted_date = format_date_input(date)
                    print(f"Current date: {formatted_date}")
            update_expense(index, description, amount, formatted_date)
        elif choice == "4":
            print ("Delete Expense:")
            index = int(input("Enter the index of the expense to delete: "))
            delete_expense(index)
        elif choice == "5":
            month_input = input("Enter month (MM) or press enter: ")
            if month_input == "":
                view_summary()
            else:
                view_summary_month(month_input)
        elif choice == "6":
            print ("Export Expenses:")
            export_expenses()
        elif choice == "7":
            print ("Exiting...")
            break
            
if __name__ == "__main__":
    main()
                
    
