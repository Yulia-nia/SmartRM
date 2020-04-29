import argparse
from removal.smartrm import SmartRM

parser = argparse.ArgumentParser(prog='SmartRM project for deleting files')
parser.add_argument('-r', '--remove',  help='Delete file to trash')
parser.add_argument('-rt', '--removetrash', help='Delete file from trash')
parser.add_argument('-c', '--clear', help='Clear trash')
parser.add_argument('-i', '--info', help='Show info about trash')


def main():
    smartRM = SmartRM()
    args = parser.parse_args()

    if args.remove:
        smartRM.remove(args.path)
    elif args.removetrash:
        smartRM.remove_file_in_trash(args.path)
    elif args.clear:
        smartRM.clear_trash()
    elif args.info:
        print(smartRM.get_trash_information())


if __name__ == '__main__':
    main()

