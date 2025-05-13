import argparse
from datetime import datetime
import csv
import os
import sys
import json

print("Expenses")

# File to store expenses
EXPENSES_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        try:
            with open(EXPENSES_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error reading expenses file. Starting with empty list.")
            return []
    return []

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

expenses = load_expenses()

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
        save_expenses(expenses)
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
    save_expenses(expenses)
    print(f"Updated expense {index}: {description} - ${amount} - {date}")

def delete_expense(index):
    try:
        if 1 <= index <= len(expenses):
            deleted_expense = expenses.pop(index - 1)
            save_expenses(expenses)
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
    print("\nExport Expenses")
    print("Enter the full path where you want to save the CSV file")
    print("Example: C:/Users/YourName/Desktop/expenses.csv")
    file_path = input("Enter file path: ").strip()
    
    if not file_path:
        print("Export cancelled")
        return
        
    # Add .csv extension if not present
    if not file_path.lower().endswith('.csv'):
        file_path += '.csv'
    
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
    parser = argparse.ArgumentParser(description='Expense Tracker')
    parser.add_argument('--action', '-a', choices=['add', 'view', 'update', 'delete', 'summary', 'export'],
                      help='Action to perform: add, view, update, delete, summary, or export')
    parser.add_argument('--description', '-d', help='Expense description')
    parser.add_argument('--amount', '-m', help='Expense amount')
    parser.add_argument('--date', '-t', help='Expense date (MMDDYYYY)')
    parser.add_argument('--index', '-i', type=int, help='Index of expense to update/delete')
    parser.add_argument('--month', '-M', help='Month for summary (MM)')
    parser.add_argument('--output', '-o', help='Output file path for export')

    args = parser.parse_args()

    if not args.action:
        print("Please specify an action using --action or -a")
        print("Available actions: add, view, update, delete, summary, export")
        sys.exit(1)

    if args.action == 'add':
        if not all([args.description, args.amount, args.date]):
            print("Error: --description, --amount, and --date are required for adding expenses")
            sys.exit(1)
        formatted_date = format_date_input(args.date)
        add_expense(args.description, args.amount, formatted_date)

    elif args.action == 'view':
        view_expenses()

    elif args.action == 'update':
        if not all([args.index, args.description, args.amount, args.date]):
            print("Error: --index, --description, --amount, and --date are required for updating expenses")
            sys.exit(1)
        formatted_date = format_date_input(args.date)
        update_expense(args.index, args.description, args.amount, formatted_date)

    elif args.action == 'delete':
        if not args.index:
            print("Error: --index is required for deleting expenses")
            sys.exit(1)
        delete_expense(args.index)

    elif args.action == 'summary':
        if args.month:
            view_summary_month(args.month)
        else:
            view_summary()

    elif args.action == 'export':
        if not args.output:
            print("Error: --output is required for exporting expenses")
            sys.exit(1)
        try:
            with open(args.output, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Description', 'Amount', 'Date'])
                for expense in expenses:
                    writer.writerow([expense['description'], expense['amount'], expense['date']])
            print(f"Expenses exported successfully to {args.output}")
        except Exception as e:
            print(f"Error exporting expenses: {e}")

if __name__ == "__main__":
    main()
                
    
