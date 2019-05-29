#!/usr/bin/env python

import random


letters = ["T", "R", "W", "A", "G", "M", "Y", "F", "P", "D", "X", "B", "N", "J", "Z", "S", "Q", "V", "H", "L", "C", "K", "E", ]
foreign = ["X", "Y", "Z"]


class InvalidPinError(Exception):
    """When the generated PIN is incorrect."""
    pass


class DNI(object):

    @staticmethod
    def validate(pin):
        if len(pin) != 9:
            raise InvalidPinError("Must be 9 digits long: %s" % (pin))

        check_digit = pin[8]
        pin = pin[:8]

        # If it's a foreign PIN number, replace X/Y/Z by 0/1/2
        if pin[0] in foreign:
            pin = pin.replace(pin[0], str(foreign.index(pin[0])))

        return check_digit == letters[int(pin) % 23]

    @property
    def value(self):
        pin_type = [
            self.national,
            self.foreign,
        ]

        pin = random.choice(pin_type)()
        if DNI.validate(pin):
            return pin

    def national(self):
        dni = str(random.randint(0, 9999999)).zfill(8)
        check_digit = int(dni) % 23
        return dni + letters[check_digit]

    def foreign(self):
        # Pick a letter at random
        letter = foreign.index(random.choice(foreign))

        # Generate a DNI with one less digit, we'll append
        # the letter we just picked
        dni = str(random.randint(0, 9999999)).zfill(7)
        numeric_nie = int(str(letter) + dni)

        # Obtain the check digit
        check_digit = numeric_nie % 23

        return foreign[letter] + dni + letters[check_digit]


if __name__ == '__main__':
    random.seed(0)
    for x in range(1000):
        print DNI().value

