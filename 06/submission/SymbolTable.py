"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

VIRTUAL_REGISTERS = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15
}

NAMED_ADDRESSES = {
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    }
"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).


Usualy done by saving the translated code in memory 0-x (say 1024), and saving variables from x (1024):
Then each new varibale gets the next assigned the next address in the symbol table.
"""
"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).


Usualy done by saving the translated code in memory 0-x (say 1024), and saving variables from x (1024):
Then each new varibale gets the next assigned the next address in the symbol table.
"""


class SymbolTable:
    """
    A symbol table that keeps a correspondence between symbolic labels and
    numeric addresses.
    note that labels may be mapped to the same numbers as varaibles, but they refer to different mem devices (not problem of the symbol table)
    the table tracks RAM addreses used, the parser counts ROM commands
    """

    def __init__(self) -> None:
        """Creates a new symbol table initialized with all the predefined symbols
        and their pre-allocated RAM addresses, according to section 6.2.3 of the
        book.
        """
        # Your code goes here!
        next_free_ram_ind= len(VIRTUAL_REGISTERS.keys())
        def_table = VIRTUAL_REGISTERS
        def_table.update(NAMED_ADDRESSES)
        self.mapping_table = def_table
        self.next_free_ram_ind = next_free_ram_ind

    def get_next_free_ind(self):
        return self.next_free_ram_ind

    def add_label(self, symbol: str, rom_count: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        self.add_entry(symbol, rom_count)

    def add_variable(self, symbol: str) -> None:
        '''add variable to symbol table
        '''
        self.add_entry(symbol, self.next_free_ram_ind)
        self.next_free_ram_ind += 1

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        self.mapping_table[symbol] = address

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given symbol?

        Args:
            symbol (str): a symbol.

        Returns:
            bool: True if the symbol is contained, False otherwise.
        """
        return symbol in self.mapping_table.keys()

    def get_address(self, symbol: str) -> int:
        """Returns the address associated with the symbol.

        Args:
            symbol (str): a symbol.

        Returns:
            int: the address associated with the symbol.
        """

        return self.mapping_table[symbol]
