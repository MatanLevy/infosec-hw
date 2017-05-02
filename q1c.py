import os, sys


PATH_TO_SUDO = './sudo'


def get_arg():
    raise NotImplementedError()


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)
