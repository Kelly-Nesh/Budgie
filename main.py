#!/usr/bin/env python3
"""Budget Manager"""

budget_sectors = {}
total_amount = 0
balance = 0


def main():
    print("Welcome to Budgie\nEnter your budget sections/divisions")
    while True:
        section = input("Enter section name: ")
        percent = input("Enter section percent: ")
        total_or_rem = input("Enter `t` for percentage to be of total"
                             " or `r` for a percentage of the remainder: ")
        if section == "q" or percent == "q":
            break
        elif not section and not percent:
            amount = input("Enter amount to budget: ")
            break
        elif not section.isalpha():
            print("section name must only contain alphabet")
            continue
        elif not percent.isnumeric():
            print("section percent must only contain numbers")
            continue
        elif total_or_rem != 't' and total_or_rem != 'r':
            print("Choose either `t` for total or `r` for remainder")
            continue
        elif section and percent and total_or_rem:
            budget_sectors[section] = [percent, total_or_rem[0]]

    total_amount = amount
    budget_calc(amount)
    budget_display()


def budget_calc(amnt):
    div = 0
    of_total = 0
    amnt = int(amnt)
    for sect, perc in budget_sectors.items():
        if perc[1] == "t":
            if amnt - div <= 0:
                balance = amnt
                break
            div = int((int(perc[0]) / 100) * amnt)
            perc.append(div)
            of_total += div
    amnt -= of_total
    balance = amnt
    print(balance, 'of', total_amount)

    for sect, perc in budget_sectors.items():
        if perc[1] == "r":
            if amnt - div < 0:
                balance = amnt
                break
            div = int((int(perc[0]) / 100) * amnt)
            perc.append(div)
            of_total += div
    balance = amnt - of_total

def budget_display():
    print("{}\t{}\t{}\t{}".format("Section", "Percentage",
                                        "Total or remainder", "Amount"))
    for sect, perc in budget_sectors.items():
        print("{}\t\t{}\t\t{}\t\t{}".format(sect, perc[0], perc[1], perc[2]))
    print("Balance: {}\nTotal Amount: {}".format(total_amount, balance))


if __name__ == "__main__":
    main()