import random

from epub import Epub
from space import Space
from lineorder import LineOrder


randomizer = random.SystemRandom()
HEADER_BIT_SIZE = 5
CHAR_BIT_SIZE = 8


def add_noise(space):
    for i in range(0, len(space)):
        space[i] = randomizer.randint(0, 1)


def store(key, message, in_path, out_path):
    epub = Epub()
    epub.expand(in_path)
    space = Space(epub)

    binary_message = ''.join([format(ord(x), '0'+str(CHAR_BIT_SIZE)+'b') for x in message])
    message_size = format(len(binary_message), 'b')
    header_size = format(len(message_size), '0'+str(HEADER_BIT_SIZE)+'b')

    bits_to_write = header_size + message_size + binary_message

    if (len(space)) < len(bits_to_write):
        print 'Error, not enough space on the epub file'

    line_order = LineOrder(key, len(space))

    add_noise(space)

    for bit in bits_to_write:
        space[line_order.next()] = (bit == '1')

    space.commit()
    epub.contract(out_path)


def retrieve(key, path):
    epub = Epub()
    epub.expand(path)
    space = Space(epub)

    line_order = LineOrder(key, len(space))

    def read_int(bit_size):
        bit_buffer = ''

        for i in range(bit_size):
            if space[line_order.next()]:
                bit_buffer += '1'
            else:
                bit_buffer += '0'

        return int(bit_buffer, 2)

    header_size = read_int(HEADER_BIT_SIZE)
    message_size = read_int(header_size)

    message = ''
    for i in range(0, message_size, CHAR_BIT_SIZE):
        message += chr(read_int(CHAR_BIT_SIZE))

    epub.cleanup()

    return message
