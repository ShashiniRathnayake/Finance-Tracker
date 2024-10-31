# import libraries

import calendar
import datetime
import os
import pandas as pd

# call class as transaction

class Transaction:
    def __init__(self, name, amount, category, transaction_type, date):
        self.name = name
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date

    def __str__(self):
        return f"{self.name} - Rs.{self.amount:.2f} ({self.category}) on {self.date} ({self.transaction_type})"

# Create a function name create_transactions_file

def create_transactions_file(transactions_file_path):
    if not os.path.exists(transactions_file_path):
        with open(transactions_file_path, "w", encoding='utf-8'):
            pass

# Create a function as record_transaction
def record_transaction(transaction_type, transactions_file_path):
    print(f"🎯 Recording {transaction_type.capitalize()}")
    transaction_name = input("Enter Item name: ")
    transaction_amount_str = input("Enter Item amount: ")

    try:
        transaction_amount = float(transaction_amount_str)
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return

    transaction_category = input("Enter Item category: ")
    transaction_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_transaction = Transaction(
        name=transaction_name,
        amount=transaction_amount,
        category=transaction_category,
        transaction_type=transaction_type,
        date=transaction_date
    )

    save_transaction_to_file(new_transaction, transactions_file_path)
    print(f"{transaction_type.capitalize()} recorded successfully.")

#Create a Function named save-transtation_to_file
def save_transaction_to_file(transaction, transactions_file_path):
    print(f"🎯 Saving Transaction: {transaction} to {transactions_file_path}")
    with open(transactions_file_path, "a", encoding='utf-8') as f:
        f.write(f"{transaction.name},{transaction.amount},{transaction.category},{transaction.transaction_type},{transaction.date}\n")

#Create a funtion to view_monthly_summary
def view_monthly_summary(transactions_file_path, budget):
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    view_summary_for_month(transactions_file_path, budget, month, year, "Monthly")

#Create a funtion to view_daily_summary
def view_daily_summary(transactions_file_path, budget):
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    view_summary_for_day(transactions_file_path, budget, day, month, year, "Daily")

#call a function to summarize specific month
def view_summary_for_month(transactions_file_path, budget, month, year, summary_type):
    print(f"🎯 {summary_type} Summary for {calendar.month_name[month]} {year}")

    transactions = load_transactions(transactions_file_path)
    filtered_transactions = filter_transactions_by_month(transactions, month, year)

    summarize_transactions(filtered_transactions, budget)

#call a function to summarize specific day
def view_summary_for_day(transactions_file_path, budget, day, month, year, summary_type):
    print(f"🎯 {summary_type} Summary for {day}-{month}-{year}")

    transactions = load_transactions(transactions_file_path)
    filtered_transactions = filter_transactions_by_day(transactions, day, month, year)

    summarize_transactions(filtered_transactions, budget)

#create a function to load_transactions 
def load_transactions(transactions_file_path):
    transactions = []
    with open(transactions_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            transaction_data = line.strip().split(",")
            
            if len(transaction_data) >= 3:  
                name, amount, category = transaction_data[:3]
                transaction = Transaction(
                    name=name,
                    amount=float(amount),
                    category=category,
                    transaction_type=None,
                    date=None
                )

                if len(transaction_data) == 5:
                    transaction.transaction_type = transaction_data[3]
                    transaction.date = transaction_data[4]

                transactions.append(transaction)
            else:
                print(f"Irregular line format: {line}")

    return transactions

def filter_transactions_by_month(transactions, month, year):
    return [t for t in transactions if t.date and
            datetime.datetime.strptime(t.date, '%Y-%m-%d %H:%M:%S').month == month and
            datetime.datetime.strptime(t.date, '%Y-%m-%d %H:%M:%S').year == year]

def filter_transactions_by_day(transactions, day, month, year):
    return [
        t for t in transactions if t.date and
        datetime.datetime.strptime(t.date, '%Y-%m-%d %H:%M:%S').day == day and
        datetime.datetime.strptime(t.date, '%Y-%m-%d %H:%M:%S').month == month and
        datetime.datetime.strptime(t.date, '%Y-%m-%d %H:%M:%S').year == year
    ]

#Function to Summarize transaction
def summarize_transactions(transactions, budget):
    amount_by_category = {"expense": 0, "income": 0}

    for transaction in transactions:
        key = transaction.transaction_type
        amount_by_category[key] += transaction.amount

    print("Expenses By Category 📈:")
    print(f"  Total Expenses: Rs.{amount_by_category['expense']:.2f}")

    total_spent = amount_by_category["expense"]
    total_income = amount_by_category["income"]

    print(f"\n💵 Total Expenses: Rs.{total_spent:.2f}")
    print(f"💰 Total Income: Rs.{total_income:.2f}")

    remaining_budget = budget + total_income - total_spent
    print(f"✅ Budget Remaining: Rs.{remaining_budget:.2f}")

#Function to view all entries
def view_all_entries(transactions_file_path):
    print("📜 All Entries:")
    transactions = load_transactions(transactions_file_path)

    for i, transaction in enumerate(transactions, start=1):
        print(f"{i}. {transaction}")

#function to save_data_to_file
def save_data_to_file(transactions_file_path):
    transactions = load_transactions(transactions_file_path)
    existing_transactions = set((transaction.name, transaction.amount, transaction.category, transaction.transaction_type, transaction.date) for transaction in transactions)

    new_transactions = [transaction for transaction in transactions if
                        (transaction.name, transaction.amount, transaction.category, transaction.transaction_type, transaction.date) not in existing_transactions]

    if new_transactions:
        save_transactions_to_file(new_transactions, transactions_file_path)
        print("Data saved to file.")
    else:
        print("No new transactions to save.")

def save_transactions_to_file(transactions, transactions_file_path):
    with open(transactions_file_path, "a", encoding='utf-8') as f:
        for transaction in transactions:
            f.write(f"{transaction.name},{transaction.amount},{transaction.category},{transaction.transaction_type},{transaction.date}\n")

def csv_to_excel(csv_file, excel_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Write DataFrame to an Excel file
    df.to_excel(excel_file, index=False)

# Specify the paths for your CSV and Excel files
csv_file_path = 'transactions.csv'
excel_file_path = 'transactions.xlsx'

# Convert CSV to Excel
csv_to_excel(csv_file_path, excel_file_path)

print(f'Conversion from CSV to Excel completed. Excel file saved at: {excel_file_path}')

#main function

def main():
    print("🎯 Running Finance Tracker!")
    transactions_file_path = "transactions.csv"
    budget = 2000

    create_transactions_file(transactions_file_path)

    while True:
        # Calculate total income, total expense, and budget remaining
        transactions = load_transactions(transactions_file_path)
        total_income, total_expense, budget_remaining = calculate_summary(transactions, budget)

        print("\n1. Record Expense")
        print("2. Record Income")
        print("3. View Monthly Summary")
        print("4. View Daily Summary")
        print("5. View All Entries")
        print("6. Save Data to File")
        print("7. Display Totals")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            record_transaction("expense", transactions_file_path)
        elif choice == "2":
            record_transaction("income", transactions_file_path)
        elif choice == "3":
            view_monthly_summary(transactions_file_path, budget)
        elif choice == "4":
            view_daily_summary(transactions_file_path, budget)
        elif choice == "5":
            view_all_entries(transactions_file_path)
        elif choice == "6":
            save_data_to_file(transactions_file_path)
        elif choice == "7":
            print_summary(total_income, total_expense, budget_remaining)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

def calculate_summary(transactions, budget):
    total_income = sum(transaction.amount for transaction in transactions if transaction.transaction_type == "income")
    total_expense = sum(transaction.amount for transaction in transactions if transaction.transaction_type == "expense")
    budget_remaining = budget + total_income - total_expense
    return total_income, total_expense, budget_remaining

def print_summary(total_income, total_expense, budget_remaining):
    print("\n💰 Totals Summary:")
    print(f"  Total Income: Rs.{total_income:.2f}")
    print(f"  Total Expense: Rs.{total_expense:.2f}")
    print(f"  Budget Remaining: Rs.{budget_remaining:.2f}")

if __name__ == "__main__":
    main()
