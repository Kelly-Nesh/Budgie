#!/usr/bin/env python3
import sqlite3 as sq
import sys

"""Budget Manager"""

balance = 0


def budgie_db():
    conn = sq.connect("budgie.sqlite3")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS budget (name VARCHAR(20) primary key)")
    cur.execute("""CREATE TABLE IF NOT EXISTS sections (budget_name varchar(25),
                name varchar(30),
                percentage integer,
                part varchar(1),
                foreign key(budget_name) references budget(name));""")
    return [conn, cur]


conn, cur = budgie_db()


def main():
    print("Welcome to Budgie.")
    msg = "Enter number to choose an option from below\n" \
          "1. Create new budget\n" \
          "2. Use existing budget\n" \
          "3. Edit budget\n" \
          "4. Quit\n "
    actions = {"1": create_budget, "2": choose_budget, "3": edit_budget,
               "4": sys.exit}
    while True:
        choice = input(msg)
        if choice not in actions:
            print("Wrong inputs. Try again")
            continue
        actions[choice]()


def create_budget():
    """Create a new budget"""
    while True:
        budget_name = input("Enter budget name: ")
        if len(budget_name) >= 20:
            print("Budget name should be less than 20 characters")
            continue
        elif not budget_name.isalnum():
            print("Budget name should can only contain alphabets and/or numbers")
            continue
        else:
            dbExists = cur.execute("SELECT name FROM budget where name='{}'".format(budget_name))
            if dbExists.fetchone():
                print("Database with the name `{}` already exists".format(budget_name))
            else:
                cur.execute("INSERT INTO budget values ('{}')".format(budget_name))
                conn.commit()
                create_sections(budget_name)
                break


def create_sections(budg_name):
    """Create sections for the budget newly created
    Args:
        budg_name (str): the name of the new budget
    """
    quit = ""
    while not quit or quit == "y":
        while True:
            section_name = input("Input section name: ")
            if not section_name.isalpha():
                print("Section name must only contain alphabets")
                continue
            break
        while True:
            section_percentage = input("Percentage to spend on section: ")
            if not section_percentage.isnumeric():
                print("Percentage should be numbers only")
                continue
            if int(section_percentage) > 100:
                print("Maximum of 100 exceeded")
                continue
            break
        while True:
            optns = ["t", "r"]
            section_part = input("Percentage of remainder or total (t/r): ")
            if not section_part.isalpha() or section_part not in optns:
                print("Use `t` for percentage over total or `r` for percentage over remainder only")
                continue
            break
        cur.execute("INSERT INTO sections (budget_name, name, percentage, part) VALUES"
                    " ('{}', '{}', '{}', '{}')".format(budg_name, section_name, section_percentage,
                                                       section_part))
        conn.commit()
        quit = input("\nAdd another section? (y / n): ")


def edit_budget():
    pass


def choose_budget():
    """Choose budget to use from the existing ones"""
    print("Choose budget to use: ")
    saved_budgets = cur.execute("SELECT name from budget").fetchall()
    for n, b in enumerate(saved_budgets):
        print("{}: {}".format(n, b[0]))
    while True:
        chosen_budget = input("")
        if chosen_budget == "q":
            break
        try:
            budget = saved_budgets[int(chosen_budget)]
        except (IndexError, TypeError, ValueError):
            print("Wrong input. Try again\nUse budget numbers")
            continue
        else:
            break
    sects = cur.execute("""select sections.name, sections.percentage, sections.part
                        from sections where budget_name='{}'""".format(budget[0])).fetchall()
    use_budget(sects, budget[0])


def use_budget(budget: list, budget_name: str):
    while True:
        try:
            amount = int(input("Enter amount to budget: "))
        except TypeError:
            print("Amount should be numbers only")
        else:
            break
    final_budget = budget_calc(amount, budget)
    budget_display(amount, final_budget, budget_name)


def budget_calc(amount: int, budget: list) -> dict:
    """Calculate budget section amounts based on percentage and part
    [('tithe', 10, 't'), ('offering', 5, 't'), ('lts', 5, 't'),
    ('ns', 15, 't'), ('needs', 70, 'r'), ('wants', 30, 'r')]"""
    spent = 0
    budget_results = {}
    for section in budget:
        if section[2] == "t":
            section_amount = int((int(section[1]) / 100) * amount)
            spent += section_amount
            if amount - spent < 0:
                print("Amount fully budgeted")
                break
            budget_results[section[0]] = section_amount
    amount = amount - spent
    if amount > 0:
        for section in budget:
            if section[2] == 'r':
                section_amount = int(int(section[1]) * amount / 100)
                if amount < 0:
                    print("Amount fully budgeted")
                    break
                budget_results[section[0]] = section_amount
    return budget_results


def budget_display(total_amt: str, budget: dict, budget_name: str):
    print(budget_name)
    spending = 0
    print("{}\t\t{}".format("Section", "Amount"))
    for sect, amt in budget.items():
        spending += amt
        print("{}\t\t{}".format(sect, amt))
    print("{}\t\t{}".format("balance", int(total_amt) - spending))

if __name__ == "__main__":
    main()
