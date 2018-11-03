from utils import *


class Seat:
    def __init__(self, row=A, column=1):
        self.row = row
        self.column = column
        self.type = get_seat_type(row, column)
        self.cost = get_seat_cost(row, column)
        self.is_reserved = False
        self.is_paid_for = False

    def is_taken(self):
        return self.is_reserved and self.is_paid_for

    def reserve(self):
        self.is_reserved = True

    def pay(self):
        self.is_reserved = True
        self.is_paid_for = True

    def unreserve(self):
        self.is_reserved = False

    def __str__(self):
        string = ""

        if self.is_taken():
            string += '#'
        elif self.is_reserved:
            string += 'o'
        else:
            string += '*'

        return color(string.center(4), self.type)
