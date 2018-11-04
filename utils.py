A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
ROWS = (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P)

Economy = 'Economy'
VIP = 'VIP'
VVIP = 'VVIP'
Twin = 'Twin'

SEAT_COSTS = {}


def load_seat_costs():
    seat_costs = {}
    with open('prices.txt', 'r') as file:
        for line in file:
            line = line.split('-')
            seat_costs[line[0]] = int(line[1])
    return seat_costs


def get_all_seat_costs():
    global SEAT_COSTS
    if not SEAT_COSTS:
        SEAT_COSTS = load_seat_costs()
    return SEAT_COSTS


def get_seat_cost(row, column):
    """get the cost of a particular seat"""
    seat_costs = get_all_seat_costs()

    return seat_costs[get_seat_type(row, column)]


def get_seat_type(row, column):
    """get the type of a particular seat"""

    # columns M - P are economy seats
    if row in (M, N, O, P):
        return Economy

    # columns G - L are vip seats
    elif row in (G, H, I, J, K, L):
        return VIP

    # columns C - F are vvip seats
    elif row in (C, D, E, F):
        return VVIP

    # columns 5 - 15 of A and B are twins
    elif column in (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
        return Twin

    # the rest are all vvip seats
    return VVIP


def get_option(message, options):
    option = input(message)
    while not (option.isdigit() and int(option) in options):
        print("Please pick a valid option")
        option = input(message)
    return int(option)


def get_int(message):
    number = input(message)
    while (not number.isdigit()) or int(number) is 0:
        print("Please input a valid number.")
        number = input(message)
    return int(number)


def seat_is_valid(seat):
    if len(seat) not in (2, 3):
        return False
    seat = list(seat)
    seat[0] = seat[0].upper()
    if seat[0] not in ROWS:
        return False
    col = str(''.join(seat[1:]))
    if not col.isdigit():
        return False
    if int(col) not in tuple(range(1, 21)):
        return False
    return True


def input_seat(message):
    seat = input(message)
    if not seat_is_valid(seat):
        print("Please input a valid seat.")
        return input_seat(message)
    return seat.upper()


def color(string, seat_type):
    try:
        from colorclass import Color, Windows
        Windows.enable()
        if seat_type is Economy:
            return Color('{bgred}' + string + '{/bgred}')
        elif seat_type is VIP:
            return Color('{bgblue}' + string + '{/bgblue}')
        elif seat_type is VVIP:
            return Color('{bggreen}' + string + '{/bggreen}')
        elif seat_type is Twin:
            return Color('{bgmagenta}' + string + '{/bgmagenta}')
        else:
            return string
    except ModuleNotFoundError:
        return string
