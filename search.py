import assemble
import string


GENERAL_REGISTERS = [
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
]


ALL_REGISTERS = GENERAL_REGISTERS + [
    'esp', 'eip', 'ebp'
]


class GadgetSearch(object):
    def __init__(self, dump_path, start_addr):
        """
        Construct the GadgetSearch object.

        Input:
            dump_path: The path to the memory dump file created with GDB.
            start_addr: The starting memory address of this dump.
        """
        self.dump = open(dump_path).read()
        self.start_addr = start_addr

    def get_format_count(self, gadget_format):
        """
        Get how many different register placeholders are in the pattern.
        
        Examples:
            self.get_format_count('POP ebx')
            => 0
            self.get_format_count('POP {0}')
            => 1
            self.get_format_count('XOR {0}, {0}; ADD {0}, {1}')
            => 2
        """
        # Hint: Use the string.Formatter().parse method:
        #   import string
        #   print string.Formatter().parse(gadget_format)
        import string
        it = iter(string.Formatter().parse(gadget_format))
        a = set()
        for i in it :
        	if (i[1] != None):
        		a.add(int(i[1]))
        return len(a)


    def get_register_combos(self, nregs, registers):
        """
        Return all the combinations of `registers` with `nregs` registers in
        each combination. Duplicates ARE allowed!

        Example:
            self.get_register_combos(2, ('eax', 'ebx'))
            => [['eax', 'eax'],
                ['eax', 'ebx'],
                ['ebx', 'eax'],
                ['ebx', 'ebx']]
        """
        import itertools
        return list(set(list(itertools.permutations(registers,nregs))+list(itertools.combinations_with_replacement(registers,nregs))))

    def format_all_gadgets(self, gadget_format, registers):
    	numberOfPlaces = self.get_format_count(gadget_format)
    	lst = self.get_register_combos(numberOfPlaces,registers)
    	arr = []
    	for elem in lst:
    		arr.append(gadget_format.format(*elem))
    	return arr	

        """
        Format all the possible gadgets for this format with the given
        registers.

        Example:
            self.format_all_gadgets("POP {0}; ADD {0}, {1}", ('eax', 'ecx'))
            => [['POP eax; ADD eax, eax'],
                ['POP eax; ADD eax, ecx'],
                ['POP ecx; ADD ecx, eax'],
                ['POP ecx; ADD ecx, ecx']]
        """
        # Hints:
        # 1. Use the format function:
        #    'Hi {0}! I am {1}, you are {0}'.format('Luke', 'Vader')
        #    => 'Hi Luke! I am Vader, you are Luke'
        # 2. You can use an array instead of specifying each argument. Use the
        #    internet, the force is strong with StackOverflow.
        
    def find_all(self, gadget):
        """
        Return all the addresses of the gadget inside the memory dump.

        Example:
            self.find_all('POP eax')
            => < all ABSOLUTE addresses in memory of 'POP eax; RET' >
        """
        # Notes:
        # 1. Addresses are ABSOLUTE (for example, 0x08403214), NOT RELATIVE to the
        #    beginning of the file (for example, 12).
        # 2. Don't forget to add the 'RET'
        opcode = assemble.assemble_data(gadget + '; RET')
        import re
        data = self.dump
        start = self.start_addr
        indices = []  #will be there all indexed of substring opcode in data
        index = 0
    	while (index < len(data)):  #find all substring equals opcode to data
    		index = data.find(opcode,index)
    		if index == -1:
    			break
    		indices.append(index)
    		index += len(opcode)
        address_list = []
        for index in indices:
        	address = start + index
        	address_list.append('%08x' % address)
        	#print('%08x' % address)	
        return address_list

    def find(self, gadget, condition=None):
        """
        Return the first result of find_all. If condition is specified, only
        consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(addr for addr in self.find_all(gadget) if condition(addr))
        except StopIteration:
            raise ValueError("Couldn't find matching address for " + gadget)

    def find_all_formats(self, gadget_format, registers=GENERAL_REGISTERS):
        """
        Similar to find_all - but return all the addresses of all
        possible gadgets that can be created with this format and registers.
        Every elemnt in the result will be a tuple of the gadget string and
        the address in which it appears.

        Example:
            self.find_all_formats('POP {0}; POP {1}')
            => [('POP eax; POP ebx', address1),
                ('POP ecx; POP esi', address2),
                ...]
        """
        str_list = self.format_all_gadgets(gadget_format,registers)
        arr = []
        for s in str_list:
        	for address in self.find_all(s):
        		arr.append((s,address))
        return arr


    def find_format(self, gadget_format, registers=GENERAL_REGISTERS, condition=None):
        """
        Return the first result of find_all_formats. If condition is specified,
        only consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(
                addr for addr in self.find_all_formats(gadget_format, registers)
                if condition(addr))
        except StopIteration:
            raise ValueError(
                "Couldn't find matching address for " + gadget_format)
