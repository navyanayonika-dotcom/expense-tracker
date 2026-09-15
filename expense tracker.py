import csv
import os
from datetime import datetime
file_name='expenses.csv'
def create_file():
    if not os.path.exists(file_name):
        with open(file_name,'w',newline='') as file:
            writer=csv.writer(file)
            writer.writerow(
                ['Date','Category','Amount','Description']
            )


def display_menu():
    print('\n=======MENU=======')
    print('1.Set Budget')
    print('2.Add Expense')
    print('3.View Expense')
    print('4.Search Expense')
    print('5.Delete Expense')
    print('6.Generate Report')
    print('7.Exit')


def main():
    
    create_file()

    while True:
        display_menu()
        choice=input('What do you wish to do today?Enter your choice(1-5) ')
        if choice=='1':
            set_budget()
        elif choice=='2':
            add_expense()
        elif choice=='3':
            view_expense()
        elif choice=='4':
            search_expense()
        elif choice=='5':
            delete_expense()
        elif choice=='6':
            generate_report()
        elif choice=='7':
            print('Thank you for using Expense Tracker.')
            print('Have a great day!☺️')
            break
        else:
            print('Invalid Choice!')

budget=0


def add_expense():
    while True:
        try:
            amount=float(input('Enter Amount: '))
            if amount<=0:
                print('Amount must be greater than zero.')
                continue
            break
        except ValueError:
            print('Please enter valid amount: ')
    category=input('Enter Category of expense: ').title()
    description=input('Describe your expense: ').title()
    date = datetime.now().strftime("%d-%m-%Y")
    with open(file_name, "a", newline='') as file:
        writer=csv.writer(file)
        writer.writerow([
            date,
            category,
            amount,
            description
])
    print("\nExpense Added Successfully!")     


def view_expense():
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader)
        print("\n========== ALL EXPENSES ==========")
        print(f"{'No.':<5}{'Date':<15}{'Category':<15}{'Amount':<12}{'Description'}")
        print("-" * 65)
        for index, row in enumerate(reader,start=1):
            print(f"{index:<5}{row[0]:<15}{row[1]:<15}₹{row[2]:<11}{row[3]}")
        print("-" * 65)


def search_expense():
    with open (file_name,'r') as file:
        reader=csv.reader(file)
        next(reader)
        search=input('Enter category to search: ').title()
        found=False
        for row in reader:
            if row[1]==search:
                print('\n----------------')
                print('Date:',row[0])
                print('Category:',row[1])
                print('Amount:Rs.',row[2])
                print('Description:',row[3])

                found=True
        if not found:
            print('No expense found.')


def delete_expense():
    with open(file_name,'r') as file:
        reader=csv.reader(file)
        rows=list(reader)

    if len(rows)==1:
        print('No expenses to delete.')
        return

    print('\n-------------EXPENSES---------------\n')
    print(f"{'No.':<5}{'Date':<15}{'Category':<15}{'Amount':<12}{'Description'}")  
    print('-'*65)

    for i in range(1,len(rows)):
        row=rows[i]
        print(f"{i:<5}{row[0]:<15}{row[1]:<15}₹{row[2]:<11}{row[3]}")

    while True:
        try:
            choice=int(input('\nEnter expense number to delete: '))
            if 1<= choice<len(rows):
                break
            print('INVALID EXPENSE NUMBER.')

        except ValueError:
            print('Please enter a number.')
    confirm=input('Are you sure you want to delete this?(YES/NO): ').upper()

    if confirm=='YES':
        del rows[choice]

        with open(file_name,'w',newline="") as file:
            writer=csv.writer(file)
            writer.writerows(rows)

        print('\nExpense deleted successfully.')
    else:
        print('\nDeletion cancelled.')


def generate_report():
    with open(file_name,'r') as file:
        reader=csv.reader(file)
        next(reader)

        total=0
        expense_count=0
        category_total={}
        highest_amt=0
        highest_row=None


        for row in reader:
            amount=float(row[2])
            total+=amount
            expense_count+=1

            category=row[1]
            if category in category_total:
                category_total[category]+=amount
            else:
                category_total[category]=amount

            if amount > highest_amt:
                highest_amt = amount
                highest_row = row

        print("\n=============EXPENSE REPORT==============")
        print(f'Total Expenses:Rs.{total:.2f}')

        if budget>0:
            remaining=budget-total

            print(f'Budget: Rs. {budget:.2f}')
            print(f'Remaining: Rs.{remaining:.2f}')

            if total>budget:

                print('''\n⚠ WARNING!\nYou have exceeded your monthly budget!
''')
            elif total>=budget*0.8:
                print('''\n⚠ WARNING!\nYou have used more than 80% of your budget.
''')
            else:
                print('\nYou are within your budget✅')


        print(f'Total number of Expenses: {expense_count}')

        print('\n-------------Category Wise Spending-----------------')
        for category,amount in category_total.items():
            print(f'{category:<15} Rs.{amount:.2f}')

        if highest_row is not None:
            print('\n------------HIGHEST EXPENSE---------------')
            print(f"Date        : {highest_row[0]}")
            print(f"Category    : {highest_row[1]}")
            print(f"Amount      : ₹{highest_row[2]}")
            print(f"Description : {highest_row[3]}")
        else:
            print('\nNo expense found.')


def set_budget():
    global budget

    while True:
        try:
            budget=float(input('Enter Monthly Budget: '))
            if budget<=0:
                print('Budget must be greater than zero,')
                continue

            print(f'Budget set to Rs. {budget:.2f}')
            break
        except ValueError:
            print('Please enter a valid amount.')


if __name__ == "__main__":
    main()
