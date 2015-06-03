import sys

from argparse import ArgumentParser

import steganography


def store():
    parser = ArgumentParser(description='Hide a message inside the epub file')
    parser.add_argument('key', help='Stego-key')
    parser.add_argument('message', help='Message to store')
    parser.add_argument('input_epub', help='Path to the input epub')
    parser.add_argument('output_epub', help='Path of the output epub, containing the message')
    args = parser.parse_args(sys.argv[2:])

    print '\nInserting message\n'
    steganography.store(args.key, args.message, args.input_epub, args.output_epub)


def retrieve():
    parser = ArgumentParser(description='Retrieve a message from the epub file')
    parser.add_argument('key', help='Stego-key')
    parser.add_argument('input_epub', help='Path to the epub')
    args = parser.parse_args(sys.argv[2:])

    try:
        print '\nExtracted message: "' + steganography.retrieve(args.key, args.input_epub) + '"\n'
    except:
        print '\nError extracting message. Wrong stego-key?\n'


if __name__ == '__main__':
    parser = ArgumentParser(
    description='Tool that hides/extract steganographic messages from inside EPUB files',
    usage='''main.py <command> <args>

There are two commands available:
    store       Store a message inside the epub
    retrieve    Retrieve a message from the epub''')

    parser.add_argument('command', help='Command to execute')

    args = parser.parse_args(sys.argv[1:2])

    if args.command == 'store':
        store()
    elif args.command == 'retrieve':
        retrieve()
    else:
        print 'Unrecognized command'
        parser.print_help()
