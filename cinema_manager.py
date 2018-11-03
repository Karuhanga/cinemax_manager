"""Cinemax theatre manager- manage your cinema with this easy to use app"""
from models import *

STARTING_MESSAGE = "What would you like to do?\n1. Seat assignment\n2. Make payments\n3. Reset seating plan\n4. See current seating plan\n5. Exit\n"
seating_plan = None


def print_seating_assignment():
    """ print out the current seating status """

    for column_label in range(0, 21):
        if column_label is 0:
            print(str('').center(4), end='')
        else:
            print(str(column_label).center(4), end='')
    print()
    for row, row_label in zip(seating_plan, ROWS):
        print(row_label.center(4), end='')
        for seat in row:
            print(seat, end='')
        print()


def make_payment():
    # make a payment for a reserved seat # todo
    print("\n\nMake payment\n\n")


def reset_seating_plan():
    """ reset the seating plan todo """
    global seating_plan
    seating_plan = [[Seat(row=row, column=column) for column in tuple(range(1, 21))] for row in ROWS]


def assign_seat():
    """ assign a person a seat todo """
    print("\n\nAssign seat\n\n")


def present_options():
    option = get_option(message=STARTING_MESSAGE, options=(1, 2, 3, 4, 5))
    if option is 1:
        assign_seat()
    elif option is 2:
        make_payment()
    elif option is 3:
        print("\n\nResetting seating plan...")
        reset_seating_plan()
        print("Done.\n\n")
    elif option is 4:
        print("\n\nPrinting assignment...\n")
        print_seating_assignment()
        print("\nDone.\n\n")
    else:
        print("Goodbye.")
        return
    present_options()


def run():
    print("Welcome to Cinemax Manager")
    reset_seating_plan()
    print_seating_assignment()
    present_options()


if __name__ == '__main__':
    run()
