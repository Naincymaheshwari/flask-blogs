import random
import string


def password_generator():
    length = 8
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
