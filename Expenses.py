import argparse
from datetime import datetime


expenses = []

def validate_date(date_str):
    try:
        # Try to parse the date in MM-DD-YYYY format
        datetime.strptime(date_str, '%m-%d-%Y')
        return True
    except ValueError:
        return False

print ("Expenses")

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

def update_expense(index, description, amount):
    if index < 1 or index > len(expenses):
        print("Invalid expense index.")
        return
    try:
        amount = int(amount)
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    index = int(index)
    expenses[index-1] = {"description": description, "amount": float(amount)}
    print(f"Updated expense {index}: {description} - ${amount}")

def delete_expense(index):
    print(f"Deleted expense {index}")
    
def view_summary():
    print("Summary:")

def export_expenses():
    print("Exporting expenses to expenses.csv")

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
            date = input("Enter expense date (MM-DD-YYYY): ")
            add_expense(description, amount, date)
        elif choice == "2":
            print ("View Expenses:")
            view_expenses()
        elif choice == "3":
            print ("Update Expense:")
            index = int(input("Enter the index of the expense to update: "))
            description = input("Enter new description: ")
            amount = input("Enter new amount: $")
            update_expense(index, description, amount)
        elif choice == "4":
            print ("Delete Expense:")
            index = int(input("Enter the index of the expense to delete: "))
            delete_expense(index)
        elif choice == "5":
            print ("View Summary:") 
            view_summary()
        elif choice == "6":
            print ("Export Expenses:")
            export_expenses()
        elif choice == "7":
            print ("Exiting...")
            break
            
if __name__ == "__main__":
    main()
                
    
