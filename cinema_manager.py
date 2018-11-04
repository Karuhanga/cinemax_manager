"""Cinemax theatre manager- manage your cinema with this easy to use app"""
from models import *

OPTIONS_MESSAGE = "What would you like to do?\n1. Buy a seat\n2. Reserve seat\n3. Pay for reserved seat\n4. Reset seating plan\n5. See current seating plan\n6. Cancel reservation\n7. Exit\n"
seating_plan = []


def get_total_sales():
    total_sales = 0
    for row in seating_plan:
        for seat in row:
            total_sales += seat.cost if seat.is_taken() else 0
    return total_sales


def print_seating_assignment():
    """ print out the current seating status """

    print()
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
    print("SCREEN")
    print("Number of seats available: {}".format(get_number_of_seats_left()))
    print("Total sales: UgShs. {}".format(get_total_sales()))
    print()


def get_seat(seat):
    for row in seating_plan:
        for column in row:
            if seat == column.name:
                return column


def pay_for_reserved_seat():
    # make a payment for a reserved seat
    print("\n\nMake payment")
    there_are_reserved_seats = print_reserved_seats()
    if not there_are_reserved_seats:
        print("There are no reserved seats\n\n")
        return
    seat = input_seat(message="Select seat:\t")
    seat = get_seat(seat)
    while (not seat) or seat.is_paid_for or (not seat.is_reserved):
        print("You can't pay for this seat")
        seat = input_seat(message="Select seat:\t")
        seat = get_seat(seat)
    seat.pay()
    print("Done.\n")


def reset_seating_plan():
    """ reset the seating plan """
    global seating_plan
    seating_plan = [[Seat(row=row, column=column) for column in tuple(range(1, 21))] for row in ROWS]


def buy_seat():
    """ assign a person a seat """
    print("\n\nBuy seats:")
    seats = pick_seats()

    if seats:
        print("Selected seats: ", end='')
        for seat in seats:
            seat.pay()
            print(seat.name, end='. ')
        print("\nPayment done.\n\n")
    else:
        print("No seats selected for purchase.")

    choice = get_option("Would you like to buy more seats?:\n1. Yes\n2. No\n", options=(1, 2))
    if choice is 1:
        return buy_seat()
    return print_seating_assignment()


def get_number_of_seats_left(category=None):
    if category:
        seats_left_in_category = 0
        for row in seating_plan:
            for seat in row:
                seats_left_in_category += 1 if not seat.is_reserved and seat.type is category else 0
        return seats_left_in_category
    seats_left = 0
    for row in seating_plan:
        for seat in row:
            seats_left += 1 if not seat.is_reserved else 0
    return seats_left


def print_available_seats(seat_count, category):
    """ prints out available seat ranges of a given category """
    print("\nAvailable seats:")
    new_line = False
    there_are_seats = False
    for row in seating_plan:
        for seat in row:
            if seat.type is category:
                new_line = True
                if not seat.is_reserved:
                    there_are_seats = True
                    print(seat.get_name(), end='')
                else:
                    print(''.center(5), end='')
        if new_line:
            print()
            new_line = False
    if there_are_seats:
        print(
            "{category} seats are UgShs. {price} each.".format(category=category, price=get_all_seat_costs()[category]))
    print()
    return there_are_seats


def print_reserved_seats():
    """ prints out reserved seats """
    print("Reserved seats:")
    new_line = False
    there_are_reserved_seats = False
    for row in seating_plan:
        for seat in row:
            if seat.is_reserved and not seat.is_taken():
                new_line = True
                there_are_reserved_seats = True
                print(seat.get_name(), end='')
        if new_line:
            print()
            new_line = False
    print()
    return there_are_reserved_seats


def enough_seats_in_row(seats_required, starting_at, category):
    starting_at = list(starting_at)
    row = ord(starting_at[0]) - 65
    column = int(''.join(starting_at[1:])) - 1

    seats = seating_plan[row][column:column + seats_required]
    if len(seats) < seats_required:
        return False
    for seat in seats:
        if (seat.type is not category) or seat.is_reserved:
            return False
    return True


def get_seats(seats_required, starting_at):
    starting_at = list(starting_at)
    row = ord(starting_at[0]) - 65
    column = int(''.join(starting_at[1:])) - 1

    return seating_plan[row][column:column + seats_required]


def in_category(seat, category):
    seat = list(seat)
    seat[0] = ord(seat[0]) - 65
    seat[1] = int(seat[1]) - 1
    return seating_plan[seat[0]][seat[1]].type is category


def pick_seats():
    seats_left = get_number_of_seats_left()
    if seats_left is 0:
        print("There are no more seats left.")
        return

    category = get_option(message="Desired seat category:\n1. Economy\n2. VIP\n3. VVIP\n4. Twin\n",
                          options=[1, 2, 3, 4])
    if category is 1:
        category = Economy
    elif category is 2:
        category = VIP
    elif category is 3:
        category = VVIP
    else:
        category = Twin

    seats_left_in_category = get_number_of_seats_left(category=category)
    if seats_left_in_category is 0:
        print("There are no more seats left in the {category} category.".format(category=category))
        return

    message = "Enter number of seats required:\t" if category is not Twin else "Enter number of couples:\t"
    seat_count = get_int(message=message)
    while seat_count > seats_left_in_category:
        print("There's only {seats_left_in_category} seats left in the {category} category.".format(
            seats_left_in_category=seats_left_in_category, category=category))
        seat_count = get_int(message=message)

    seat_count = seat_count if category is not Twin else seat_count * 2

    there_are_seats = print_available_seats(seat_count, category)

    if not there_are_seats:
        print("No seats available. Please try again.")
        return

    seat = input_seat(message="Choose seat:\t")

    while not (in_category(seat, category) and enough_seats_in_row(seats_required=seat_count, starting_at=seat,
                                                                   category=category)):
        print(
            "Can't select this seat. It is either taken or there are not enough seats of this category left starting at this seat")
        choice = get_option(message="1. Pick another starting seat\n2. Break down the number of seats\n3. Cancel\n",
                            options=(1, 2, 3))
        if choice is 1:
            seat = input_seat(message="Choose seat:\t")
        elif choice is 2:
            return pick_seats()
        else:
            return []

    return get_seats(seats_required=seat_count, starting_at=seat)


def reserve_seat():
    """ assign a person a seat """
    print("\n\nReserve seats:")
    seats = pick_seats()
    if seats:
        print("Selected seats: ", end='')
        for seat in seats:
            seat.reserve()
            print(seat.name, end='. ')
        print("\nReservation done.\n\n")
    else:
        print("No seats selected for reservation.")

    choice = get_option("Would you like to reserve more seats?:\n1. Yes\n2. No\n", options=(1, 2))
    if choice is 1:
        return reserve_seat()
    return print_seating_assignment()


def cancel_reservation():
    """ unreserve a seat """
    print("\n\nCancel reservation")
    there_are_reserved_seats = print_reserved_seats()
    if not there_are_reserved_seats:
        print("There are no reserved seats\n\n")
        return
    seat = input_seat(message="Select seat:\t")
    seat = get_seat(seat)
    while (not seat) or seat.is_paid_for or (not seat.is_reserved):
        print("You can't cancel this reservation. Ensure it is not already paid for and is reserved")
        seat = input_seat(message="Select seat:\t")
        seat = get_seat(seat)
    seat.unreserve()
    print("Reservation cancelled.\n")


def present_options():
    option = get_option(message=OPTIONS_MESSAGE, options=(1, 2, 3, 4, 5, 6, 7))
    if option is 1:
        buy_seat()
    elif option is 2:
        reserve_seat()
    elif option is 3:
        pay_for_reserved_seat()
    elif option is 4:
        print("\n\nResetting seating plan...")
        reset_seating_plan()
        print("Done.\n\n")
    elif option is 5:
        print("\n\nPrinting assignment...\n")
        print_seating_assignment()
        print("\nDone.\n\n")
    elif option is 6:
        cancel_reservation()
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
