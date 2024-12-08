"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re
from SymbolTable import SymbolTable
from Code import Code

class Command:
    ''' keep track of commands and process their type:
    check for null, or A, C and L. 
    for each type, find key values.
    '''
    def __init__(self, command: str) -> None:
        self.command = command
        self._symbol = None
        self._comp = None
        self._dest = None
        self._jump = None
        self.command_type = None
        self._is_shift = False
        if command is None or command == '':
            self.command = None
            return

        self.command_type = self.check_type()  # so that always has some value
        self.process_c_command()
        self.process_symbol()
        self.check_shift()

    def check_type(self):
        """
        Determines the type of the assembly command.

        Returns:
            str: The command type ('A_COMMAND', 'C_COMMAND', 'L_COMMAND').
        """
        first_char = self.command[0]
        if first_char == "(":
            return "L_COMMAND"
        if first_char == "@":
            return "A_COMMAND"
        return "C_COMMAND"

    def process_symbol(self):
        """
        Extracts the symbol from A or L commands.
        """
        if self.command_type not in ('A_COMMAND', 'L_COMMAND'):
            return
        # Remove '@' or '(' and ')' from the command to get the symbol
        self._symbol = self.command[1:]
        if self.command_type == 'L_COMMAND':
            self._symbol = self._symbol[:-1]

    def process_c_command(self):
        """
        Parses the dest, comp, and jump parts of C commands.
        """
        if self.command_type != 'C_COMMAND':
            return
        # Use regex to parse the C command
        pattern = re.compile(r'(?:(?P<dest>[^=]+)=)?(?P<comp>[^;]+)(?:;(?P<jump>.+))?')
        match = pattern.match(self.command)
        if match:
            self._dest = match.group('dest')
            self._comp = match.group('comp')
            self._jump = match.group('jump')

    def check_shift(self):
        if self._comp is None: return
        if '<<' in self._comp or '>>' in self._comp:
            self._is_shift = True

    @property
    def type(self):
        """
        Returns the type of the command.

        Returns:
            str: The command type.
        """
        return self.command_type
    
    @property
    def is_shift(self):
        """
        Returns the symbol of the command.

        Returns:
            str: The symbol extracted from the command.
        """
        return self._is_shift
    
    @property
    def symbol(self):
        """
        Returns the symbol of the command.

        Returns:
            str: The symbol extracted from the command.
        """
        return self._symbol

    @property
    def dest(self):
        """
        Returns the dest part of the command.

        Returns:
            str: The dest mnemonic.
        """
        return self._dest

    @property
    def comp(self):
        """
        Returns the comp part of the command.

        Returns:
            str: The comp mnemonic.
        """
        return self._comp

    @property
    def jump(self):
        """
        Returns the jump part of the command.

        Returns:
            str: The jump mnemonic.
        """
        return self._jump

    def __repr__(self) -> str:
        """
        Returns a string representation of the command for debugging.

        Returns:
            str: A string representation of the command.
        """
        if self.command is None or self.command == '':
            return "null"
        details = [f"Command Type: {self.command_type}"]
        details.append(self.command)
        if self._symbol is not None:
            details.append(f"Symbol: {self._symbol}")
        if self._dest is not None:
            details.append(f"Dest: {self._dest}")
        if self._comp is not None:
            details.append(f"Comp: {self._comp}")
        if self._jump is not None:
            details.append(f"Jump: {self._jump}")
        return ", ".join(details)

class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.

    to deal with multi line comments, don't read line by line
    
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.
        

        Args:
            input_file (typing.TextIO): input file.
        """
        self.file_content = input_file.read()
        self.processed_lines = [] #save processed lines for second pass
        self.curr_line_counter = 0
        self.current_line = None
        self.curr_command = None
        self.ROM_command_count = 0 #if starts whitespace
        self.mlc = False #flag for multi line comment
        self.symbol_table = SymbolTable()
        self.first_pass = True
        self.second_pass = False
        self.coder = Code()
        self.remove_comments_and_whitespace()


    def remove_comments_and_whitespace(self):
        """
        Preprocesses the file content to remove comments and unnecessary whitespace.
        """
        # Remove block comments (/* */)
        content = re.sub(r'/\*.*?\*/', '', self.file_content, flags=re.DOTALL)
        # Split into lines
        lines = content.split('\n')
        self.processed_lines = []
        for line in lines:
            # Remove inline comments (//)
            line = re.sub(r'//.*', '', line)
            # Strip leading and trailing whitespace
            line = line.strip()
            # Remove all internal whitespace (spaces, tabs)
            line = re.sub(r'\s+', '', line)
            # Skip empty lines
            if not line:
                continue
            self.processed_lines.append(line)
            
    def has_more_commands(self) -> bool:
        """Are there more commands in the input?
        although, the first and second will have same num lines

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.curr_line_counter < len(self.processed_lines)


    def add_label_to_symbol_table(self):
        '''add label to symbol table
        take into account encountering label before decleration.
        only add label if being declared: (xxx)'''
        # check if label is being declared
        if self.curr_command.command.startswith("(") and self.curr_command.command.endswith(")"):
            #print(f'adding label  {self.symbol()} to symbol table with value {self.ROM_command_count}')
            #check if symbol already in table
            if not self.symbol_table.contains(self.symbol()):
                self.symbol_table.add_label(self.symbol(), self.ROM_command_count)

    def add_variable_to_symbol_table(self):
        """Adds a variable to the symbol table if it doesn't already exist."""
        if self.curr_command.command is None: return
        command_type = self.command_type()
        symbol = self.symbol()
        if command_type == 'A_COMMAND' and not symbol.isnumeric() and not self.symbol_table.contains(symbol):
            self.symbol_table.add_variable(symbol)

            
    def update_rom_count(self):
        if self.curr_command.type in ['A_COMMAND', 'C_COMMAND']:
            self.ROM_command_count += 1
            
    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.curr_line_counter >= len(self.processed_lines):
            return None

        file_line = self.processed_lines[self.curr_line_counter]
        self.curr_command = Command(file_line)

        if self.first_pass:
            if self.command_type() == 'L_COMMAND': self.add_label_to_symbol_table()
            self.update_rom_count()
        elif self.second_pass:
            self.add_variable_to_symbol_table()
            binary_command = self.get_command_binary()
            self.curr_line_counter += 1
            return binary_command

        self.curr_line_counter += 1
        return None

    def get_command_binary(self):
        if self.command_type() == 'A_COMMAND':
            return self.binarise_a()
        if self.command_type() == 'C_COMMAND':
            return self.binarise_c()
        return None

    def binarise_a(self):
        '''@Xxx where Xxx is either a symbol or a decimal number
        '''
        symbol = self.symbol()
        #if numeric:
        if symbol.isnumeric():
            return str('{0:016b}'.format(int(symbol)))
        #if variable:
        return str('{0:016b}'.format(self.symbol_table.get_address(symbol)))

    def binarise_c(self):
        '''dest=comp;jump
        '''
        dest = self.coder.dest(self.curr_command.dest)
        comp = self.coder.comp(self.curr_command.comp)
        jump = self.coder.jump(self.curr_command.jump)
        command_type = self.curr_command.type
        start = self.coder.start(command_type, self.curr_command.is_shift)
        return f"{start}{comp}{dest}{jump}"

    def prep_for_second_pass(self):
        self.first_pass = False
        self.second_pass = True
        self.curr_line_counter = 0
        self.curr_command = None
        return

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        return self.curr_command.type

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        return self.curr_command.symbol


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        return self.curr_command.dest

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        return self.curr_command.comp

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        return self.curr_command.jump