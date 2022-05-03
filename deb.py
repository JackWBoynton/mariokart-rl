

def add_address(x, y):
    """Returns a string representation of the sum of the two parameters.
    x is a hex string address that can be converted to an int.
    y is an int.
    """
    return "{0:08X}".format(int(x, 16) + y)



data = add_address('80453130', 0xE90 * 1)
print(data+ ' 70')